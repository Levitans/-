# -*- encoding = utf-8 -*-
# @Time : 2022-04-16 0:08
# @Author : Levitan
# @File : learn_helper.py
# @Software : PyCharm
import time
import traceback

from package.learn import globalvar as gl
from package.learn import color
from package.learn.mydriver import MyDriver
from package.learn.school import fuist
from package.learn.display import Display, MyFormat
from package.learn.task.quiz.quiz import QuizOfTask, QuizOfHomework
from package.learn.task.audio import Audio
from package.learn.task.video import Video
from package.learn.task.ppt import PPT
from package.learn import color

from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait


def automatic_learning(driver):
    learn = fuist
    driver.go_courses_page()

    # 获取所有课程
    try:
        courses_list = learn.get_courses(driver.get_driver())
    except exceptions.NoSuchElementException as e:
        errInfo = traceback.format_exc()
        gl.exception_log_manger.writeLog(errInfo)
        raise Exception("获取课程时出现异常："+str(e)+"\n可能原因见：package\\learn\\school\\README.md")
    print(color.blue("当前课程有："))
    Display.printTable([i.name for i in courses_list], MyFormat([50, 50], displayNumber=True))
    index = int(input("\n输入课程序号：")) - 1
    course = courses_list[index]
    Display.separate()

    # 获取所有章节
    driver.get_url(course.get_ZJ_path())
    driver.driver_wait(By.CLASS_NAME, "chapter_td")
    try:
        chapter_list = learn.get_chapters(driver.get_driver())
    except exceptions.NoSuchElementException as e:
        errInfo = traceback.format_exc()
        gl.exception_log_manger.writeLog(errInfo)
        raise Exception("获取章节时出现异常："+str(e)+"\n可能原因见：package\\learn\\school\\README.md")

    # 跳过已完成的章节
    for i in chapter_list:
        if i.isFinish:
            print("章节：" + color.green(i.name) + " 已经完成")
        else:
            print("章节：" + color.blue(i.name) + " 未完成")
            i.webElement.click()
            break
    Display.separate()

    # 收起目录栏
    driver.get_driver().find_element(By.CLASS_NAME, "switchbtn").click()
    time.sleep(1)
    driver.go_js("var q=document.documentElement.scrollTop=10000")
    time.sleep(0.5)

    # 循环所有章节
    while True:
        # 寻找是否有选项卡
        prev_table_list = []
        try:
            prev_table_list = driver.get_driver().find_element(By.CSS_SELECTOR, '[class="prev_tab"]') \
                .find_element(By.CSS_SELECTOR, '[class="prev_ul"]') \
                .find_elements(By.TAG_NAME, 'li')
        except exceptions.NoSuchElementException:
            pass
        prev_table_number = len(prev_table_list) if len(prev_table_list) != 0 else 1  # 选项卡个数
        print("当前章节选项卡有 " + str(prev_table_number) + " 个")

        # 遍历每个选项卡
        for tableIndex in range(prev_table_number):
            # 第一个选项卡不用点击
            if tableIndex != 0:
                item = prev_table_list[tableIndex].find_element(By.TAG_NAME, 'div')
                driver.get_driver().execute_script("arguments[0].scrollIntoView(false);", item)
                item.click()
                time.sleep(1)

            # 进入第一层iframe
            driver.get_driver().switch_to.frame("iframe")
            iframeList = driver.get_driver().find_elements(By.TAG_NAME, 'iframe')
            print("当前章节有 " + color.yellow(str(len(iframeList))) + " 个任务点")

            # 遍历每个任务点
            for i in range(len(iframeList)):
                print("当前为第 " + color.blue(str(i + 1)) + " 任务点")

                # 循环判断任务点类型
                # 因为当前 QuizOfTask 类型任务点还没有欧判读方法，所以 QuizOfTask 任务放在元组最后面
                for item in (PPT, Video, Audio, QuizOfTask):
                    task = item(driver.get_driver())
                    if task.isCurrentTask(i):
                        print("当前任务点是 " + color.green(task.__name__))
                        driver.get_driver().switch_to.frame(iframeList[i])
                        try:
                            task.finish()
                            break
                        except Exception as e:
                            errInfo = traceback.format_exc()
                            gl.exception_log_manger.writeLog(errInfo)
                            driver.get_driver().switch_to.default_content()
                            print(color.read("当前任务点 {} 运行时出错".format(task.__name__)))
                            print(color.read(str(e)))
                            print("跳过当前任务点")
                            break
                    else:
                        print("当前任务点不是 " + color.yellow(task.__name__))
                Display.separate()
                driver.get_driver().switch_to.default_content()
                driver.get_driver().switch_to.frame("iframe")
                iframeList = driver.get_driver().find_elements(By.TAG_NAME, 'iframe')
            driver.get_driver().switch_to.default_content()
        print("当前章节已完成")
        Display.separate()
        next_button = driver.is_element_presence(By.CSS_SELECTOR, '[class="jb_btn jb_btn_92 fs14 prev_next next"]')
        if next_button is not None:
            next_button.click()
            driver.driver_wait(By.CLASS_NAME, "course_main")
        else:
            print("课程学习完毕")
            exit()


def do_homework(driver: MyDriver):
    school = fuist
    driver.go_courses_page()

    # 获取所有课程
    try:
        courses_list = school.get_courses(driver.get_driver())
    except exceptions.NoSuchElementException as e:
        errInfo = traceback.format_exc()
        gl.exception_log_manger.writeLog(errInfo)
        raise Exception("获取课程时出现异常："+str(e)+"\n可能原因见：package\\learn\\school\\README.md")
    print(color.blue("当前课程有："))
    Display.printTable([i.name for i in courses_list], MyFormat([50, 50], displayNumber=True))
    index = int(input("\n输入课程序号：")) - 1
    course = courses_list[index]
    Display.separate()

    # 进入作业
    driver.get_url(course.url)
    driver.driver_wait(By.CLASS_NAME, "nav_side")

    key_value = driver.get_driver().find_element(By.CLASS_NAME, "nav_side") \
        .find_element(By.CSS_SELECTOR, '[class="nav-content   stuNavigationList"]')

    key_value_dict = {}
    for i in key_value.find_elements(By.TAG_NAME, "input"):
        key_value_dict[i.get_attribute("id")] = i.get_attribute("value")

    ZY_url = "https://mooc1.chaoxing.com/mooc2/work/list?" \
             "courseId=" + key_value_dict['courseid'] + \
             "&classId=" + key_value_dict['clazzid'] + \
             "&cpi=" + key_value_dict['cpi'] + \
             "&ut=s" \
             "&enc=" + key_value_dict['workEnc']
    driver.get_url(ZY_url)
    driver.driver_wait(By.CLASS_NAME, "bottomList")

    homework_url_list = []
    item = driver.get_driver().find_element(By.CLASS_NAME, "bottomList").find_elements(By.TAG_NAME, "li")
    for i in item:
        if i.find_element(By.CSS_SELECTOR, '[class="status fl"]').text == "已完成":
            continue
        homework_url_list.append(i.get_attribute("data"))

    print("当前未提交作业有：{} 份".format(len(homework_url_list)))
    for i in range(len(homework_url_list)):
        print("正在完成作业 {} ".format(i+1))
        driver.get_url(homework_url_list[i])
        time.sleep(1)
        quiz = QuizOfHomework(driver.get_driver())
        try:
            quiz.finish()
        except Exception as e:
            errInfo = traceback.format_exc()
            gl.exception_log_manger.writeLog(errInfo)
            print(color.read("完成作业 "+str(i+1)+" 时出现异常："+str(e)))
            print(color.read("跳过这份作业"))
        driver.get_driver().back()
        time.sleep(1)

