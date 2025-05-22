# 图形界面子模块
import os
import ctypes
import tkinter as tk
import webbrowser as wb
from tkinter import ttk, Label, Text, StringVar, Menu, Button, Entry
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from system_init import *

scaling_factor = 1


def msg_box(title, msg):  # 消息框
    global msg_w
    msg_w = tk.Toplevel(root)
    msg_w.geometry("640x480")
    msg_w.iconbitmap("data/image/logo.ico")
    msg_w.attributes("-topmost", 1)
    msg_w.title(title)
    msg_text = ScrolledText(msg_w)
    msg_text.insert("end", msg)
    msg_text.configure(state="disabled")
    msg_text.pack()
    msg_w.bind("<Button-3>", show_menu_msg)


def show_menu_msg(event):  # 右键菜单
    menu = Menu(msg_w, tearoff=0)
    menu.add_command(label="📄复制 Crtl+C", command=lambda: msg_w.focus_get().event_generate('<<Copy>>'))
    menu.post(event.x_root, event.y_root)


def show_menu(event):  # 右键菜单
    menu = Menu(root, tearoff=0)
    menu.add_command(label="✂剪切 Ctrl+X", command=lambda: root.focus_get().event_generate('<<Cut>>'))
    menu.add_command(label="📄复制 Crtl+C", command=lambda: root.focus_get().event_generate('<<Copy>>'))
    menu.add_command(label="📋粘贴 Crtl+V", command=lambda: root.focus_get().event_generate('<<Paste>>'))
    menu.add_separator()
    menu.add_command(label="🗑删除 Del", command=lambda: root.focus_get().event_generate('<<Clear>>'))
    menu.post(event.x_root, event.y_root)


def get_dpi():  # 获取DPI
    try:
        hDC = ctypes.windll.user32.GetDC(0)
        dpi = ctypes.windll.gdi32.GetDeviceCaps(hDC, 88)
        ctypes.windll.user32.ReleaseDC(0, hDC)
        return dpi
    except:
        return 96


def scaled_size(original_size):  # 计算适配的窗口大小
    global scaling_factor
    dpi = get_dpi()
    scaling_factor = dpi / 96
    return int(original_size[0] * scaling_factor), int(original_size[1] * scaling_factor)


def open_live2d_set_w():  # Live2D设置窗口
    def read_settings():  # 读取设置
        settings = {}
        with open('dist/assets/live2d_core/live2d_js_set.txt', 'r', encoding='utf-8') as file8:
            lines8 = file8.readlines()
            current_key = None
            for line in lines8:
                line = line.strip()
                if line.startswith('[') and line.endswith(']'):
                    current_key = line[1:-1].strip()
                elif current_key:
                    settings[current_key] = line
                    current_key = None
        return settings

    def save_settings(settings):  # 保存设置
        entry_model_path2 = live2d_menu.get().replace('\\', '/')
        with open('dist/assets/live2d_core/live2d_js_set.txt', 'w', encoding='utf-8') as file8:
            for key, value in settings.items():
                file8.write(f'[{key}]\n{value}\n\n')
        with open('dist/assets/live2d.js', 'w', encoding='utf-8') as file9:
            file9.write(
                live2d_js_part1 + entry_model_path2 + live2d_js_part2 + entry_model_x.get() + live2d_js_part3 + entry_model_y.get() + live2d_js_part4 + entry_model_size.get() + live2d_js_part5)

    def on_save():  # 保存设置
        entry_model_path2 = live2d_menu.get().replace('\\', '/')
        settings = {"模型路径": entry_model_path2, "模型横坐标": entry_model_x.get(),
                    "模型纵坐标": entry_model_y.get(), "模型大小": entry_model_size.get()}
        save_settings(settings)
        messagebox.showinfo("保存成功", "Live2D设置已保存！\n刷新2D角色网页生效")

    def find_model3_json_files():
        live2d_folder = 'dist/assets/live2d_model'
        model3_files = []
        for root2, dirs, files in os.walk(live2d_folder):
            for f in files:
                if f.endswith('.model3.json'):
                    relative_path = os.path.relpath(os.path.join(root2, f), live2d_folder)
                    model3_files.append(relative_path)
        return model3_files

    def load_settings():
        settings = read_settings()
        live2d_var.set(settings.get("模型路径", ""))
        entry_model_x.insert(0, settings.get("模型横坐标", ""))
        entry_model_y.insert(0, settings.get("模型纵坐标", ""))
        entry_model_size.insert(0, settings.get("模型大小", ""))

    live2d_set_w = tk.Toplevel(root)
    live2d_set_w.title("Live2D设置 - 枫云AI虚拟伙伴Web版")
    original_window_size4 = (413, 310)
    scaled_window_size4 = scaled_size(original_window_size4)
    live2d_set_w.geometry(f"{scaled_window_size4[0]}x{scaled_window_size4[1]}")
    Label(live2d_set_w, text="Live2D设置", font=("楷体", 18, "bold"), fg="#587EF4").pack(pady=10)
    Label(live2d_set_w, text="模型路径:").pack()
    model3_options = find_model3_json_files()
    live2d_var = StringVar(root)
    live2d_menu = ttk.Combobox(live2d_set_w, textvariable=live2d_var, values=model3_options, state="readonly",
                               justify='center', width=43, font=("楷体", 13))
    live2d_menu.pack()
    Label(live2d_set_w, text="模型横坐标:").pack()
    entry_model_x = Entry(live2d_set_w, width=5)
    entry_model_x.pack()
    Label(live2d_set_w, text="模型纵坐标:").pack()
    entry_model_y = Entry(live2d_set_w, width=5)
    entry_model_y.pack()
    Label(live2d_set_w, text="模型大小:").pack()
    entry_model_size = Entry(live2d_set_w, width=2)
    entry_model_size.pack()
    button_frame = tk.Frame(live2d_set_w)
    button_frame.pack(pady=10)
    Button(button_frame, text="取消", command=live2d_set_w.destroy).pack(side='left', padx=5)
    Button(button_frame, text="保存", command=on_save, bg="#2A6EE9", fg="white").pack(side='left', padx=5)
    load_settings()
    live2d_set_w.mainloop()


def open_mmd_set_w():  # MMD设置窗口
    def read_settings():  # 读取设置
        settings = {}
        with open('dist/assets/mmd_core/mmd_js_set.txt', 'r', encoding='utf-8') as file17:
            lines17 = file17.readlines()
            current_key = None
            for line in lines17:
                line = line.strip()
                if line.startswith('[') and line.endswith(']'):
                    current_key = line[1:-1].strip()
                elif current_key:
                    settings[current_key] = line
                    current_key = None
        return settings

    def save_settings(settings):  # 保存设置
        entry_model_path2 = mmd_menu.get().replace('\\', '/')
        with open('dist/assets/mmd_core/mmd_js_set.txt', 'w', encoding='utf-8') as file17:
            for key, value in settings.items():
                file17.write(f'[{key}]\n{value}\n\n')
        with open('dist/assets/mmd.js', 'w', encoding='utf-8') as file26:
            file26.write(mmd_js_part1 + entry_model_path2 + mmd_js_part2 + entry_mouth_index.get() + mmd_js_part3 + entry_eye_index.get() + mmd_js_part4)
        with open('dist/assets/mmd_vmd.js', 'w', encoding='utf-8') as file18:
            file18.write(mmd_vmd_js_part1 + entry_model_path2 + mmd_vmd_js_part2 + vmd_menu.get() + mmd_vmd_js_part3)

    def on_save():  # 保存设置
        entry_model_path2 = mmd_menu.get().replace('\\', '/')
        settings = {"模型路径": entry_model_path2, "动作路径": vmd_menu.get(),
                    "模型嘴索引": entry_mouth_index.get(), "模型眼索引": entry_eye_index.get()}
        save_settings(settings)
        messagebox.showinfo("保存成功", "MMD 3D设置已保存！\n刷新3D角色网页生效")

    def find_pmx_files():
        mmd_folder = 'dist/assets/mmd_model'
        pmx_files = []
        for root2, dirs, files in os.walk(mmd_folder):
            for f in files:
                if f.endswith('.pmx'):
                    relative_path = os.path.relpath(os.path.join(root2, f), mmd_folder)
                    pmx_files.append(relative_path)
        return pmx_files

    def find_vmd_files():
        vmd_folder = 'dist/assets/mmd_action'
        vmd_files = []
        for root2, dirs, files in os.walk(vmd_folder):
            for f in files:
                if f.endswith('.vmd'):
                    relative_path = os.path.relpath(os.path.join(root2, f), vmd_folder)
                    vmd_files.append(relative_path)
        return vmd_files

    def load_settings():
        settings = read_settings()
        mmd_var.set(settings.get("模型路径", ""))
        vmd_var.set(settings.get("动作路径", ""))
        entry_mouth_index.insert(0, settings.get("模型嘴索引", ""))
        entry_eye_index.insert(0, settings.get("模型眼索引", ""))

    mmd_set_w = tk.Toplevel(root)
    mmd_set_w.title("MMD 3D设置 - 枫云AI虚拟伙伴Web版")
    original_window_size4 = (413, 310)
    scaled_window_size4 = scaled_size(original_window_size4)
    mmd_set_w.geometry(f"{scaled_window_size4[0]}x{scaled_window_size4[1]}")
    Label(mmd_set_w, text="MMD 3D设置", font=("楷体", 18, "bold"), fg="#587EF4").pack(pady=10)
    Label(mmd_set_w, text="模型路径:").pack()
    pmx_options = find_pmx_files()
    mmd_var = StringVar(root)
    mmd_menu = ttk.Combobox(mmd_set_w, textvariable=mmd_var, values=pmx_options, state="readonly",
                            justify='center', width=43, font=("楷体", 13))
    mmd_menu.pack()
    Label(mmd_set_w, text="动作路径:").pack()
    vmd_options = find_vmd_files()
    vmd_var = StringVar(root)
    vmd_menu = ttk.Combobox(mmd_set_w, textvariable=vmd_var, values=vmd_options, state="readonly",
                            justify='center', width=43, font=("楷体", 13))
    vmd_menu.pack()
    Label(mmd_set_w, text="模型嘴索引:").pack()
    entry_mouth_index = Entry(mmd_set_w, width=4)
    entry_mouth_index.pack()
    Label(mmd_set_w, text="模型眼索引:").pack()
    entry_eye_index = Entry(mmd_set_w, width=4)
    entry_eye_index.pack()
    button_frame = tk.Frame(mmd_set_w)
    button_frame.pack(pady=10)
    Button(button_frame, text="取消", command=mmd_set_w.destroy).pack(side='left', padx=5)
    Button(button_frame, text="保存", command=on_save, bg="#2A6EE9", fg="white").pack(side='left', padx=5)
    load_settings()
    mmd_set_w.mainloop()


def open_change_w():  # 资源管理窗口
    change_w = tk.Toplevel(root)
    change_w.title("资源管理 - 枫云AI虚拟伙伴Web版")
    original_window_size3 = (750, 375)
    scaled_window_size3 = scaled_size(original_window_size3)
    change_w.geometry(f"{scaled_window_size3[0]}x{scaled_window_size3[1]}")
    change_w.iconbitmap("data/image/logo.ico")
    Label(change_w, text="更换Live2D模型", font=("楷体", 18, "bold"), fg="#587EF4").place(relx=0.0375, rely=0.0367)
    Label(change_w, text='第1步:\n推荐从模之屋下载模型\n格式选择Live2D', font=("楷体", 12)).place(relx=0.0125,
                                                                                                  rely=0.1667)
    Button(change_w, text="下载", command=lambda: wb.open("https://www.aplaybox.com/model/model"), bg="#3E92ED",
           fg="white").place(relx=0.245, rely=0.2)
    Label(change_w, text='第2步:\n打开模型文件夹,\n放入下载解压好的模型', font=("楷体", 12)).place(relx=0.0125,
                                                                                                   rely=0.45)
    Button(change_w, text="打开", command=lambda: os.startfile("dist\\assets\\live2d_model"), bg="#3E92ED",
           fg="white").place(relx=0.245, rely=0.5)
    Label(change_w, text='第3步:\n点击配置按钮\n进行路径和参数设置', font=("楷体", 12)).place(relx=0.0225, rely=0.75)
    Button(change_w, text="配置", command=open_live2d_set_w, bg="#3E92ED", fg="white").place(relx=0.245, rely=0.8)
    Label(change_w, text="更换MMD 3D模型", font=("楷体", 18, "bold"), fg="#587EF4").place(relx=0.35, rely=0.0367)
    Label(change_w, text='第1步:\n推荐从模之屋下载模型,动作\n模型格式选MMD,类型选人物\n动作类型选人物动作',
          font=("楷体", 12)).place(relx=0.3325,
                                   rely=0.15)
    Button(change_w, text="模型", command=lambda: wb.open("https://www.aplaybox.com/model/model"), bg="#3E92ED",
           fg="white").place(relx=0.615, rely=0.15)
    Button(change_w, text="动作", command=lambda: wb.open("https://www.aplaybox.com/model/action"), bg="#3E92ED",
           fg="white").place(relx=0.615, rely=0.25)
    Label(change_w, text='第2步:\n打开模型文件夹,\n放入下载解压好的模型', font=("楷体", 12)).place(relx=0.3625,
                                                                                                   rely=0.37)
    Button(change_w, text="打开", command=lambda: os.startfile("dist\\assets\\mmd_model"), bg="#3E92ED",
           fg="white").place(relx=0.615, rely=0.42)
    Label(change_w, text='第3步:\n打开动作文件夹,\n放入下载解压好的动作', font=("楷体", 12)).place(relx=0.3625,
                                                                                                   rely=0.57)
    Button(change_w, text="打开", command=lambda: os.startfile("dist\\assets\\mmd_action"), bg="#3E92ED",
           fg="white").place(relx=0.615, rely=0.62)
    Label(change_w, text='第4步:\n点击配置按钮\n进行路径和参数设置', font=("楷体", 12)).place(relx=0.3725, rely=0.77)
    Button(change_w, text="配置", command=open_mmd_set_w, bg="#3E92ED", fg="white").place(relx=0.615, rely=0.82)
    Label(change_w, text="更换Web背景", font=("楷体", 18, "bold"), fg="#587EF4").place(relx=0.7, rely=0.0367)
    Label(change_w, text='第1步:\n上传一张图片,\n格式需要为jpg', font=("楷体", 12)).place(relx=0.725, rely=0.15)
    Button(change_w, text="上传图片", command=upload_image, bg="#3E92ED", fg="white").place(relx=0.7375, rely=0.31)
    Label(change_w, text='第2步:\n刷新网页', font=("楷体", 12)).place(relx=0.75, rely=0.42)
    Label(change_w, text="头像管理", font=("楷体", 18, "bold"), fg="#587EF4").place(relx=0.72, rely=0.54)
    Label(change_w, text='头像文件夹\n(格式需要为png)', font=("楷体", 12)).place(relx=0.71, rely=0.62)
    Button(change_w, text="打开", command=lambda: os.startfile("data\\image\\ch"), bg="#3E92ED", fg="white").place(
        relx=0.9, rely=0.62)
    Label(change_w, text="音乐管理", font=("楷体", 18, "bold"), fg="#587EF4").place(relx=0.72, rely=0.75)
    Label(change_w, text='音乐文件夹\n(格式需要为mp3)', font=("楷体", 12)).place(relx=0.71, rely=0.83)
    Button(change_w, text="打开", command=lambda: os.startfile("data\\music"), bg="#3E92ED", fg="white").place(
        relx=0.9, rely=0.83)
    change_w.mainloop()


original_window_size = (1280, 720)
scaled_window_size = scaled_size(original_window_size)
root = tk.Tk()
root.title("枫云AI虚拟伙伴Web版 v3.0")
root.geometry(f"{scaled_window_size[0]}x{scaled_window_size[1]}")
root.attributes('-alpha', 0.9)
root.configure(bg="#EEFFFF")
root.option_add('*Font', '楷体 15')
root.option_add("*Background", "#EEFFFF")
root.option_add("*Foreground", "black")
root.iconbitmap("data/image/logo.ico")
logo_img = Image.open("data/image/logo.png")
logo_img = logo_img.resize((int(30 * scaling_factor), int(30 * scaling_factor)), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_img)
try:
    head_img = Image.open(f"data/image/ch/{mate_name}.png")
except:
    head_img = Image.open("data/image/logo.png")
head_img = head_img.resize((int(50 * scaling_factor), int(50 * scaling_factor)), Image.Resampling.LANCZOS)
head_photo = ImageTk.PhotoImage(head_img)
head_label = Label(root, image=head_photo, bg="#EEFFFF")
head_label.place(relx=0.01, rely=0.02)
Label(root, text=f"当前伙伴:\n{mate_name}", bg="#EEFFFF").place(relx=0.06, rely=0.03)
if chat_web_switch == "开启":
    Label(root,
          text=f"对话网址:\nhttp://{server_ip}:{chatweb_port}\n2D角色网址:\nhttp://{server_ip}:{live2d_port}",
          bg="#EEFFFF").place(relx=0.2, rely=0.01)
    Label(root,
          text=f"3D动作网址:\nhttp://{server_ip}:{mmd_port}/vmd\n3D角色网址:\nhttp://{server_ip}:{mmd_port}",
          bg="#EEFFFF").place(relx=0.45, rely=0.01)
else:
    Label(root, text=f"对话网址:\n未开启\n2D角色网址:\nhttp://{server_ip}:{live2d_port}",
          bg="#EEFFFF").place(relx=0.2, rely=0.01)
    Label(root,
          text=f"3D动作网址:\nhttp://{server_ip}:{mmd_port}/vmd\n3D角色网址:\nhttp://{server_ip}:{mmd_port}",
          bg="#EEFFFF").place(relx=0.45, rely=0.01)
Label(root, text="🎙语音识别模式", bg="#EEFFFF").place(relx=0.02, rely=0.41)
voice_options = ["实时语音识别", "自定义唤醒词", "关闭语音识别"]
voice_var = StringVar(root)
voice_var.set(voice_switch)
voice_option_menu = ttk.Combobox(root, textvariable=voice_var, values=voice_options, width=14, state="readonly",
                                 justify='center')
voice_option_menu.place(relx=0.02, rely=0.45)
Label(root, text="🤖对话语言模型", bg="#EEFFFF").place(relx=0.02, rely=0.53)
llm_options = ["GLM-4-Flash", "GLM-Z1-Flash", "通义千问2.5-7B", "DeepSeek-R1-7B", "InternLM2.5-7B", "腾讯混元Lite",
               "讯飞星火Lite", "Letta长期记忆", "本地Qwen整合包", "本地LM Studio", "本地Ollama LLM",
               "本地RWKV运行器", "本地OpenVINO", "Dify聊天助手", "AnythingLLM", "自定义API-LLM"]
llm_var = StringVar(root)
llm_var.set(prefer_llm)
llm_menu = ttk.Combobox(root, textvariable=llm_var, values=llm_options, height=16, width=14, state="readonly",
                        justify='center')
llm_menu.place(relx=0.02, rely=0.57)
Label(root, text="🔊语音合成引擎", bg="#EEFFFF").place(relx=0.02, rely=0.65)
tts_options = ["云端edge-tts", "云端百度TTS", "本地GPT-SoVITS", "本地CosyVoice", "本地Spark-TTS", "本地Index-TTS",
               "本地Kokoro-TTS", "本地pyttsx3", "关闭语音合成"]
tts_var = StringVar(root)
tts_var.set(prefer_tts)
tts_menu = ttk.Combobox(root, textvariable=tts_var, values=tts_options, width=14, state="readonly", justify='center')
tts_menu.place(relx=0.02, rely=0.69)
Label(root, text="🖼图像识别引擎", bg="#EEFFFF").place(relx=0.02, rely=0.77)
img_options = ["GLM-4V-Flash", "本地Ollama VLM", "本地QwenVL整合包", "本地GLM-V整合包", "本地Janus整合包",
               "自定义API-VLM", "关闭图像识别"]
img_var = StringVar(root)
img_var.set(prefer_img)
img_menu = ttk.Combobox(root, textvariable=img_var, values=img_options, width=14, state="readonly", justify='center')
img_menu.place(relx=0.02, rely=0.81)
output_box = ScrolledText(root, width=85, height=20, font=("楷体", 18))
output_box.place(relx=0.175, rely=0.14)
output_box.insert('end', history)
output_box.see("end")
input_box = ScrolledText(root, width=82, height=4, font=("楷体", 18))
input_box.place(relx=0.175, rely=0.845)
state_box = Text(root, width=18, height=3, fg="blue", bg="#EEFFFF")
state_box.place(relx=0.015, rely=0.89)
state_box.insert("end", "欢迎使用枫云AI虚拟伙伴Web版")
root.bind("<Button-3>", show_menu)
