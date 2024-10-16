import glob
import base64
import os
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
import easyocr
import os
import glob
import cv2
import numpy as np


# 从base64数据获得每个字的轮廓图片，文件名为加密后unicode，图片为加密前
def get_png():

    with open('glyph/font_base64.txt', 'r') as txt_file:
        base64_data = txt_file.read()

    with open("glyph/font.ttf", "wb") as ttf_file:  # 解码并保存为TTF文件
        ttf_file.write(base64.b64decode(base64_data))

    TTFont("glyph/font.ttf").saveXML("glyph/font.xml")  # 转xml

    tree = ET.parse("glyph/font.xml")
    root = tree.getroot()  # 根目录解析

    glyphs = root.findall(".//TTGlyph")

    for glyph in glyphs:
        name = glyph.attrib["name"]
        print(name)

        plt.figure(figsize=(6, 6))
        plt.axis('off')

        for contour in glyph.findall(".//contour"):
            x_coords = []
            y_coords = []

            for pt in contour.findall(".//pt"):
                x_coords.append(int(pt.attrib["x"]))
                y_coords.append(int(pt.attrib["y"]))

            x_coords.append(x_coords[0])
            y_coords.append(y_coords[0])  # 使轮廓线首位相连

            plt.plot(x_coords, y_coords, linestyle='-', color='black')  # 使用matplotlib绘图

        plt.savefig(f'glyph/{name}.png')
        plt.close()
        print(f'图片已保存:glyph/{name}.png')


def filler():
    for image_path in glob.glob("glyph/*.png"):
        print(image_path)
        img = cv2.imread(image_path)

        # 转换为灰度图像 二值化处理 反转黑白颜色(不然窗口的边框也会算一个轮廓)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        binary_img = cv2.bitwise_not(binary_img)

        # 查找轮廓
        contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print(hierarchy)

        # 创建一个空白图像用于绘制结果
        output_img = np.ones_like(img) * 255  # 白色背景

        contours_order = []

        # 子父轮廓编号
        # 从子到父
        for i, contour in enumerate(contours):
            _ = 0
            parent = hierarchy[0][i][3]
            while parent != -1:
                parent = hierarchy[0][parent][3]
                _ += 1
            contours_order.append(_)

        print(contours_order)

        for index in range(len(contours_order)):
            # 12黑，34白，56黑，以此类推
            if contours_order[index] // 2 % 2 == 1:
                cv2.drawContours(output_img, contours, index, (255, 255, 255), cv2.FILLED)
                cv2.imshow('Final Result', output_img)
                cv2.waitKey(125)

            elif contours_order[index] // 2 % 2 == 0:
                cv2.drawContours(output_img, contours, index, (0, 0, 0), cv2.FILLED)
                cv2.imshow('Final Result', output_img)
                cv2.waitKey(125)

        cv2.destroyAllWindows()
        cv2.imwrite(image_path, output_img)
        print(f'图片已保存:{image_path}')


def get_map():
    # 创建 EasyOCR 读取器
    reader = easyocr.Reader(['ch_sim'])  # 支持中文和英文
    dic = {}
    for image_path in glob.glob('glyph/*.png'):

        # 读取图片并进行 OCR
        result = reader.readtext(image_path)
        print(result)

        # 打印结果
        for detection in result:
            decrypted = detection[1]  # 提取识别的文字

            uni = image_path.split('uni')[-1].split('.')[0]
            encrypted = chr(int(uni, 16))
            dic[encrypted] = decrypted

            print(encrypted, decrypted)

        os.remove(image_path)
    return dic


if __name__ == "__main__":
    #  get_png()
    ...
