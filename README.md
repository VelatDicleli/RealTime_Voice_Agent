# 🎙️ RealTime Voice Agent

A real-time voice AI assistant application. Features WebRTC-based audio communication, speech recognition with Groq Whisper, voice synthesis with ElevenLabs, and intelligent responses powered by LangGraph ReAct agent.

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│      User       │────▶│    FastRTC      │────▶│  Groq Whisper   │
│   (Microphone)  │     │    (WebRTC)     │     │     (STT)       │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
┌─────────────────┐     ┌─────────────────┐     ┌────────▼────────┐
│   ElevenLabs    │◀────│   ReAct Agent   │◀────│   LangChain     │
│     (TTS)       │     │   (LangGraph)   │     │   Processing    │
└────────┬────────┘     └────────┬────────┘     └─────────────────┘
         │                       │
         │              ┌────────▼────────┐
         │              │   n8n Webhook   │
         │              │   (Tool Calls)  │
         │              └─────────────────┘
         ▼
┌─────────────────┐
│      User       │
│    (Speaker)    │
└─────────────────┘
```

## ✨ Features

- **🎤 Real-Time Audio Communication**: Low-latency audio streaming with FastRTC and WebRTC
- **🗣️ Speech Recognition (STT)**: Turkish speech recognition using Groq Whisper Large V3
- **🔊 Voice Synthesis (TTS)**: Natural Turkish voice with ElevenLabs Multilingual V2
- **🤖 Intelligent Agent**: AI assistant with tool-calling capabilities using LangGraph ReAct pattern
- **🔧 Tool Calling**: External tool invocation via n8n webhook integration
- **🌐 WebRTC**: Reliable connections through Cloudflare TURN servers
- **🎯 VAD**: Smart speech detection with Silero VAD

## 🛠️ Available Tools

| Tool | Description |
|------|-------------|
| `retrieve_data_from_vector_store` | Query data from vector store |
| `weather_info` | Get current weather information |
| `email_send` | Send email |
| `calendar_create` | Create calendar event |
| `append_sheets_row` | Append row to Google Sheets |

## 📋 Requirements

- Python 3.10+
- Groq API Key
- ElevenLabs API Key
- Cloudflare TURN Credentials
- HuggingFace Token

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd RealTime_Voice_Agent
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
HF_TOKEN=your_huggingface_token
CLOUDFLARE_TURN_KEY_ID=your_cloudflare_turn_key_id
CLOUDFLARE_TURN_KEY_API_TOKEN=your_cloudflare_turn_api_token
```

## 🚀 Usage

```bash
python app.py
```

The application will start at `http://0.0.0.0:7866` by default.

## 📁 Project Structure

```
RealTime_Voice_Agent/
├── app.py                  # Main application - WebRTC stream & audio processing
├── reAct_agent.py          # LangGraph ReAct agent definitions
├── handle_tool_calling.py  # n8n webhook integration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
└── README.md               # This file
```

## 🔧 Configuration

### VAD (Voice Activity Detection) Settings

Customize VAD parameters in `app.py`:

```python
algo_options=AlgoOptions(
    audio_chunk_duration=0.6,      # Audio chunk duration
    started_talking_threshold=0.2, # Speech start threshold
    speech_threshold=0.1,          # Speech threshold
),
model_options=SileroVadOptions(
    threshold=0.65,                # VAD threshold
    min_speech_duration_ms=300,    # Minimum speech duration
    min_silence_duration_ms=150,   # Minimum silence duration
),
```

### TTS Settings

Modify ElevenLabs voice settings in the `tts_generate` function:

```python
voice_id="JBFqnCBsd6RMkjVDRZzb"  # Voice ID
model_id="eleven_multilingual_v2" # Model
language_code="tr"                # Language
```

## 📡 n8n Webhook Integration

Tool calls are routed to n8n webhook via `handle_tool_calling.py`. To update the webhook URL:

```python
webhook_url = "https://your-n8n-instance/webhook/your-webhook-id"
```

Payload format sent to webhook:

```json
{
    "tool_name": "weather_info",
    "arguments": {
        "location": "Istanbul"
    }
}
```

## 🔄 Flow Diagram

1. **User speaks** → Microphone audio captured via WebRTC
2. **VAD detection** → Silero VAD triggers when speech stops
3. **STT** → Groq Whisper converts speech to text
4. **Agent processing** → LangGraph ReAct agent processes the text
5. **Tool call** (optional) → n8n webhook invoked if needed
6. **TTS** → ElevenLabs converts response to speech
7. **Audio output** → Voice response played to user

## 🐛 Troubleshooting

### Audio not detected
- Check microphone permissions
- Lower VAD threshold values

### Slow response
- Check your internet connection
- Verify Groq API rate limits

### Tool calls not working
- Ensure n8n webhook URL is correct
- Verify webhook is active

## 📜 License

MIT License

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
