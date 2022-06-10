import pyttsx3

text = 'какой-нибудь текст'
tts = pyttsx3.init()
rate = tts.getProperty('rate') #Скорость произношения
tts.setProperty('rate', rate-40)

volume = tts.getProperty('volume') #Громкость голоса
tts.setProperty('volume', volume+0.9)

voices = tts.getProperty('voices')

# Задать голос по умолчанию
tts.setProperty('voice', 'ru')
tts.setProperty('voice', RU_VOICE_ID)

tts.say(text)
tts.runAndWait()
