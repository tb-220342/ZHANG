# 语音识别模块
import json
import wave
import pyaudio
import numpy as np
from funasr_onnx import SenseVoiceSmall

with open('data/db/config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
asr_sensitivity = config["语音识别灵敏度"]
with open('data/set/more_set.json', 'r', encoding='utf-8') as file15:
    more_set = json.load(file15)
mic_num = int(more_set["麦克风编号"])
if asr_sensitivity == "高":
    SILENCE_DURATION = 2
elif asr_sensitivity == "中":
    SILENCE_DURATION = 3
else:
    SILENCE_DURATION = 4
FORMAT = pyaudio.paInt16
CHANNELS, RATE, CHUNK = 1, 16000, 1024
SILENCE_CHUNKS = SILENCE_DURATION * RATE / CHUNK
p = pyaudio.PyAudio()
stream, model = None, None
cache_path = "data/cache/cache_record.wav"


def rms(data):  # 计算rms值
    return np.sqrt(np.mean(np.frombuffer(data, dtype=np.int16) ** 2))


def dbfs(rms_value):  # 计算dbfs值
    return 20 * np.log10(rms_value / (2 ** 15))


def record_audio():  # 录音
    global stream
    frames = []
    recording = True
    silence_counter = 0
    if stream is None:
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK,
                        input_device_index=mic_num)
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)
        current_rms = rms(data)
        current_dbfs = dbfs(current_rms)
        if str(current_dbfs) != "nan":
            silence_counter += 1
            if silence_counter > SILENCE_CHUNKS:
                recording = False
        else:
            silence_counter = 0
    return b''.join(frames)


def recognize_audio(audiodata):  # 识别
    global model
    if model is None:
        model = SenseVoiceSmall("data/model/sensevoice-small-onnx-quant", batch_size=10, quantize=True)
    with wave.open(cache_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(audiodata)
    res = model(cache_path, language="auto", use_itn=False)
    info = res[0].split('<|')[1:]
    emotion = info[1].split('|>')[0]
    event = info[2].split('|>')[0]
    text = info[3].split('}')[0].split('|>')[1]
    emotion_dict = {"HAPPY": "[开心]", "SAD": "[伤心]", "ANGRY": "[愤怒]", "DISGUSTED": "[厌恶]",
                    "SURPRISED": "[惊讶]", "NEUTRAL": "", "EMO_UNKNOWN": ""}
    event_dict = {"BGM": "[背景音乐]", "Applause": "[鼓掌]", "Laughter": "[大笑]", "Cry": "[哭]",
                  "Sneeze": "[打喷嚏]", "Cough": "[咳嗽]", "Breath": "[深呼吸]", "Speech": "", "Event_UNK": ""}
    emotion = emotion_dict.get(emotion, emotion)
    event = event_dict.get(event, event)
    result = event + text + emotion
    return result
