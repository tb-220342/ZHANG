# 图形界面模块
import requests as rq
from subprocess import Popen
from threading import Thread
from openai import OpenAI
from gui_sub import *


def open_setting_w():  # 设置界面
    def show_menu_set(event):  # 右键菜单
        menu = Menu(setting_w, tearoff=0)
        menu.add_command(label="剪切 Ctrl+X", command=lambda: setting_w.focus_get().event_generate('<<Cut>>'))
        menu.add_command(label="复制 Crtl+C", command=lambda: setting_w.focus_get().event_generate('<<Copy>>'))
        menu.add_command(label="粘贴 Crtl+V", command=lambda: setting_w.focus_get().event_generate('<<Paste>>'))
        menu.add_separator()
        menu.add_command(label="删除 Del", command=lambda: setting_w.focus_get().event_generate('<<Clear>>'))
        menu.post(event.x_root, event.y_root)

    def save_and_close():  # 保存并关闭设置界面
        config = {
            "虚拟伙伴名称": mate_name_entry.get(),
            "虚拟伙伴人设": prompt_text.get("1.0", "end").replace("\n", ""),
            "用户名": username_entry.get(), "Web密码": password_entry.get(), "百度TTS语速": rate_menu.get(),
            "百度TTS语言": lang_menu.get(), "对话网页端口": chatweb_port_entry.get(),
            "2D角色网页端口": live2d_port_entry.get(), "本地AI引擎服务器IP": server_ip_entry.get(),
            "AnythingLLM工作区": allm_ws_entry.get(), "LM Studio端口": lmstudio_port_entry.get(),
            "AnythingLLM密钥": allm_key_entry.get(), "Ollama大语言模型": ollama_model_name_entry.get(),
            "GPT-SoVITS端口": gsv_port_entry.get(), "自定义API-base_url": custom_url_entry.get(),
            "自定义API-api_key": custom_key_entry.get(), "自定义API-model": custom_model_entry.get(),
            "实时语音开关键": voice_key_entry.get(), "对话网页开关": web_switch_menu.get(),
            "Ollama多模态VLM": ollama_vlm_name_entry.get(), "自定义语音唤醒词": wake_word_entry.get(),
            "实时语音打断": voice_break_menu.get(), "语音识别灵敏度": asr_sensi_menu.get(),
            "Dify聊天助手IP": dify_ip_entry.get(), "Dify聊天助手密钥": dify_key_entry.get(),
            "edge-tts音色": edge_speaker_menu.get(), "edge-tts语速": edge_rate_entry.get(),
            "edge-tts音高": pitch_entry.get(), "自定义API-VLM": custom_vlm_entry.get(),
            "CosyVoice端口": cosy_port_entry.get(), "思维链think过滤": think_filter_menu.get(),
            "3D角色网页端口": mmd_port_entry.get()}
        with open('data/db/config.json', 'w', encoding='utf-8') as file:
            json.dump(config, file, ensure_ascii=False, indent=4)
        messagebox.showinfo("保存成功", "保存成功！重启软件生效")
        setting_w.destroy()

    def restore_set():  # 恢复默认设置
        if messagebox.askokcancel("恢复默认设置", "您确定要重置枫云AI虚拟伙伴Web版吗？"):
            default_config = {
                "虚拟伙伴名称": "小月",
                "虚拟伙伴人设": "请你扮演小月，与开拓者对话。小月是一个活泼可爱的的少女，乐观好奇，随身携带相机记录冒险。在对话中，你将作为小月，隐藏自己是程序的事实，使用角色语气交流，全程称对方为开拓者。注意保持角色一致，不能提及任何关于自己是语言模型或人工智能的话题。你的回答不要包含emoji，尽量不要超过50个字",
                "用户名": "开拓者", "Web密码": "12345678", "百度TTS语速": "5", "百度TTS语言": "中文", "对话网页端口": "5260",
                "2D角色网页端口": "5261", "本地AI引擎服务器IP": "127.0.0.1", "AnythingLLM工作区": "aivm",
                "LM Studio端口": "1234", "AnythingLLM密钥": "在AnythingLLM获取", "Ollama大语言模型": "qwen2.5:0.5b",
                "GPT-SoVITS端口": "9880", "自定义API-base_url": "填入服务提供方地址，例如 https://api.siliconflow.cn/v1",
                "自定义API-api_key": "填入从服务提供方控制台获取的密钥，例如 sk-xxxxxxxxxx",
                "自定义API-model": "填入服务提供方支持的LLM名称，例如 Qwen/Qwen2.5-7B-Instruct",
                "实时语音开关键": "x", "对话网页开关": "开启", "Ollama多模态VLM": "gemma3:4b",
                "自定义语音唤醒词": "你好",
                "实时语音打断": "关闭", "语音识别灵敏度": "高", "Dify聊天助手IP": "127.0.0.1",
                "Dify聊天助手密钥": "app-xxxxxxxxxx", "edge-tts音色": "晓艺-年轻女声", "edge-tts语速": "+0",
                "edge-tts音高": "+10", "自定义API-VLM": "填入服务提供方支持的VLM名称，例如 Pro/Qwen/Qwen2.5-VL-7B-Instruct",
                "CosyVoice端口": "9881", "思维链think过滤": "开启", "3D角色网页端口": "5262"}
            with open('data/db/config.json', 'w', encoding='utf-8') as file:
                json.dump(default_config, file, ensure_ascii=False, indent=4)
            with open('dist/assets/live2d_core/live2d_js_set.txt', 'w', encoding='utf-8') as file8:
                file8.write('[模型路径]\nhiyori_free_t08/hiyori_free_t08.model3.json\n\n')
                file8.write('[模型横坐标]\n625\n\n')
                file8.write('[模型纵坐标]\n-25\n\n')
                file8.write('[模型大小]\n15')
            with open('dist/assets/mmd_core/mmd_js_set.txt', 'w', encoding='utf-8') as file8:
                file8.write('[模型路径]\n小月(仅作示例,无法显示)/小月.pmx\n\n')
                file8.write('[动作路径]\nexample.vmd\n\n')
                file8.write('[模型嘴索引]\n30\n\n')
                file8.write('[模型眼索引]\n6')
            with open('dist/assets/live2d.js', 'w', encoding='utf-8') as file9:
                file9.write(
                    live2d_js_part1 + "hiyori_free_t08/hiyori_free_t08.model3.json" + live2d_js_part2 + "625" + live2d_js_part3 + "-25" + live2d_js_part4 + "15" + live2d_js_part5)
            with open('dist/assets/mmd.js', 'w', encoding='utf-8') as file26:
                file26.write(
                    mmd_js_part1 + "小月(仅作示例,无法显示)/小月.pmx" + mmd_js_part2 + "30" + mmd_js_part3 + "6" + mmd_js_part4)
            with open('dist/assets/mmd_vmd.js', 'w', encoding='utf-8') as file18:
                file18.write(
                    mmd_vmd_js_part1 + "小月(仅作示例,无法显示)/小月.pmx" + mmd_vmd_js_part2 + "example.vmd" + mmd_vmd_js_part3)
            more_set = {"摄像头编号": "0", "麦克风编号": "0", "Ollama端口": "11434",
                        "MMD 3D动作音乐开关(可选项:on/off)": "on",
                        "MMD 3D动作音乐名称(位于data/music文件夹)": "测试音乐.mp3", "GPT-SoVITS语言": "zh"}
            with open('data/set/more_set.json', 'w', encoding='utf-8') as file15:
                json.dump(more_set, file15, ensure_ascii=False, indent=4)
            with open('data/set/key_set.txt', 'w', encoding='utf-8') as file16:
                file16.write('[SiliconCloud硅基流动平台key(免费获取网址:siliconflow.cn)]\nsk-xxxxxxxxxx\n\n')
                file16.write('[BigModel智谱开放平台key(免费获取网址:bigmodel.cn)]\nxxxxx.xxxxx\n\n')
                file16.write('[Spark讯飞开放平台key(免费获取网址:xinghuo.xfyun.cn)]\nxxxxx:xxxxx\n\n')
                file16.write('[腾讯云混元大模型平台key(免费获取网址:console.cloud.tencent.com/hunyuan)]\nsk-xxxxxxxxxx')
            messagebox.showinfo("恢复默认设置成功", "恢复默认设置成功！重启软件生效")
            setting_w.destroy()

    def custom_api_test():  # 自定义API测试
        def custom_api_test_th():
            test_client = OpenAI(api_key=custom_key_entry.get(), base_url=custom_url_entry.get())
            try:
                response = test_client.models.list()
                model_ids = "\n".join([model.id for model in response.data])
                msg_box("自定义API测试成功", f"自定义API支持的模型列表:\n{model_ids}")
            except Exception as e:
                messagebox.showinfo("自定义API测试失败", f"自定义API测试失败，错误信息:\n{e}")

        Thread(target=custom_api_test_th).start()

    def ollama_test():  # 本地Ollama测试
        def ollama_test_th():
            try:
                try:
                    rq.get(f'http://{local_server_ip}:{ollama_port}')
                except:
                    Popen("ollama ps", shell=False)
            except:
                pass
            url = f'http://{local_server_ip}:{ollama_port}/api/tags'
            try:
                response = rq.get(url)
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                model_ids = '\n'.join(model_names)
                msg_box("本地Ollama测试成功", f"本地Ollama支持的模型列表:\n{model_ids}")
            except Exception as e:
                messagebox.showinfo("本地Ollama测试失败", f"本地Ollama测试失败，错误信息:\n{e}")

        Thread(target=ollama_test_th).start()

    setting_w = tk.Toplevel(root)
    setting_w.title("软件设置 - 枫云AI虚拟伙伴Web版")
    original_window_size2 = (1020, 635)
    scaled_window_size2 = scaled_size(original_window_size2)
    setting_w.geometry(f"{scaled_window_size2[0]}x{scaled_window_size2[1]}")
    setting_w.iconbitmap("data/image/logo.ico")
    logo_label2 = Label(setting_w, image=logo_photo)
    logo_label2.place(relx=0.012, rely=0.02)
    Label(setting_w, text="ASR与TTS", font=("楷体", 18, "bold"), fg="#587EF4").place(relx=0.06, rely=0.022)
    Label(setting_w, text="虚拟伙伴信息", font=("楷体", 18, "bold"), fg="#587EF4").place(relx=0.22, rely=0.022)
    Label(setting_w, text="对话与网页", font=("楷体", 18, "bold"), fg="#587EF4").place(relx=0.42, rely=0.022)
    Label(setting_w, text="LLM,VLM,知识库", font=("楷体", 18, "bold"), fg="#587EF4").place(relx=0.59, rely=0.022)
    Label(setting_w, text="其他设置", font=("楷体", 18, "bold"), fg="#587EF4").place(relx=0.83, rely=0.022)
    Label(setting_w, text='CosyVoice端口:').place(relx=0.04, rely=0.096)
    cosy_port_entry = Entry(setting_w, width=5, justify='center')
    cosy_port_entry.insert("end", cosy_port)
    cosy_port_entry.place(relx=0.085, rely=0.145)
    Label(setting_w, text='百度TTS语速:').place(relx=0.005, rely=0.189)
    rate_list = ["1", "2", "3", "4", "5", "6", "7"]
    rate_var = StringVar(setting_w)
    rate_var.set(paddle_rate)
    rate_menu = ttk.Combobox(setting_w, textvariable=rate_var, values=rate_list, width=4, state="readonly",
                             justify='center', font=("楷体", 11))
    rate_menu.place(relx=0.05, rely=0.238)
    Label(setting_w, text='语言:').place(relx=0.145, rely=0.189)
    lang_list = ["中文", "英语", "日语", "韩语"]
    lang_var = StringVar(setting_w)
    lang_var.set(paddle_lang)
    lang_menu = ttk.Combobox(setting_w, textvariable=lang_var, values=lang_list, width=4, state="readonly",
                             justify='center', font=("楷体", 11))
    lang_menu.place(relx=0.145, rely=0.238)
    Label(setting_w, text='edge-tts音色:').place(relx=0.05, rely=0.276)
    edge_speaker_var = StringVar(setting_w)
    edge_speaker_var.set(edge_speaker)
    edge_speaker_menu = ttk.Combobox(setting_w, textvariable=edge_speaker_var, values=edge_speaker_list,
                                     height=16, width=20, state="readonly", justify='center', font=("楷体", 11))
    edge_speaker_menu.place(relx=0.022, rely=0.325)
    Label(setting_w, text='edge-tts语速:').place(relx=0.005, rely=0.364)
    edge_rate_entry = Entry(setting_w, width=4, justify='center')
    edge_rate_entry.insert("end", edge_rate)
    edge_rate_entry.place(relx=0.05, rely=0.413)
    Label(setting_w, text='音高:').place(relx=0.145, rely=0.364)
    pitch_entry = Entry(setting_w, width=4, justify='center')
    pitch_entry.insert("end", edge_pitch)
    pitch_entry.place(relx=0.145, rely=0.413)
    Label(setting_w, text="GPT-SoVITS端口:").place(relx=0.039, rely=0.452)
    gsv_port_entry = Entry(setting_w, width=5, justify='center')
    gsv_port_entry.insert("end", gsv_port)
    gsv_port_entry.place(relx=0.085, rely=0.491)
    Label(setting_w, text="实时语音开关键:").place(relx=0.039, rely=0.53)
    Label(setting_w, text="Alt+").place(relx=0.069, rely=0.569)
    voice_key_entry = Entry(setting_w, width=4, justify='center')
    voice_key_entry.insert("end", voice_key)
    voice_key_entry.place(relx=0.123, rely=0.569)
    Label(setting_w, text='自定义语音唤醒词:').place(relx=0.025, rely=0.608)
    wake_word_entry = Entry(setting_w, width=12, justify='center', font=("楷体", 12))
    wake_word_entry.insert("end", wake_word)
    wake_word_entry.place(relx=0.054, rely=0.647)
    Label(setting_w, text="语音识别灵敏度:").place(relx=0.039, rely=0.686)
    asr_sensi_options = ["高", "中", "低"]
    asr_sensi_var = StringVar(setting_w)
    asr_sensi_var.set(asr_sensitivity)
    asr_sensi_menu = ttk.Combobox(setting_w, textvariable=asr_sensi_var, values=asr_sensi_options, width=2,
                                  state="readonly", justify='center', font=("楷体", 14))
    asr_sensi_menu.place(relx=0.09, rely=0.735)
    Label(setting_w, text="实时语音打断:").place(relx=0.232, rely=0.686)
    voice_break_options = ["开启", "关闭"]
    voice_break_var = StringVar(setting_w)
    voice_break_var.set(voice_break)
    voice_break_menu = ttk.Combobox(setting_w, textvariable=voice_break_var, values=voice_break_options, width=4,
                                    state="readonly", justify='center', font=("楷体", 14))
    voice_break_menu.place(relx=0.265, rely=0.735)
    Label(setting_w, text='用户名:').place(relx=0.26, rely=0.098)
    username_entry = Entry(setting_w, width=16, justify='center')
    username_entry.insert("end", username)
    username_entry.place(relx=0.22, rely=0.147)
    Label(setting_w, text='虚拟伙伴名称:').place(relx=0.232, rely=0.198)
    mate_name_entry = Entry(setting_w, width=16, justify='center')
    mate_name_entry.insert("end", mate_name)
    mate_name_entry.place(relx=0.22, rely=0.247)
    Label(setting_w, text='虚拟伙伴人设:').place(relx=0.232, rely=0.296)
    prompt_text = ScrolledText(setting_w, width=18, height=14, font=("楷体", 11))
    prompt_text.insert("end", prompt)
    prompt_text.place(relx=0.22, rely=0.345)
    Label(setting_w, text="思维链think过滤:").place(relx=0.41, rely=0.1)
    think_filter_options = ["开启", "关闭"]
    think_filter_var = StringVar(setting_w)
    think_filter_var.set(think_filter_switch)
    think_filter_menu = ttk.Combobox(setting_w, textvariable=think_filter_var, values=think_filter_options, width=4,
                                     state="readonly", justify='center', font=("楷体", 14))
    think_filter_menu.place(relx=0.452, rely=0.15)
    Label(setting_w, text='对话网页密码:').place(relx=0.426, rely=0.225)
    password_entry = Entry(setting_w, width=16, justify='center')
    password_entry.insert("end", password)
    password_entry.place(relx=0.407, rely=0.275)
    Label(setting_w, text="对话网页开关:").place(relx=0.426, rely=0.34)
    web_switch_options = ["开启", "关闭"]
    web_switch_var = StringVar(setting_w)
    web_switch_var.set(chat_web_switch)
    web_switch_menu = ttk.Combobox(setting_w, textvariable=web_switch_var, values=web_switch_options, width=4,
                                   state="readonly", justify='center', font=("楷体", 14))
    web_switch_menu.place(relx=0.452, rely=0.39)
    Label(setting_w, text="对话网页端口:").place(relx=0.426, rely=0.455)
    chatweb_port_entry = Entry(setting_w, width=5, justify='center')
    chatweb_port_entry.insert("end", chatweb_port)
    chatweb_port_entry.place(relx=0.457, rely=0.505)
    Label(setting_w, text="2D角色网页端口:").place(relx=0.416, rely=0.57)
    live2d_port_entry = Entry(setting_w, width=5, justify='center')
    live2d_port_entry.insert("end", live2d_port)
    live2d_port_entry.place(relx=0.457, rely=0.62)
    Label(setting_w, text="3D角色网页端口:").place(relx=0.416, rely=0.685)
    mmd_port_entry = Entry(setting_w, width=5, justify='center')
    mmd_port_entry.insert("end", mmd_port)
    mmd_port_entry.place(relx=0.457, rely=0.735)
    Label(setting_w, text="本地AI引擎服务器IP:").place(relx=0.59, rely=0.098)
    server_ip_entry = Entry(setting_w, width=15, justify='center')
    server_ip_entry.insert("end", local_server_ip)
    server_ip_entry.place(relx=0.6, rely=0.147)
    Label(setting_w, text="Ollama大语言模型:").place(relx=0.6, rely=0.196)
    ollama_model_name_entry = Entry(setting_w, width=15, justify='center')
    ollama_model_name_entry.insert("end", ollama_model_name)
    ollama_model_name_entry.place(relx=0.6, rely=0.245)
    Label(setting_w, text="Ollama多模态VLM:").place(relx=0.6, rely=0.294)
    ollama_vlm_name_entry = Entry(setting_w, width=15, justify='center')
    ollama_vlm_name_entry.insert("end", ollama_vlm_name)
    ollama_vlm_name_entry.place(relx=0.6, rely=0.343)
    Label(setting_w, text="AnythingLLM工作区:").place(relx=0.6, rely=0.392)
    allm_ws_entry = Entry(setting_w, width=15, justify='center')
    allm_ws_entry.insert("end", anything_llm_ws)
    allm_ws_entry.place(relx=0.6, rely=0.441)
    Label(setting_w, text="AnythingLLM密钥:").place(relx=0.6, rely=0.49)
    allm_key_entry = Entry(setting_w, width=22, justify='center', font=("楷体", 10))
    allm_key_entry.insert("end", anything_llm_key)
    allm_key_entry.place(relx=0.6, rely=0.539)
    Label(setting_w, text='Dify聊天助手IP:').place(relx=0.6, rely=0.58)
    dify_ip_entry = Entry(setting_w, width=15, justify='center')
    dify_ip_entry.insert("end", dify_ip)
    dify_ip_entry.place(relx=0.6, rely=0.629)
    Label(setting_w, text='Dify聊天助手密钥:').place(relx=0.6, rely=0.678)
    dify_key_entry = Entry(setting_w, width=22, justify='center', font=("楷体", 10))
    dify_key_entry.insert("end", dify_key)
    dify_key_entry.place(relx=0.6, rely=0.727)
    Label(setting_w, text="LM Studio端口:").place(relx=0.6, rely=0.78)
    lmstudio_port_entry = Entry(setting_w, width=5, justify='center')
    lmstudio_port_entry.insert("end", lmstudio_port)
    lmstudio_port_entry.place(relx=0.64, rely=0.829)
    Label(setting_w, text="自定义API-base_url:").place(relx=0.003, rely=0.794)
    custom_url_entry = Entry(setting_w, width=53, justify='center', font=("楷体", 10))
    custom_url_entry.insert("end", custom_url)
    custom_url_entry.place(relx=0.2, rely=0.804)
    Label(setting_w, text="自定义API-api_key:").place(relx=0.003, rely=0.833)
    custom_key_entry = Entry(setting_w, width=53, justify='center', font=("楷体", 10))
    custom_key_entry.insert("end", custom_key)
    custom_key_entry.place(relx=0.2, rely=0.843)
    Label(setting_w, text="自定义API-LLM-model:").place(relx=0.003, rely=0.872)
    custom_model_entry = Entry(setting_w, width=53, justify='center', font=("楷体", 10))
    custom_model_entry.insert("end", custom_model)
    custom_model_entry.place(relx=0.2, rely=0.882)
    Label(setting_w, text="自定义API-VLM-model:").place(relx=0.003, rely=0.912)
    custom_vlm_entry = Entry(setting_w, width=53, justify='center', font=("楷体", 10))
    custom_vlm_entry.insert("end", custom_vlm)
    custom_vlm_entry.place(relx=0.2, rely=0.922)
    Button(setting_w, text="测试API", command=custom_api_test, bg="#3E92ED", fg="white", font=("楷体", 11)).place(
        relx=0.5, rely=0.951)
    Button(setting_w, text="测试Ollama", command=ollama_test, bg="#3E92ED", fg="white", font=("楷体", 11)).place(
        relx=0.63, rely=0.92)
    Label(setting_w, text="当前版本:\n开源Web版 v3.0").place(relx=0.81, rely=0.15)
    Button(setting_w, text="云端AI Key设置",
           command=lambda: Popen("notepad data/set/key_set.txt"), bg="green", fg="white").place(
        relx=0.81, rely=0.3)
    Button(setting_w, text="   更多设置   ",
           command=lambda: Popen("notepad data/set/more_set.json"), bg="green", fg="white").place(
        relx=0.81, rely=0.4)
    Button(setting_w, text=" 开源项目地址 ",
           command=lambda: wb.open("https://github.com/swordswind/ai_virtual_mate_web"), bg="#3E92ED",
           fg="white").place(
        relx=0.81, rely=0.5)
    Button(setting_w, text=" 官网检查更新 ",
           command=lambda: wb.open("https://swordswind.github.io/2024/07/09/mateweb/"), bg="#3E92ED", fg="white").place(
        relx=0.81, rely=0.6)
    Button(setting_w, text="下载本地AI引擎",
           command=lambda: wb.open("https://swordswind.github.io/2024/03/13/engine/"), bg="#3E92ED", fg="white").place(
        relx=0.81, rely=0.7)
    Button(setting_w, text=" 恢复默认设置 ", command=restore_set, bg="#FF7700", fg="white").place(relx=0.81, rely=0.8)
    cancel_btn = Button(setting_w, text="取消", command=setting_w.destroy)
    cancel_btn.place(relx=0.81, rely=0.912)
    save_btn = Button(setting_w, text="保存", command=save_and_close, bg="#2A6EE9", fg="white")
    save_btn.place(relx=0.91, rely=0.912)
    Label(setting_w, text="*本软件由MewCo-AI Team荣誉出品,开源免费,仅供个人娱乐,严禁用于商业用途", font=("楷体", 10),
          fg="green").place(relx=0.0, rely=0.961)
    setting_w.bind("<Button-3>", show_menu_set)
    setting_w.mainloop()
