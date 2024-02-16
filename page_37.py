from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

#  37中文网
class SoupItemTable37:
    def __init__(self, brower , url: str):
        html = brower(url, 5)
        self.brower = brower
        self.soup = BeautifulSoup(html, 'html.parser')
        self.url = url

    def parser(self):
        tables = self.find_tables_of_contents()
        i, j = 0, 0

        ws = WriteStream()
        for (title, ref) in tables:
            j += 1
            item = SoupItemContent37(self.brower, ref)
            contents = item.parser()
            ws.add(title)
            ws.add_contents(contents)
            if j % 5 == 0:
                path = './tmp/' + str(i) + "_" + str(j) + ".txt"
                ws.write(path)
                i = j
        if j > i:
            path = './tmp/' + str(i) + "_" + str(j) + ".txt"
            ws.write(path)
            i = j

    def rebuild_url(self, href: str) -> str:
        parsered_url = urlparse(self.url)
        return "http://" + parsered_url.hostname + href

    def find_tables_of_contents(self) -> [(str, str)]:
        tables = self.soup.find("div", class_="listmain")
        a_tags = tables.find_all("a")
        table_contents = []
        for tag in a_tags:
            href = self.rebuild_url(tag.get("href"))
            # print(tag.text, href)
            tup = (tag.text, href)
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
        print(title)
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