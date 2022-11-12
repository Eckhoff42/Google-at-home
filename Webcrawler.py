from urllib import request
from bs4 import BeautifulSoup


class Webcrawler():
    def __init__(self, file_name: str, queue_size: int = 1000):
        self.file_name = file_name
        self.queue_size = queue_size
        self.queue = []
        self.visited = {}
        self.added = {}
        self.file = open(self.file_name, 'w')

    def add_url(self, url: str):
        if len(self.queue) < self.queue_size:
            if url not in self.visited and url not in self.added:
                self.queue.append(url)
                self.added[url] = True

    def next_url(self) -> str:
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None

    def crawl_url(self, url: str):
        self.visited[url] = True
        try:
            response = request.urlopen(url)
            if response.getcode() == 200:
                self.parse_content(url, response.read())
        except Exception as e:
            print(f"could not crawl url: {url}")
            print(e)

    def save(self, url: str, text: list[str]):
        self.file.write(f"{url}:{{\n")
        for line in text:
            self.file.write(f"{line.text},\n")
        self.file.write(f"}},\n")

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


if __name__ == '__main__':
    spider = Webcrawler('data.txt')

    spider.crawl_url(
        "https://www.vg.no/nyheter/innenriks/i/Kn8p34/rebekka-33-ventet-stroemregning-paa-3500-maa-i-stedet-ut-med-7500")
    spider.close_file()
