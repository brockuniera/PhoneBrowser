import HTMLParser
import requests


class WikiParse(HTMLParser.HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "start tag", tag

    def handle_endtag(self, tag):
        print "end tag", tag

    def handle_data(self, data):
        print "data", data


if __name__ == "__main__":
    parser = WikiParse()
