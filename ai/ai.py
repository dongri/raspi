import openai
import speech_recognition as sr
from gtts import gTTS
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ.get("RASPI_OPENAI_API_KEY")

def listen_and_recognize():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak:")
        audio_data = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_data, language="zh-CN") # ja-JP: 日本語 / en-US: 英語 / zh-CN: 中国語
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None

def ask_openai(text):
    messages = [
        {"role": "system", "content": "你是我的助手"},
        {"role": "user", "content": text},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    return response.choices[0]["message"]["content"]

def speak(text):
    tts = gTTS(text=text, lang='zh')
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")

def main():
    while True:
        text = listen_and_recognize()
        if text:
            print(f"You: {text}")
            response = ask_openai(text)
            print(f"AI: {response}")
            speak(response)

if __name__ == "__main__":
    main()
