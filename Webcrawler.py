import argparse
from urllib import request
from bs4 import BeautifulSoup
import re


class Webcrawler():
    def __init__(self, file_name: str, queue_size: int = 1000):
        self.file_name = file_name
        self.queue_size = queue_size
        self.queue = set()
        self.visited = set()
        self.file = open(self.file_name, 'w')

        # [root_url] = (allowed, [disallowed subpaths])
        self.robot_files = {}

    def add_url(self, url: str):
        if len(self.queue) < self.queue_size:
            if url not in self.visited:
                self.queue.add(url)

    def next_url(self) -> str:
        if len(self.queue) > 0:
            next_url = self.queue.pop()
            self.visited.add(next_url)
            return next_url
        return None

    def get_root_url(self, url: str) -> str:
        # regex get the first part of url
        return re.search(r"(https?://[^/]+)", url).group(1)

    def robots_allowed(self, url: str) -> bool:
        root_url = self.get_root_url(url)

        if root_url in self.robot_files:
            if self.robot_files[root_url][0] == False:
                return False

            for ending in self.robot_files[root_url][1]:
                url_part = url[:len(root_url) + len(ending)]
                if url_part == root_url + ending:
                    return False
            return True

        else:
            try:
                response = request.urlopen(root_url + "/robots.txt")
                if response.getcode() == 200:
                    return self.read_robots(root_url, response)
                else:
                    self.robot_files[root_url][0] = True
                    return True
            except Exception as e:
                print(f"could not crawl url: {url} | {e.code}")
                return False

    def read_robots(self, root_url: str, response) -> bool:
        content = response.read().decode('utf-8')

        allowed = True
        disallowed = []
        for line in content.splitlines():
            if line.startswith("User-agent:"):
                if line.startswith("User-agent: *"):
                    allowed = True
                else:
                    allowed = False
                    break
            elif line.startswith("Disallow:"):
                disallowed.append(line[10:])

        self.robot_files[root_url] = allowed, disallowed
        return True

    def crawl_url(self, url: str):
        # read robots.txt
        if not self.robots_allowed(url):
            print(f"{url} does not allow robots")
            return

        try:
            response = request.urlopen(url)
            if response.getcode() == 200:
                self.parse_content(url, response.read())
        except Exception as e:
            print(f"could not crawl robot url: {url} | {e.code}")

    def save(self, url: str, text: list[str]):
        # self.file.write(f"{url}:{{\n")
        for line in text:
            self.file.write(f"{line.text}\n")
        # self.file.write(f"}},\n")

    def close_file(self):
        self.file.close()

    def parse_content(self, url: str, html: str):
        soup = BeautifulSoup(html, 'html.parser')
        heading = soup.find_all('h1')

        if heading:
            self.save(url, heading)

        for link in soup.find_all('a'):
            normalized_url = self.normalize_url(link.get('href'))
            if normalized_url is not None:
                self.add_url(normalized_url)

    def normalize_url(self, url: str):
        if url is not None and url.startswith("http"):
            return url

    def crawl(self, start_url: str, max_pages: int):
        self.add_url(start_url)
        while len(self.visited) < max_pages:
            url = self.next_url()
            if url is None:
                break
            print(f"visiting {url}")
            self.crawl_url(url)

        print(f"writing data to file '{self.file_name}'")
        self.close_file()


def init_argparser():
    parser = argparse.ArgumentParser(
        description='Crawl a website and save the headings to a file',
        usage='python Webcrawler.py [url] [max_pages] [file_name]'
    )
    parser.add_argument('-u', '--url', type=str,
                        help='the url to start crawling from')
    parser.add_argument("-p", '--max_pages', type=int,
                        help='the maximum number of pages to crawl')
    parser.add_argument('-f', '--file_name', type=str,
                        help='the name of the file to save the headings to')

    return parser.parse_args()


if __name__ == '__main__':
    args = init_argparser()

    spider = Webcrawler(args.file_name)
    spider.crawl(args.url, args.max_pages)
