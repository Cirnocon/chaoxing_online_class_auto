from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import decoder

# selenium初始化
wd = webdriver.Edge()
wd.implicitly_wait(2)  # 是个宏


# 打开登录网站
wd.get('https://i.chaoxing.com/base?t=1727606960631')


# 用户登录
print(f'当前页面：{wd.title}')
wd.find_element(By.ID, 'phone').send_keys('13702134432')
wd.find_element(By.ID, 'pwd').send_keys('177497@Cirno')
wd.find_element(By.ID, 'loginBtn').click()  # 点击登录


# 个人空间
time.sleep(2)
print(f'当前页面：{wd.title}')
wd.switch_to.frame("frame_content")
wd.find_element(By.XPATH, '//li[@cname="音乐鉴赏"]').click()  # 点击课程


# 课程目录页面
time.sleep(2)
wd.switch_to.window(wd.window_handles[1])
print(f'当前页面：{wd.title}')
# wd.find_element(By.XPATH, '//div[@class="start-study readclosecoursepop"]')  # 我已阅读，进入小节
wd.switch_to.frame("frame_content-zj")
wd.find_element(By.XPATH, '//*[@class="chapter_unit"][1]//li[1]').click()  # 进入小节


# 学生学习界面遍历小节
time.sleep(2)
print(f'当前页面：{wd.title}')

# 关闭侧栏
wd.switch_to.default_content()
side_bar = wd.find_element(By.XPATH, '//div[@class="switchbtn"]')
side_bar.click()


while True:
    # 进入视频界面
    title = wd.find_elements(By.CLASS_NAME, 'spanText')
    title[-2].click()
    print('已切换进视频页面')
    time.sleep(0.5)

    # 判断任务点是否完成
    iframe_1 = wd.find_element(By.ID, 'iframe')
    wd.switch_to.frame(iframe_1)
    status_finished = wd.find_elements(By.XPATH, '//*[@aria-label="任务点已完成"]')
    
    # 视频未完成
    if len(status_finished) == 0:
        print('视频任务点未完成')
        iframe_2 = wd.find_element(By.XPATH, '//iframe[@class="ans-attach-online ans-insertvideo-online"]')
        wd.switch_to.frame(iframe_2)
        big_display_button = wd.find_element(By.CLASS_NAME, 'vjs-big-play-button')
        big_display_button.click()
        print('开始播放')
        time.sleep(1)

        # 等待视频播放完成
        while True:
            duration_bar = wd.find_element(By.XPATH, '//div[@class="vjs-play-progress vjs-slider-bar"]')
            duration_text = duration_bar.get_attribute('style')  # 形式如‘width：0.00;'
            duration_percent = float(duration_text.split('width:')[1].split('%')[0])  # 转换为浮点
            print(f'当前进度：{duration_percent}%')
            # 跳出判断
            if duration_percent == 100.0:
                break
            time.sleep(10)

    # 进入测验页面
    print('视频任务点完成')
    wd.switch_to.default_content()
    time.sleep(1)
    next_focus_button = wd.find_element(By.ID, 'prevNextFocusNext')
    next_focus_button.click()
    print('已切换进测验页面')
    time.sleep(0.5)

    # 判断任务点是否完成
    iframe_1 = wd.find_element(By.ID, 'iframe')
    wd.switch_to.frame(iframe_1)
    status_finished = wd.find_elements(By.XPATH, '//*[@aria-label="任务点已完成"]')

    # 测验未完成
    if len(status_finished) == 0:
        print('测验任务点未完成')

        iframe_2 = wd.find_element(By.XPATH, '//div[@class="ans-attach-ct"]/iframe')
        wd.switch_to.frame(iframe_2)

        iframe_3 = wd.find_element(By.ID, 'frame_content')
        wd.switch_to.frame(iframe_3)


        print('开始解码')
        script = wd.find_element(By.ID, 'cxSecretStyle')  # find</script>对象
        script_inner = script.get_attribute('innerHTML')  # 获取内部信息
        data_base64 = script_inner.split('base64,')[1].split('format')[0].split("'")[0]  # 切出base64部分

        with open('glyph/font_base64.txt', 'w') as file:
            file.write(data_base64)
        print('已保存:glyph/font_base64.txt')

        decoder.get_png()
        decoder.filler()
        a = decoder.get_map()




    # 完成
    wd.switch_to.default_content()
    next_focus_button = wd.find_element(By.ID, 'prevNextFocusNext')
    next_focus_button_re = wd.find_element(By.XPATH, '//*[@class="jb_btn jb_btn_92 fr fs14 nextChapter"]')
    next_focus_button.click()
    print('下一节')
    time.sleep(0.5)
    next_focus_button_re.click()
    print('下一节再确认')
    time.sleep(2)
    wd.switch_to.default_content()
