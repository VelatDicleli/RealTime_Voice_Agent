# 🎙️ RealTime Voice Agent

Gerçek zamanlı sesli AI asistan uygulaması. WebRTC tabanlı ses iletişimi, Groq Whisper ile ses tanıma, ElevenLabs ile ses sentezi ve LangGraph ReAct agent ile akıllı yanıtlar sunar.

## 🏗️ Mimari

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Kullanıcı     │────▶│   FastRTC       │────▶│   Groq Whisper  │
│   (Mikrofon)    │     │   (WebRTC)      │     │   (STT)         │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
┌─────────────────┐     ┌─────────────────┐     ┌────────▼────────┐
│   ElevenLabs    │◀────│   ReAct Agent   │◀────│   LangChain     │
│   (TTS)         │     │   (LangGraph)   │     │   Processing    │
└────────┬────────┘     └────────┬────────┘     └─────────────────┘
         │                       │
         │              ┌────────▼────────┐
         │              │   n8n Webhook   │
         │              │   (Tool Calls)  │
         │              └─────────────────┘
         ▼
┌─────────────────┐
│   Kullanıcı     │
│   (Hoparlör)    │
└─────────────────┘
```

## ✨ Özellikler

- **🎤 Gerçek Zamanlı Ses İletişimi**: FastRTC ve WebRTC ile düşük gecikmeli ses akışı
- **🗣️ Ses Tanıma (STT)**: Groq Whisper Large V3 modeli ile Türkçe ses tanıma
- **🔊 Ses Sentezi (TTS)**: ElevenLabs multilingual v2 modeli ile doğal Türkçe ses
- **🤖 Akıllı Agent**: LangGraph ReAct pattern ile araç kullanabilen AI asistan
- **🔧 Tool Calling**: n8n webhook entegrasyonu ile harici araç çağrıları
- **🌐 WebRTC**: Cloudflare TURN sunucuları ile güvenilir bağlantı
- **🎯 VAD**: Silero VAD ile akıllı konuşma algılama

## 🛠️ Mevcut Araçlar (Tools)

| Araç | Açıklama |
|------|----------|
| `retrieve_data_from_vector_store` | Vector store'dan veri sorgulama |
| `weather_info` | Hava durumu bilgisi alma |
| `email_send` | E-posta gönderme |
| `calendar_create` | Takvim etkinliği oluşturma |
| `append_sheets_row` | Google Sheets'e satır ekleme |

## 📋 Gereksinimler

- Python 3.10+
- Groq API Key
- ElevenLabs API Key
- Cloudflare TURN Credentials
- HuggingFace Token

## ⚙️ Kurulum

### 1. Repoyu klonlayın

```bash
git clone <repo-url>
cd RealTime_Voice_Agent
```

### 2. Sanal ortam oluşturun

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

### 4. Ortam değişkenlerini ayarlayın

Proje kök dizininde `.env` dosyası oluşturun:

```env
GROQ_API_KEY=your_groq_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
HF_TOKEN=your_huggingface_token
CLOUDFLARE_TURN_KEY_ID=your_cloudflare_turn_key_id
CLOUDFLARE_TURN_KEY_API_TOKEN=your_cloudflare_turn_api_token
```

## 🚀 Çalıştırma

```bash
python app.py
```

Uygulama varsayılan olarak `http://0.0.0.0:7866` adresinde başlayacaktır.

## 📁 Dosya Yapısı

```
RealTime_Voice_Agent/
├── app.py                  # Ana uygulama - WebRTC stream ve ses işleme
├── reAct_agent.py          # LangGraph ReAct agent tanımları
├── handle_tool_calling.py  # n8n webhook entegrasyonu
├── requirements.txt        # Python bağımlılıkları
├── .env                    # Ortam değişkenleri (oluşturulmalı)
└── README.md               # Bu dosya
```

## 🔧 Konfigürasyon

### VAD (Voice Activity Detection) Ayarları

`app.py` içinde VAD parametrelerini özelleştirebilirsiniz:

```python
algo_options=AlgoOptions(
    audio_chunk_duration=0.6,      # Ses parça süresi
    started_talking_threshold=0.2, # Konuşma başlangıç eşiği
    speech_threshold=0.1,          # Konuşma eşiği
),
model_options=SileroVadOptions(
    threshold=0.65,                # VAD eşiği
    min_speech_duration_ms=300,    # Minimum konuşma süresi
    min_silence_duration_ms=150,   # Minimum sessizlik süresi
),
```

### TTS Ayarları

ElevenLabs ses ayarlarını `tts_generate` fonksiyonunda değiştirebilirsiniz:

```python
voice_id="JBFqnCBsd6RMkjVDRZzb"  # Ses ID'si
model_id="eleven_multilingual_v2" # Model
language_code="tr"                # Dil
```

## 📡 n8n Webhook Entegrasyonu

Tool çağrıları `handle_tool_calling.py` üzerinden n8n webhook'una yönlendirilir. Webhook URL'ini güncellemek için:

```python
webhook_url = "https://your-n8n-instance/webhook/your-webhook-id"
```

Webhook'a gönderilen payload formatı:

```json
{
    "tool_name": "weather_info",
    "arguments": {
        "location": "Istanbul"
    }
}
```

## 🔄 Akış Diyagramı

1. **Kullanıcı konuşur** → Mikrofon sesi WebRTC üzerinden alınır
2. **VAD algılama** → Silero VAD konuşma durduğunda tetiklenir
3. **STT** → Groq Whisper sesi metne çevirir
4. **Agent işleme** → LangGraph ReAct agent metni işler
5. **Tool çağrısı** (opsiyonel) → Gerekirse n8n webhook'u çağrılır
6. **TTS** → ElevenLabs yanıtı sese çevirir
7. **Ses çıkışı** → Kullanıcıya sesli yanıt verilir

## 🐛 Sorun Giderme

### Ses algılanmıyor
- Mikrofon izinlerini kontrol edin
- VAD eşik değerlerini düşürün

### Yavaş yanıt
- İnternet bağlantınızı kontrol edin
- Groq API limitlerini kontrol edin

### Tool çağrıları çalışmıyor
- n8n webhook URL'inin doğru olduğundan emin olun
- Webhook'un aktif olduğunu kontrol edin

## 📜 Lisans

MIT License

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır. Büyük değişiklikler için önce bir issue açarak tartışmaya başlayın.

