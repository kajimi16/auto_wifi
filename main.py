from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
import os
import time

# 设置环境变量禁用统计报告
os.environ["SE_SEND_STATS"] = "false"

# 初始化浏览器选项
options = webdriver.EdgeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")  # 设置窗口大小确保元素可见
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁用额外日志

try:
    # 初始化浏览器驱动
    driver = webdriver.Edge(options=options)
    
    # 设置超时时间
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(0)  # 禁用隐式等待，使用显式等待
    
    print("正在打开登录页面...")
    driver.get("http://10.248.98.2")
    username = input("请输入学号")
    password = input("请输入密码")
    
    
    try:
        # 等待并点击SSO登录按钮
        print("等待SSO登录按钮...")
        sso_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "login-sso"))
        )
        # 确保按钮可见
        driver.execute_script("arguments[0].scrollIntoView(true);", sso_button)
        time.sleep(0.5)  # 短暂等待滚动完成
        driver.execute_script("arguments[0].click();", sso_button)
        print("已点击SSO登录按钮")
        
        # 等待用户名输入框出现
        print("等待用户名输入框...")
        username_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#username[type='text']"))
        )
        
        # 确保元素可交互后再操作
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#username[type='text']"))
        )
        
        # 滚动到元素并高亮显示（调试用）
        driver.execute_script("arguments[0].scrollIntoView(true);", username_input)
        driver.execute_script("arguments[0].style.border='3px solid red';", username_input)
        time.sleep(0.5)
        
        # 使用JavaScript设置值
        driver.execute_script("arguments[0].value = arguments[1];", username_input, username)
        # 触发输入事件
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles: true}));", username_input)
        print("已输入用户名")
        
        # 等待密码输入框出现
        print("等待密码输入框...")
        password_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#password[type='password']"))
        )
        
        # 确保元素可交互
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#password[type='password']"))
        )
        
        # 滚动到元素并高亮显示
        driver.execute_script("arguments[0].scrollIntoView(true);", password_input)
        driver.execute_script("arguments[0].style.border='3px solid red';", password_input)
        time.sleep(0.5)
        
        # 使用JavaScript设置密码
        driver.execute_script("arguments[0].value = arguments[1];", password_input, password)
        # 触发输入事件
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles: true}));", password_input)
        print("已输入密码")
        
        # 等待登录按钮
        print("等待登录按钮...")
        login_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "login_submit"))
        )
        
        # 确保按钮可见
        driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
        driver.execute_script("arguments[0].style.border='3px solid green';", login_button)
        time.sleep(0.5)
        
        # 使用JavaScript点击
        driver.execute_script("arguments[0].click();", login_button)
        print("已点击登录按钮")
        
        # 等待登录完成
        print("等待登录结果...")
        try:
            # 等待登录后的元素出现或URL变化
            WebDriverWait(driver, 15).until(
                lambda d: "success" in d.current_url.lower() or 
                d.find_elements(By.CSS_SELECTOR, "div.login-success, div.logout-button")
            )
            print("登录成功!")
            
            # 保存截图确认状态
            driver.save_screenshot("login_success.png")
            print("已保存成功截图: login_success.png")
            
        except TimeoutException:
            print("登录状态验证超时")
            driver.save_screenshot("login_timeout.png")
            print("已保存超时截图: login_timeout.png")
            
    except TimeoutException as e:
        print(f"操作超时: {str(e)}")
        driver.save_screenshot("timeout_error.png")
        print("已保存超时错误截图: timeout_error.png")
        
    except ElementNotInteractableException as e:
        print(f"元素不可交互: {str(e)}")
        driver.save_screenshot("element_not_interactable.png")
        print("已保存元素不可交互截图: element_not_interactable.png")
        
    except Exception as e:
        print(f"发生未知错误: {str(e)}")
        driver.save_screenshot("unknown_error.png")
        print("已保存未知错误截图: unknown_error.png")
        # 保存页面源代码用于调试
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("已保存页面源代码: page_source.html")

finally:
    # 添加延迟确保操作完成
    time.sleep(3)
    # 关闭浏览器
    driver.quit()
    print("浏览器已关闭")