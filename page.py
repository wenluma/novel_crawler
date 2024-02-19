from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys
class SoupItemTable:
    def __init__(self, brower, config):
        url = config['uri']
        html = brower(url, 5)
        self.brower = brower
        self.soup = BeautifulSoup(html, 'html.parser')
        self.url = url
        if 'start' in config:
            self.start = max(config['start'], 1)
        else:
            self.start = 1
        self.dir_name = './' + config['save_dir_name'] + '/'
        if 'end' in config:
            self.end = config['end']
        else:
            self.end = sys.maxsize

        if 'test' in config:
            self.test = config['test']
        else:
            self.test = False
        self.config = config

    def parser(self):
        if self.test:
            cell_config = self.config['chapter']
            tables = self.process_table()
            tables = tables[self.start - 1:self.end]
            for (title, ref) in tables:
                item = SoupItemContent(self.brower, cell_config, ref)
                contents = item.parser()
                for line in contents:
                    print(line)
                break
            return
        cell_config = self.config['chapter']
        tables = self.process_table()
        tables = tables[self.start - 1:self.end]
        i, j = 0, 0

        ws = WriteStream()
        for (title, ref) in tables:
            j += 1
            item = SoupItemContent(self.brower, cell_config, ref)
            contents = item.parser()
            ws.add(title)
            ws.add_contents(contents)
            if j % 5 == 0:
                path = self.dir_name + str(i + self.start) + "_" + str(j + self.start - 1) + ".txt"
                ws.write(path)
                i = j
        if j - i == 1:
            path = self.dir_name + str(i + self.start) + ".txt"
            ws.write(path)
            i = j
        elif j > i:
            path = self.dir_name + str(i + self.start) + "_" + str(j + self.start - 1) + ".txt"
            ws.write(path)
            i = j


    def rebuild_url(self, href: str) -> str:
        if href.startswith('//'):
            result = "https:" + href
            return result
        else:
            parsered_url = urlparse(self.url)
            return "http://" + parsered_url.hostname + href

    def find_tables_of_contents(self, value) -> [(str, str)]:
        table_contents = []
        tables = self.soup.find_all(value)
        for item in tables:
            tag = item.find("a")
            uri = "https:" + tag.get("href")
            tup = (tag.text, uri)
            table_contents.append(tup)
        return table_contents

    def process_table(self):
        config_list = self.config['table']
        for cell in config_list:
            type = cell['type']
            if type == 'id':
                value = cell['id']
                return self.find_tables_of_contents(value)

    def find_chatper_title(self) -> str:
        title = self.soup.title.string
        return title

class SoupItemContent:
    def __init__(self, brower, config, url):
        html = brower(url, 5)
        self.brower = brower
        self.config = config
        self.soup = BeautifulSoup(html, 'html.parser')
        self.url = url

    def parser(self):
        title = self.find_chatper_title()
        print(title, self.url)
        contents = self.find_chapter_content()
        # for line in contents:
            # print(line)
        return contents


    def find_chatper_title(self) -> str:
        title = self.soup.title.string
        return title

    def find_chapter_content(self) -> [str]:
        chapter_content = None
        cell = self.config
        type = cell['type']
        if type == 'id':
            value = cell['id']
            chapter_content = self.soup.find("div", id=value)
        result: [str] = []
        for item in chapter_content.contents:
            line = item.get_text().strip('\n').strip()
            if line != '':
                result.append(line)
        return result

class WriteStream:
    def __init__(self):
        self.lines = []

    def add(self, title: str):
        self.lines.append(title)
        self.lines.append('\n')

    def add_contents(self, lines: [str]):
        self.lines.extend(lines)

    def write(self, path):
        with open(path, 'w') as file:
            file.writelines("\n".join(self.lines))
            file.write('\n')
        self.lines.clear()