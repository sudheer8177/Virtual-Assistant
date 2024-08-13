import os
import time
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")

# Check if the API key is loaded properly
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in your .env file.")

# Configure Google Generative AI with the API key
genai.configure(api_key=api_key)

# Initialize the Generative Model with the specific model name
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            speak("I didn't hear anything, could you repeat?")
            return None
        except sr.UnknownValueError:
            print("Sorry, I did not catch that. Could you please repeat?")
            speak("Sorry, I didn't catch that. Can you please repeat?")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            speak("An error occurred while trying to recognize your voice.")
            return None

# Function to clean the generated text
def clean_text(text):
    # Remove unwanted characters such as asterisks
    return text.replace('*', '')

# Function to interact with Google's Gemini API using API key with retry mechanism
def ask_google(prompt, retries=3):
    try:
        # Generate content using the model
        response = model.generate_content(prompt)
        # Clean the generated text
        cleaned_text = clean_text(response.text)
        return cleaned_text
    except Exception as e:
        print(f"An error occurred while generating content: {e}")
        return "Sorry, I couldn't generate content at the moment."

# Main function to run the virtual assistant
def virtual_assistant():
    while True:
        print("Say something or 'exit' to quit.")
        query = listen()
        if query:
            if 'exit' in query.lower():
                speak("Goodbye!")
                break
            else:
                # Use the user's speech as the prompt for the AI model
                response = ask_google(query)
                print(f"Assistant: {response}")
                speak(response)

if __name__ == "__main__":
    try:
        virtual_assistant()
    except KeyboardInterrupt:
        print("\nAssistant stopped by user. Exiting...")
        speak("Goodbye!")
