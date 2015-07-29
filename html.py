from lxml import html
from Queue import Queue
import threading


class Speaker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        import pyttsx

        self.voiceengine = pyttsx.init()
        # self.voiceengine.connect('started-word', self.onWord)

        self.wordqueue = Queue()

        self.shouldStop = False
        self.lock = threading.Lock()

    # Allow us to stop on words
    def onWord(self, name, location, length):
        if self._checkToStop():
            self.voiceengine.stop()

    def enqueue_words(self, words):
        self.wordqueue.put(words)

    def interrupt(self):
        """
        Sets the speaker to stop at the end of the next spoken word
        """
        self.lock.acquire()
        self.shouldStop = True
        self.lock.release()

    def _checkToStop(self):
        result = None
        self.lock.acquire()
        result = bool(self.shouldStop)
        self.lock.release()
        return result

    def run(self):
        self.voiceengine.startLoop(False)

        while True:
            print "getting..."
            item = self.wordqueue.get()
            print item
            self.voiceengine.say(item)
            self.voiceengine.iterate()

        self.voiceengine.endLoop()
        return


if __name__ == "__main__":
    # Get a webpage
    webtext = """
    <html>
    <body>
    <div id="mw-content-text">
    <p><a href='fuck'> dick </a></p>
    <p><a href='fuck'> cock </a></p>
    <p><a href='fuck'> brandon </a></p>
    <p><a href='fuck'> ayy </a></p>
    </div>
    </body>
    </html>
    """

    # Build and use our parser
    tree = html.fromstring(webtext)
    content = tree.xpath('//*[@id="mw-content-text"]')
    links = tree.xpath('//*[@id="mw-content-text"]/p/a')

    # Read links to user
    for i in xrange(0, len(links), 8):
        for j, link in enumerate(links[i:i + 8]):
            # Only print the first 9 entries
            # Then give a message for getting more choices

            output = 'Press {0} for {1}'.format(j + 1, link.text_content())
            print output
