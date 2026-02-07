import os
import json
import asyncio
import webbrowser
import speech_recognition as sr
from groq import Groq
from AppOpener import open as open_app
import edge_tts
from datetime import datetime
import pygame
import subprocess
from dotenv import load_dotenv

try:
    pygame.mixer.init()
except pygame.error:
    print("⚠️ Warning: Audio device error")

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

# Validasi Key
if not API_KEY or "gsk_" not in API_KEY:
    print("❌ ERROR: API Key tidak valid. Cek file .env kamu!")
    exit()

client = Groq(api_key=API_KEY)

SYSTEM_PROMPT = """
You are ConvBot. Current time: {time}
Your Goal: Identify intention (OPEN apps, SEARCH content, CONTROL system, CHAT).
Output ONLY JSON.

JSON Formats:
- Action: {{"type": "action", "target": "target_name", "content": "search_query", "category": "web/app/sys/playback", "reply": "Confirmation"}}
- Chat: {{"type": "chat", "reply": "Response"}}
- Close: {{"type": "close", "reply": "Closing text"}}

Rules:
- PLAYBACK: target="spotify"/"youtube", content="song/video name". category="playback".
- SYSTEM: target="wifi_off"/"wifi_on".
- WEB: Must use FULL URL (https://...).
- APP: App name only.
- REPLY: Short conversational Indonesian.
"""

async def speak(text):
    """Mouth: EdgeTTS + Pygame"""
    print(f"🗣️  ConvBot: {text}")
    filename = "temp_voice.mp3"
    
    # Hapus file lama (biar gak error permission)
    if os.path.exists(filename):
        try:
            pygame.mixer.music.unload()
            os.remove(filename)
        except:
            pass 

    try:
        communicate = edge_tts.Communicate(text, "id-ID-ArdiNeural")
        await communicate.save(filename)
        
        if not pygame.mixer.get_init(): pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
            
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"Error Speak: {e}")

def listen_mic():
    """Ear: Whisper (Adaptive Listening)"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening... ")

        r.dynamic_energy_threshold = True
        r.pause_threshold = 1.0  
        
        r.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            audio = r.listen(source, timeout=None) 
            print("Thinking...")
            
            with open("temp_input.wav", "wb") as f:
                f.write(audio.get_wav_data())
            
            with open("temp_input.wav", "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=(file.name, file.read()), model="whisper-large-v3", language="id"
                )
            return transcription.text
        except sr.WaitTimeoutError:
            return None 
        except Exception:
            return None

def brain_process(text):
    """Brain: Llama 3"""
    print(f"👤 User: {text}")
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT.format(time=datetime.now())},
                {"role": "user", "content": text}
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error Brain: {e}")
        return {"type": "chat", "reply": "Maaf, error memproses."}

def control_system(command):
    """Hand: System Control"""
    try:
        if "wifi_off" in command:
            subprocess.run('netsh interface set interface "Wi-Fi" admin=disable', shell=True)
        elif "wifi_on" in command:
            subprocess.run('netsh interface set interface "Wi-Fi" admin=enable', shell=True)
    except Exception as e:
        print(f"Error Sys: {e}")

async def main():
    print("ConvBot - READY")
    print("Tip: Bilang 'Stop' atau 'Cukup' untuk mematikan.")
    
    while True:
        try:
            user_text = listen_mic()
            if not user_text: continue

            data = brain_process(user_text)

            if data["type"] == "close":
                await speak(data["reply"])
                print("👋 Bye! (Voice Stop)")
                break

            if data["type"] == "action":
                target = data["target"].lower()
                content = data.get("content", "")
                category = data.get("category", "")
                
                print(f"⚙️ Execute: {category} -> {target}")

                if category == "playback":
                    if "youtube" in target:
                        query = content.replace(" ", "+")
                        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                    
                    elif "spotify" in target:
                        if os.name == 'nt':
                            os.system(f'start spotify:search:"{content}"')
                        else:
                            webbrowser.open(f"spotify:search:{content}")

                elif category == "web":
                    if not target.startswith("http"): target = f"https://{target}"
                    webbrowser.open(target)

                elif category == "app":
                    open_app(target, match_closest=True)

                elif category == "sys":
                    if "off" in target:
                        await speak(data["reply"]) 
                        control_system(target)
                        continue
                    else:
                        control_system(target)
                        await asyncio.sleep(4)

            if "reply" in data and data["reply"]:
                await speak(data["reply"])
            
            await asyncio.sleep(0.5)

        except KeyboardInterrupt:
            print("\n👋 Bye! (Ctrl+C)")
            break
        except Exception as e:
            print(f"Critical Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())