from html.parser import HTMLParser
from os.path import splitext
from urllib.request import urlretrieve
from pathlib import Path
from argparse import ArgumentParser

class HyperlinkHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.pdf_links = set()

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            href = [attr_value for attr_name, attr_value in attrs if attr_name.lower() == 'href']
            pdf = [link for link in href if splitext(link)[1] == '.pdf']
            if len(pdf) > 0:
                self.pdf_links.add(pdf[0])

def main(source, output):
    parser = HyperlinkHTMLParser()
    path = Path(output, "page.html")
    # TODO: Check for Windows
    filename, headers = urlretrieve(source, filename=path.as_posix())
    with open(filename, "r") as file:
        parser.feed(file.read())

    for link in parser.pdf_links:
        print(f"Downloading {link}...")
        path = Path(output, link)
        # TODO: Check for Windows
        urlretrieve(f"{source}{link}", filename=path.as_posix())

    print("\nDone.\n")

if __name__ == '__main__':
    parser = ArgumentParser()
    # `source` must include domain and protocol
    parser.add_argument("source", type=str)
    # `output` must be an existing directory
    parser.add_argument("output", type=str)
    main()
