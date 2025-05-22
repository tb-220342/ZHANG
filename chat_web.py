# 对话网页模块
import flet as ft
from flet_core import Image as ImageW
from flet_core import Row
from llm import *
from tts import *


def get_head(head_name):  # 获取头像
    head_path = f"data/image/ch/{head_name}.png"
    if os.path.exists(head_path):
        return head_path
    else:
        return "data/image/logo.png"


class Message:  # 对话消息
    def __init__(self, user_name2: str, text: str, message_type: str):
        self.user_name2 = user_name2
        self.text = text
        self.message_type = message_type


class ChatMessage(ft.Row):  # 对话消息
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(content=ImageW(get_head(message.user_name2), width=50, height=50)),
            ft.Column([ft.Text(message.user_name2, weight=ft.FontWeight.BOLD, size=20),
                       ft.TextField(value=message.text, read_only=True, focused_bgcolor="#ebebeb",
                                    border=ft.InputBorder.NONE, max_lines=100, filled=True, border_radius=2)],
                      tight=True, spacing=5, )]


def web_main(page: ft.Page):  # 网页主函数
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.title = "対話 - 楓雲AI仮想パートナーWeb版"
    logo_image = ImageW("data/image/logo.png", width=25, height=25)
    title_label = ft.Text(value="楓雲AI仮想パートナーWeb版", size=22, color="#587EF4")
    ip_label1 = ft.Text(value=f"2DキャラクターURL: http://{server_ip}:{live2d_port}", size=16)
    ip_label2 = ft.Text(value=f"3DキャラクターURL: http://{server_ip}:{mmd_port}", size=16)
    open_ch_2d_bt = ft.ElevatedButton(text="2Dキャラクターを開く(ホスト)", on_click=open_ch_2d)
    open_ch_3d_bt = ft.ElevatedButton(text="3Dキャラクターを開く(ホスト)", on_click=open_ch_3d)
    row1 = Row([logo_image, title_label])
    page.add(row1)
    row2 = Row([ip_label1, open_ch_2d_bt])
    page.add(row2)
    row3 = Row([ip_label2, open_ch_3d_bt])
    page.add(row3)

    def join_chat_click(e):  # 加入对话
        if not join_user_name.value:
            join_user_name.error_text = "名前を入力してください！"
            join_user_name.update()
        elif join_password.value != password:
            join_password.error_text = "パスワードが違います"
            join_password.update()
        else:
            page.session.set("user_name2", join_user_name.value)
            page.dialog.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(
                Message(user_name2=join_user_name.value, text=f"{join_user_name.value} がチャットに参加しました",
                        message_type="login_message"))
            page.update()

    def send_message_click(e):  # 发送消息
        user_name2 = page.session.get("user_name2")
        user_message = new_message.value.strip()
        if user_message == "":
            state.value = "内容を入力してから送信してください"
            page.update()
            return
        state.value = f"メッセージ送信済み、【{mate_name}】が思考中..."
        page.pubsub.send_all(Message(user_name2=user_name2, text=user_message, message_type="chat_message"))
        new_message.value = ""
        new_message.focus()
        bot_response = chat_llm(prompt, user_message)
        bot_response = bot_response.replace("#", "").replace("*", "")
        if think_filter_switch == "开启":
            bot_response = bot_response.split("</think>")[-1].strip()
        state.value = f"【{mate_name}】からの返信を受信しました"
        page.pubsub.send_all(Message(user_name2=mate_name, text=bot_response, message_type="chat_message"))
        get_tts_play_live2d(bot_response)

    def export_chat2(e):  # 导出对话
        messages = []
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        ch = [username, mate_name]
        for control in chat.controls:
            if isinstance(control, ChatMessage):
                messages.append(ch[0] + ":\n" + control.controls[1].controls[1].value)
                ch.reverse()
        file_path = f'data/history/楓雲AI仮想パートナーWeb版_{mate_name}_対話記録_{timestamp}.txt'
        with open(file_path, 'w', encoding='utf-8') as file3:
            for message in messages:
                file3.write(message + '\n\n')
        state.value = f"対話履歴は data/history/楓雲AI仮想パートナーWeb版_{mate_name}_対話記録_{timestamp}.txt にエクスポートされました"
        page.update()

    def clean_chat(e):  # 清空对话
        chat.controls.clear()
        clean_chat_web()
        state.value = "記録とコンテキストメモリは消去されました"
        page.update()

    def on_message(message: Message):  # 对话消息
        m = None
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.GREEN, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)
    join_user_name = ft.TextField(label="ユーザー名", value=username, autofocus=True, on_submit=join_chat_click)
    join_password = ft.TextField(label="パスワード", value="", autofocus=True, password=True)
    page.dialog = ft.AlertDialog(open=True, modal=True, title=ft.Text("楓雲AI仮想パートナーWeb版"),
                                 content=ft.Column([join_user_name, join_password], width=300, height=120, tight=True),
                                 actions=[ft.ElevatedButton(text="ログイン", on_click=join_chat_click)],
                                 actions_alignment=ft.MainAxisAlignment.END)
    chat = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    new_message = ft.TextField(hint_text="メッセージを入力してください...", autofocus=True, shift_enter=True, min_lines=1,
                               max_lines=5, filled=True, expand=True, on_submit=send_message_click)
    page.add(ft.Container(
        content=chat, border=ft.border.all(1, ft.colors.OUTLINE), border_radius=5, padding=10, expand=True),
        ft.Row([ft.IconButton(icon=ft.icons.DOWNLOAD_ROUNDED, tooltip="履歴をエクスポート", on_click=export_chat2),
                ft.IconButton(icon=ft.icons.ADD_ROUNDED, tooltip="新しい対話を開始", on_click=clean_chat), new_message,
                ft.IconButton(icon=ft.icons.SEND_ROUNDED, tooltip="メッセージを送信", on_click=send_message_click)]))
    state = ft.Text("楓雲AI仮想パートナーWeb版へようこそ")
    page.add(state)
