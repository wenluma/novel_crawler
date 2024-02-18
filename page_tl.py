from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

#  天籁小说网
class SoupItemTableTL:
    def __init__(self, brower , url: str, test=False):
        html = brower(url, 5)
        self.brower = brower
        self.soup = BeautifulSoup(html, 'html.parser')
        self.url = url
        self.start_chapter = 435
        self.test = test

    def parser(self):
        if self.test:
            tables = self.find_tables_of_contents()
            for (title, ref) in tables:
                item = SoupItemContent37(self.brower, ref)
                contents = item.parser()
                for line in contents:
                    print(line)
                break
            return
        tables = self.find_tables_of_contents()

        tables = tables[self.start_chapter - 1:]
        i, j = 0, 0

        ws = WriteStream()
        for (title, ref) in tables:
            j += 1
            item = SoupItemContent37(self.brower, ref)
            contents = item.parser()
            ws.add(title)
            ws.add_contents(contents)
            if j % 5 == 0:
                path = './tmp1/' + str(i + self.start_chapter) + "_" + str(j + self.start_chapter) + ".txt"
                ws.write(path)
                i = j
        if j > i:
            path = './tmp1/' + str(i + self.start_chapter) + "_" + str(j + self.start_chapter) + ".txt"
            ws.write(path)
            i = j

    def rebuild_url(self, href: str) -> str:
        if href.startswith('//'):
            result = "https:" + href
            return result
        else:
            parsered_url = urlparse(self.url)
            return "http://" + parsered_url.hostname + href

    def find_tables_of_contents(self) -> [(str, str)]:
        table_contents = []
        tables = self.soup.find_all("dd")
        for item in tables:
            tag = item.find("a")
            uri = "https:" + tag.get("href")
            tup = (tag.text, uri)
            table_contents.append(tup)
        return table_contents

    def find_chatper_title(self) -> str:
        title = self.soup.title.string
        return title

    def find_chapter_content(self) -> [str]:
        chapter_content = self.soup.find("div", class_="chapter-content")
        result: [str] = []
        for item in chapter_content.contents:
            line = item.get_text()
            if line != '':
                result.append(line)
        return result

class SoupItemContent37:
    def __init__(self, brower, url):
        html = brower(url, 5)
        self.brower = brower
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
        # chapter_content = self.soup.find("div", class_="chapter-content")
        chapter_content = self.soup.find("div", id="content")
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