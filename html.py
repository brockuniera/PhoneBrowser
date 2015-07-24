from HTMLParser import HTMLParser
import requests
import pyttsx

from pprint import pprint


def get_webtext(url):
    page = requests.get(url)
    return page.text


def getAttrInListOfTuples(attr, theList):
    for tup in theList:
        if attr == tup[0]:
            return tup[1]


class WikiParse(HTMLParser):

    def __init__(self):
        """
        Initialize variables to keep track of state
        """
        # Call parent constructor
        HTMLParser.__init__(self)

        # State for tracking depth
        self.allow_printing = False
        self.depth = 0
        self.currenttag = ''

        # Array of content things
        self.output = []
        # A list of dictionaries, with keys = ['href', 'content']
        self.links = []

        self.num = 0

    def handle_starttag(self, tag, attrs):
        self.num += 1
        print self.num

        # Find the div we care about; it has id="mw-content-text"
        if not self.allow_printing:
            for tup in attrs:
                # Look for a tag with mw-content-text as id
                if 'id' == tup[0] and 'mw-content-text' in tup[1:]:
                    self.allow_printing = True
                    break

        # Once we do, start printing data and keeping track of depth
        if self.allow_printing:
            self.depth += 1
            self.currenttag = tag

            # import pdb; pdb.set_trace()

            if self.currenttag == 'a':
                self.links.append({
                    'href': getAttrInListOfTuples(u'href', attrs)
                })

    def handle_endtag(self, tag):
        # If we encounter an end tag with the same depth as
        # our starting div, we should stop!
        if self.allow_printing:
            self.depth -= 1
            if self.depth == 0:
                self.allow_printing = False

    def handle_data(self, data):
        print self.num
        # Once we find our div, start capturing everything
        if self.allow_printing:
            if self.depth < 4:
                # Capture this data in the ouput list
                self.output.append(data.encode('ascii', 'ignore'))
            if self.currenttag == 'a':
                # Capture links
                print data
                self.links[-1]['content'] = data

if __name__ == "__main__":
    # GOAL: Read wikipedia.org/philosophy to user

    # Get a webpage
    # webtext = get_webtext("https://en.wikipedia.org/wiki/Deus_Ex")
    webtext = """
    <html id="mw-content-text">
    <body>
    <a href='fuck'> dick<p>asdf</p> </a>
    </body>
    </html>

    """

    # Build and use our parser
    parser = WikiParse()
    parser.feed(webtext)

    # Create speaking engine
    engine = pyttsx.init()
    import pdb; pdb.set_trace()
    engine.say([item['content'] for item in parser.links])
    engine.setProperty('voices', u'com.apple.speech.synthesis.voice.Hysterical')
    engine.runAndWait()
