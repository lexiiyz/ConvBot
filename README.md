# ConvBot 🤖

A voice-controlled conversational AI assistant that can open apps, search the web, control your system, and chat with you in Indonesian.

## Features

- **Voice Input Recognition** - Speak to interact with ConvBot
- **Text-to-Speech Output** - Responses delivered via EdgeTTS with audio playback
- **App Opening** - Open applications on your system by voice command
- **Web Search** - Search the internet through voice commands
- **System Control** - Control WiFi and other system features
- **Media Playback Control** - Control Spotify and YouTube playback
- **Natural Chat** - Have conversations in Indonesian
- **Groq AI Integration** - Powered by Groq's fast API

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/lexiiyz/ConvBot.git
   cd convbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the root directory and add your Groq API key:
   ```
   GROQ_API_KEY=gsk_your_api_key_here
   ```
   
   Get your API key from [Groq Console](https://console.groq.com)

## Usage

Run the bot:
```bash
python main.py
```

Then speak your commands! Examples:
- "Open Spotify"
- "Search Python tutorials"
- "Turn off WiFi"
- "Play Levitating on Spotify"
- "Chat: How are you today?"

## Requirements

- Python 3.8+
- Groq API key
- Microphone for voice input
- Audio output device

## Dependencies

- `groq` - Groq API client
- `speech-recognition` - Voice input
- `AppOpener` - Open applications
- `edge-tts` - Text-to-speech
- `pygame` - Audio playback
- `python-dotenv` - Environment variable management

## License

MIT
