from selenium import webdriver
from page_37 import SoupItemTable37
import os

def setup_chrome_browser(url: str, time: float=5) -> str:
    # Set up browser
    driver = webdriver.Chrome()
    # Load the page
    driver.get(url)
    # Wait for JavaScript to finish loading
    driver.implicitly_wait(time)

    # Get the rendered HTML
    html_content = driver.page_source

    # Close the browser
    driver.quit()

    return html_content


def main():
    # 目标网站的URL
    url = 'https://www.tzkczc.com/19_19581/'
    item = SoupItemTable37(setup_chrome_browser, url)
    item.parser()

if __name__ == "__main__":
    main()
    # try:
    #     if os.path.exists('./tmp'):
    #         print('has tmp')
    #     else:
    #         os.mkdir('./tmp')
    # except OSError as e:
    #     print(e)
