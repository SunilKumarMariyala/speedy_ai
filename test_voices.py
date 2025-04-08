import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

print("🗣️ Available Voices:\n")

for index, voice in enumerate(voices):
    print(f"{index}: {voice.name} - {voice.id}")
    engine.setProperty('voice', voice.id)
    engine.say(f"This is voice number {index}. Hello Sunil, I am Speedy, your assistant.")
    engine.runAndWait()
