# Seckill_Shopping
聚划算手机扫码登录
### Basis
* 解决 Python 安装第三方库时超时报错（Read timed out）

`pip --default-timeout=100 install -U 第三方库名`
* web端自动化测试框架 `selenium`

`from selenium import webdriver`
* 下载 [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)，拷贝到 `/usr/local/bin/` 目录下

```
from selenium import webdriver

chrome_driver = '/usr/local/bin/chromedriver'
browser = webdriver.Chrome(chrome_driver)
browser.get('https://www.google.com.hk/')
```
> 运行上面代码，会自动打开Google Chrome，然后访问 Google

### 聚划算秒杀
* 扫二维码登录
```
def login_by_qcode():
    qcode = driver.find_element_by_id("J_QRCodeImg")

    action = ActionChains(driver)
    action.reset_actions()
    action.move_to_element(qcode)
    action.move_by_offset(20, -20).click()
    action.perform()

    while True:
        url = driver.current_url

        if not url.startswith("https://login.taobao.com"):
            cookies = driver.get_cookies()
            res = ""
            for cookie in cookies:
                res += cookie.get('name') + '=' + cookie.get('value') + ';'

            res = res[:-1]
            print(res)
            break

        try:
            refresh = driver.find_element_by_class_name("J_QRCodeRefresh")
            refresh.click()
        except:
            pass

        time.sleep(6)
```

* 进入秒杀页面
```
def enter_seckill_page(url):
    driver.get(url)
```
* 判断是否可抢
```
def confirm_seckill():
    is_seckill = True
    while True:
        try:
            # 未开团
            driver.find_element_by_class_name('J_JuSMSRemind')
            is_seckill = False
        except Exception as e:
            print("we can seckill now !")
            is_seckill = True

        if not is_seckill:
            time.sleep(6)
            enter_seckill_page('开团提醒页面URL')
        else:
            submit = driver.find_element_by_class_name('J_BuySubmit')
            submit.click()
            break
```
