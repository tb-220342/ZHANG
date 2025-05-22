# 语音合成模块
import asyncio
import edge_tts
import librosa
import pyttsx3
import numpy as np
from function import *

voice_path = 'data/cache/cache_voice'
try:
    engine = pyttsx3.init()
except:
    pass
lang_mapping = {"中文": "zh", "英语": "uk", "日语": "jp"}
select_lang = lang_mapping.get(paddle_lang, "kor")
edge_speaker_mapping = {"晓艺-年轻女声": "zh-CN-XiaoyiNeural", "晓晓-成稳女声": "zh-CN-XiaoxiaoNeural",
                        "云健-大型纪录片男声": "zh-CN-YunjianNeural", "云希-短视频热门男声": "zh-CN-YunxiNeural",
                        "云夏-年轻男声": "zh-CN-YunxiaNeural", "云扬-成稳男声": "zh-CN-YunyangNeural",
                        "晓北-辽宁话女声": "zh-CN-liaoning-XiaobeiNeural",
                        "晓妮-陕西话女声": "zh-CN-shaanxi-XiaoniNeural", "晓佳-粤语成稳女声": "zh-HK-HiuGaaiNeural",
                        "晓满-粤语年轻女声": "zh-HK-HiuMaanNeural", "云龙-粤语男声": "zh-HK-WanLungNeural",
                        "晓辰-台湾话年轻女声": "zh-TW-HsiaoChenNeural", "晓宇-台湾话成稳女声": "zh-TW-HsiaoYuNeural",
                        "云哲-台湾话男声": "zh-TW-YunJheNeural", "佳太-日语男声": "ja-JP-KeitaNeural"}
edge_select_speaker = edge_speaker_mapping.get(edge_speaker, "ja-JP-NanamiNeural")


def play_voice():  # 播放语音
    def play_mp3_th():
        pg.init()
        try:
            pg.mixer.music.load(voice_path)
            pg.mixer.music.play()
            while pg.mixer.music.get_busy():
                pg.time.Clock().tick(1)
            pg.mixer.music.stop()
        except:
            pass
        pg.quit()

    Thread(target=play_mp3_th).start()


def get_tts_play_live2d(text):  # 获取并播放语音
    async def ms_edge_tts():
        communicate = edge_tts.Communicate(text, edge_select_speaker, rate=f"{edge_rate}%", pitch=f"{edge_pitch}Hz")
        await communicate.save(voice_path)

    text = text.split("</think>")[-1].strip()
    try:
        if tts_menu.get() == "云端edge-tts":
            asyncio.run(ms_edge_tts())
            play_voice()
        elif tts_menu.get() == "云端百度TTS":
            url = f'https://fanyi.baidu.com/gettts?lan={select_lang}&spd={paddle_rate}&text={text}'
            response = rq.get(url)
            wav_data = response.content
            with open(voice_path, 'wb') as f:
                f.write(wav_data)
            play_voice()
        elif tts_menu.get() == "本地GPT-SoVITS":
            url = f'http://{local_server_ip}:{gsv_port}/?text={text}&text_language={gsv_lang}'
            try:
                response = rq.get(url)
                wav_data = response.content
                with open(voice_path, 'wb') as f:
                    f.write(wav_data)
                play_voice()
            except Exception as e:
                notice(f"本地GPT-SoVITS整合包API服务器未开启，错误详情：{e}")
        elif tts_menu.get() == "本地CosyVoice":
            url = f'http://{local_server_ip}:{cosy_port}/cosyvoice/?text={text}'
            try:
                response = rq.get(url)
                wav_data = response.content
                with open(voice_path, 'wb') as f:
                    f.write(wav_data)
                play_voice()
            except Exception as e:
                notice(f"本地CosyVoice整合包API服务器未开启，错误详情：{e}")
        elif tts_menu.get() == "本地Kokoro-TTS":
            url = f'http://{local_server_ip}:9882/kokoro/?text={text}'
            try:
                response = rq.get(url)
                wav_data = response.content
                with open(voice_path, 'wb') as f:
                    f.write(wav_data)
                play_voice()
            except Exception as e:
                notice(f"本地Kokoro-TTS整合包API服务器未开启，错误详情：{e}")
        elif tts_menu.get() == "本地Spark-TTS":
            url = f'http://{local_server_ip}:9883/spark/?text={text}'
            try:
                response = rq.get(url)
                wav_data = response.content
                with open(voice_path, 'wb') as f:
                    f.write(wav_data)
                play_voice()
            except Exception as e:
                notice(f"本地Spark-TTS整合包API服务器未开启，错误详情：{e}")
        elif tts_menu.get() == "本地Index-TTS":
            url = f'http://{local_server_ip}:9884/indextts/?text={text}'
            try:
                response = rq.get(url)
                wav_data = response.content
                with open(voice_path, 'wb') as f:
                    f.write(wav_data)
                play_voice()
            except Exception as e:
                notice(f"本地Index-TTS整合包API服务器未开启，错误详情：{e}")
        elif tts_menu.get() == "本地pyttsx3":
            try:
                engine.save_to_file(text, voice_path)
                engine.runAndWait()
                play_voice()
            except:
                notice("您的电脑暂不支持pyttsx3，可选择其他语音合成引擎")
    except:
        notice(f"{tts_menu.get()}服务拥挤，可选择其他语音合成引擎")

    def play_live2d():  # 读取缓存音频播放Live2D对口型动作
        try:
            x, sr = librosa.load(voice_path, sr=8000)
            x = x - min(x)
            x = x / max(x)
            x = np.log(x) + 1
            x = x / max(x) * 1.2
            s_time = time.time()
            for _ in range(int(len(x) / 800)):
                it = x[int((time.time() - s_time) * 8000) + 1]
                if it < 0:
                    it = 0
                with open("data/cache/cache.txt", "w") as cache_file:
                    cache_file.write(str(float(it)))
                time.sleep(0.1)
        except:
            pass
        time.sleep(0.1)
        with open("data/cache/cache.txt", "w") as cache_file:
            cache_file.write("0")

    Thread(target=play_live2d).start()
