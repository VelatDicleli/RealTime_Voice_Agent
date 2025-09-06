import io
import os
import json
import numpy as np
import soundfile as sf
import re
from dotenv import load_dotenv
from fastrtc import (
    audio_to_bytes,
    get_cloudflare_turn_credentials,
    get_cloudflare_turn_credentials_async,
    Stream,
    ReplyOnPause,
    AlgoOptions,
    SileroVadOptions,
)
from handle_tool_calling import handle_tool_call
from reAct_agent import agent, agent_config
from groq import Groq
from elevenlabs import ElevenLabs

load_dotenv()

hf_token = os.environ.get("HF_TOKEN")
id = os.environ.get("CLOUDFLARE_TURN_KEY_ID")
id_token = os.environ.get("CLOUDFLARE_TURN_KEY_API_TOKEN")
groq_key = os.environ.get("GROQ_API_KEY")

groq_client = Groq(api_key=groq_key)
elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def mp3_to_frame(path: str):
    """MP3 dosyasını numpy audio frame’e çevirir"""
    data, samplerate = sf.read(path, dtype='float32')
    return samplerate, data  

def tts_generate(text: str):
    """ElevenLabs TTS ile text → audio çevirme"""
    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",  
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        language_code="tr",
    )
    
    tmp_path = "tts_output.mp3"
    with open(tmp_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    return mp3_to_frame(tmp_path)

def voice_agent(audio: tuple[int, np.ndarray]):
   
    transcript = groq_client.audio.transcriptions.create(
        file=("audio-file.mp3", audio_to_bytes(audio)),
        model="whisper-large-v3",
        language="tr",
        response_format="text",
    )
    print("Transkript:", transcript)

    try:
       
        agent_response = agent.invoke(
            {"messages": [{"role": "user", "content": transcript}]},
            config=agent_config,
        )
        response_text = agent_response["messages"][-1].content
        messages = agent_response["messages"]

        tool_result = None
        for msg in reversed(messages):
            if hasattr(msg, "additional_kwargs"):
                tool_calls = getattr(msg, "additional_kwargs").get("tool_calls", [])
                if tool_calls:
                    tc = tool_calls[-1]
                    tool_name = tc["function"]["name"]
                    args = json.loads(tc["function"]["arguments"])
                    tool_call = {"name": tool_name, "arguments": args}
                    tool_result = handle_tool_call(tool_call)
                    break

        final_text = response_text
        if tool_result:
            final_text += f'{tool_result["output"]}'

        clean_text = re.sub(r"[^\w\s]", "", final_text)

    except Exception as e:
        print(f"Agent işleme hatası: {e}")
        clean_text = "İşlem başarısız oldu."

    
    frame = tts_generate(clean_text)
    yield frame

def startup():
  
    frame = tts_generate("Merhaba! Size nasıl yardımcı olabilirim?")
    yield frame

async def get_credentials():
    return await get_cloudflare_turn_credentials_async(
        hf_token=hf_token,
        turn_key_api_token=id_token,
        turn_key_id=id
    )


stream = Stream(
    handler=ReplyOnPause(
        voice_agent,
        startup_fn=startup,
        algo_options=AlgoOptions(
            audio_chunk_duration=0.6,
            started_talking_threshold=0.2,
            speech_threshold=0.1,
        ),
        model_options=SileroVadOptions(
            threshold=0.65,
            min_speech_duration_ms=300,
            min_silence_duration_ms=150,
        ),
    ),
    rtc_configuration=get_credentials,
    server_rtc_configuration=get_cloudflare_turn_credentials(
        ttl=360_000,
        hf_token=hf_token,
        turn_key_api_token=id_token,
        turn_key_id=id
    ),
    modality="audio",
    mode="send-receive",
    ui_args={"title": "Sesli Asistan", "host": "0.0.0.0"},
)

if __name__ == "__main__":
    stream.ui.launch(server_port=7866)
