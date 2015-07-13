import HTMLParser
import requests


def get_webtext(url="https://en.wikipedia.org/wiki/Deus_Ex"):
    page = requests.get(url)
    return page.text


class WikiParse(HTMLParser.HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            print "start tag", tag

    def handle_endtag(self, tag):
        print "end tag", tag

    def handle_data(self, data):
        print "data", data


if __name__ == "__main__":
    # GOAL: Read wikipedia.org/philosophy to user

    # Get a webpage
    webtext = get_webtext()

    # Build our parser
    parser = WikiParse()
    parser.feed("<html><body><p>asdf</p></html></body>")
