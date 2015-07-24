import pyttsx

words = ['callen', 'is', 'gay']

engine = pyttsx.init()
for word in words:
    engine.say(word)
    engine.runAndWait()
