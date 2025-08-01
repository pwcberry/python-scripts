"""Scans a web page for links to pages that contain links for PDF files to download"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import urljoin
import json
import ssl
import certifi
from argparse import ArgumentParser
import fetch_pdf

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"

class HyperlinkHTMLParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.page_links = set()

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            href = [attr_value for attr_name, attr_value in attrs if attr_name.lower() == 'href']
            if len(href) > 0:
                self.page_links.add(urljoin(self.base_url, href[0]))

    @property
    def size(self):
        return len(self.page_links)


def main(source_url, output_dir):
    try:
        # Download the page
        page_path = Path(output_dir, "page.html")
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        request = Request(source_url, headers={"User-Agent": USER_AGENT})
        response = urlopen(request, context=ssl_context)
        page_path.write_text(response.read().decode("utf-8"))

        # Parse the HTML
        page_parser = HyperlinkHTMLParser(source_url)
        page_parser.feed(page_path.read_text())
        json_path = Path(output_dir, "page_links.json")
        json_path.write_text(json.dumps(list(page_parser.page_links)))

        if page_parser.size > 0:
            for link in page_parser.page_links:
                fetch_pdf.fetch_pdf(link, output_dir)

    except URLError as e:
        print(f"Request error in batch: {e.reason}")
    except OSError as e:
        print(f"OS error in batch: {e}")
    except Exception as e:
        print(f"Unknown error: {e}")


if __name__ == '__main__':
    parser = ArgumentParser()
    # `source` must include domain and protocol
    parser.add_argument("source", type=str)
    # `output` must be an existing directory
    parser.add_argument("output", type=str)

    args = parser.parse_args()
    main(args.source, args.output)
