# 系统初始化模块
import json
import socket
import shutil
from tkinter import filedialog as fd, messagebox

with open('data/db/config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
mate_name = config["虚拟伙伴名称"]
prompt = config["虚拟伙伴人设"]
username = config["用户名"]
password = config["Web密码"]
paddle_rate = config["百度TTS语速"]
paddle_lang = config["百度TTS语言"]
chatweb_port = config["对话网页端口"]
live2d_port = config["2D角色网页端口"]
local_server_ip = config["本地AI引擎服务器IP"]
anything_llm_ws = config["AnythingLLM工作区"]
lmstudio_port = config["LM Studio端口"]
anything_llm_key = config["AnythingLLM密钥"]
ollama_model_name = config["Ollama大语言模型"]
gsv_port = config["GPT-SoVITS端口"]
custom_url = config["自定义API-base_url"]
custom_key = config["自定义API-api_key"]
custom_model = config["自定义API-model"]
voice_key = config["实时语音开关键"]
chat_web_switch = config["对话网页开关"]
ollama_vlm_name = config["Ollama多模态VLM"]
wake_word = config["自定义语音唤醒词"]
voice_break = config["实时语音打断"]
asr_sensitivity = config["语音识别灵敏度"]
dify_ip = config["Dify聊天助手IP"]
dify_key = config["Dify聊天助手密钥"]
edge_speaker = config["edge-tts音色"]
edge_rate = config["edge-tts语速"]
edge_pitch = config["edge-tts音高"]
custom_vlm = config["自定义API-VLM"]
cosy_port = config["CosyVoice端口"]
think_filter_switch = config["思维链think过滤"]
mmd_port = config["3D角色网页端口"]
with open('data/db/preference.json', 'r', encoding='utf-8') as file2:
    preference = json.load(file2)
voice_switch = preference["语音识别模式"]
prefer_llm = preference["对话语言模型"]
prefer_tts = preference["语音合成引擎"]
prefer_img = preference["图像识别引擎"]
with open('data/db/history.db', 'r', encoding='utf-8') as file3:
    history = file3.read()
with open('dist/assets/live2d_core/live2d_js_part1', 'r', encoding='utf-8') as file10:
    live2d_js_part1 = file10.read()
with open('dist/assets/live2d_core/live2d_js_part2', 'r', encoding='utf-8') as file11:
    live2d_js_part2 = file11.read()
with open('dist/assets/live2d_core/live2d_js_part3', 'r', encoding='utf-8') as file12:
    live2d_js_part3 = file12.read()
with open('dist/assets/live2d_core/live2d_js_part4', 'r', encoding='utf-8') as file13:
    live2d_js_part4 = file13.read()
with open('dist/assets/live2d_core/live2d_js_part5', 'r', encoding='utf-8') as file14:
    live2d_js_part5 = file14.read()
with open('data/set/more_set.json', 'r', encoding='utf-8') as file15:
    more_set = json.load(file15)
cam_num = int(more_set["摄像头编号"])
mic_num = int(more_set["麦克风编号"])
ollama_port = more_set["Ollama端口"]
vmd_music_switch = more_set["MMD 3D动作音乐开关(可选项:on/off)"]
vmd_music_name = more_set["MMD 3D动作音乐名称(位于data/music文件夹)"]
gsv_lang = more_set["GPT-SoVITS语言"]
with open('data/set/key_set.txt', 'r', encoding='utf-8') as file16:
    lines16 = file16.readlines()
sf_key = lines16[1].strip()
glm_key = lines16[4].strip()
spark_key = lines16[7].strip()
hy_key = lines16[10].strip()
with open('dist/assets/mmd_core/mmd_js_part1', 'r', encoding='utf-8') as file19:
    mmd_js_part1 = file19.read()
with open('dist/assets/mmd_core/mmd_js_part2', 'r', encoding='utf-8') as file20:
    mmd_js_part2 = file20.read()
with open('dist/assets/mmd_core/mmd_js_part3', 'r', encoding='utf-8') as file21:
    mmd_js_part3 = file21.read()
with open('dist/assets/mmd_core/mmd_js_part4', 'r', encoding='utf-8') as file22:
    mmd_js_part4 = file22.read()
with open('dist/assets/mmd_core/mmd_vmd_js_part1', 'r', encoding='utf-8') as file23:
    mmd_vmd_js_part1 = file23.read()
with open('dist/assets/mmd_core/mmd_vmd_js_part2', 'r', encoding='utf-8') as file24:
    mmd_vmd_js_part2 = file24.read()
with open('dist/assets/mmd_core/mmd_vmd_js_part3', 'r', encoding='utf-8') as file25:
    mmd_vmd_js_part3 = file25.read()


def get_local_ip():  # 获取本机局域网IP地址
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('223.5.5.5', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    return ip


def upload_image():  # 上传图片
    file_path = fd.askopenfilename(title="选择一张JPG图片", filetypes=[("JPG文件", "*.jpg")])
    if file_path:
        target_path = "dist/assets/image/bg.jpg"
        shutil.copy(file_path, target_path)
        messagebox.showinfo("提示", "更换网页背景成功,请刷新网页")


server_ip = get_local_ip()
edge_speaker_list = ["晓艺-年轻女声", "晓晓-成稳女声", "云健-大型纪录片男声", "云希-短视频热门男声",
                     "云夏-年轻男声", "云扬-成稳男声", "晓北-辽宁话女声", "晓妮-陕西话女声", "晓佳-粤语成稳女声",
                     "晓满-粤语年轻女声", "云龙-粤语男声", "晓辰-台湾话年轻女声", "晓宇-台湾话成稳女声",
                     "云哲-台湾话男声", "佳太-日语男声", "七海-日语女声"]
