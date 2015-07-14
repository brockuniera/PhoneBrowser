from HTMLParser import HTMLParser
import requests


def get_webtext(url="https://en.wikipedia.org/wiki/Deus_Ex"):
    page = requests.get(url)
    return page.text


class WikiParse(HTMLParser):

    def __init__(self):
        """
        Initialize variables to keep track of state
        """
        HTMLParser.__init__(self)
        self.allow_printing = False
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        # Find the div we care about; it has id="mw-content-text"
        if not self.allow_printing:
            for tup in attrs:
                if 'id' == tup[0] and 'mw-content-text' in tup[1:]:
                    self.allow_printing = True
                    break

        # Once we do, start printing data and keeping track of depth
        if self.allow_printing:
            self.depth += 1

    def handle_endtag(self, tag):
        # If we encounter an end tag with the same depth as
        # our starting div, we should stop!
        if self.allow_printing:
            self.depth -= 1
            if self.depth == 0:
                self.allow_printing = False

    def handle_data(self, data):
        # Once we find our div, start printing everything
        if self.allow_printing:
            print data


if __name__ == "__main__":
    # GOAL: Read wikipedia.org/philosophy to user

    # Get a webpage
    webtext = get_webtext()

    # Build our parser
    parser = WikiParse()
    parser.feed(webtext)
