from selenium import webdriver
# from page_tl import SoupItemTableTL
from page import SoupItemTable
import os
import yaml

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


def main(config):
    # 目标网站的URL
    # url = 'https://www.tzkczc.com/19_19581/'
    print(f'start: {config['uri']}')
    item = SoupItemTable(setup_chrome_browser, config)
    item.parser()
    print('done')

def open_yaml():
    with open('config.yaml', 'r') as file:
        data = yaml.safe_load(file)
        return data

def create_dir_if_needed(dir_name):
    try:
        current_path = './' + dir_name
        if os.path.exists(current_path):
            print('has ' + dir_name)
        else:
            os.mkdir(current_path)
    except OSError as e:
        print(e)


if __name__ == "__main__":
    key = 'TL'
    yaml_data = open_yaml()
    single = yaml_data[key]
    create_dir_if_needed(single['save_dir_name'])
    main(single)
