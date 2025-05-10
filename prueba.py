"""from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.azlyrics.com/lyrics/oliviarodrigo/brutal.html')
# Interact with the page or wait for CAPTCHA resolution if necessary
content = driver.page_source
print(content)
driver.quit()"""

import httpx
from httpx_ip_rotator import ApiGatewayTransport


with ApiGatewayTransport("https://azlyrics.com") as g:
    mounts = {
        "https://azlyrics.com": g
    }
    with httpx.Client(mounts=mounts) as client:
        response = client.get("https://www.azlyrics.com/lyrics/oliviarodrigo/brutal.html")
        print(response.status_code)