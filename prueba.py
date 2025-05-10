from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.azlyrics.com/lyrics/oliviarodrigo/brutal.html')
# Interact with the page or wait for CAPTCHA resolution if necessary
content = driver.page_source
print(content)
driver.quit()