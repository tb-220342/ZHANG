# 多模态模型模块
import cv2
import numpy as np
import pyautogui as pag
from base64 import b64encode
from ollama import Client
from function import *

img_path = "data/cache/cache.jpg"
photo_path = "data/cache/cache.png"
glm_url = "https://open.bigmodel.cn/api/paas/v4"


def glm_4v_cam(question):  # 多模态模型读取摄像头
    cap = cv2.VideoCapture(cam_num, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return "无法打开摄像头"
    ret, frame = cap.read()
    cap.release()
    base64_image = encode_image(frame)
    messages = [{"role": "user", "content": [{"type": "text", "text": question}, {"type": "image_url", "image_url": {
        "url": f"data:image/png;base64,{base64_image}"}}]}]
    vlm_client = OpenAI(base_url=glm_url, api_key=glm_key)
    completion = vlm_client.chat.completions.create(model="glm-4v-flash", messages=messages)
    return completion.choices[0].message.content


def glm_4v_screen(question):  # 多模态模型读取电脑屏幕
    screenshot = pag.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    base64_image = encode_image(screenshot_bgr)
    messages = [{"role": "user", "content": [{"type": "text", "text": question}, {"type": "image_url", "image_url": {
        "url": f"data:image/png;base64,{base64_image}"}}]}]
    vlm_client = OpenAI(base_url=glm_url, api_key=glm_key)
    completion = vlm_client.chat.completions.create(model="glm-4v-flash", messages=messages)
    return completion.choices[0].message.content


def ollama_vlm_cam(question):
    try:
        rq.get(f'http://{local_server_ip}:{ollama_port}')
    except:
        Popen(f"ollama pull {ollama_vlm_name}", shell=False)
    cap = cv2.VideoCapture(cam_num, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return "无法打开摄像头"
    ret, frame = cap.read()
    cap.release()
    _, buffer = cv2.imencode('.jpg', frame)
    byte_data = buffer.tobytes()
    client = Client(host=f'{local_server_ip}:{ollama_port}')
    response = client.chat(model=ollama_vlm_name,
                           messages=[{'role': 'user', 'content': question, 'images': [byte_data]}])
    return response['message']['content']


def ollama_vlm_screen(question):
    try:
        rq.get(f'http://{local_server_ip}:{ollama_port}')
    except:
        Popen(f"ollama pull {ollama_vlm_name}", shell=False)
    screenshot = pag.screenshot()
    screenshot.save(img_path, "JPEG")
    with open(img_path, 'rb') as file5:
        image = file5.read()
    os.remove(img_path)
    client = Client(host=f'{local_server_ip}:{ollama_port}')
    response = client.chat(model=ollama_vlm_name,
                           messages=[{'role': 'user', 'content': question, 'images': [image]}])
    return response['message']['content']


def qwen_vlm_cam(question):
    cap = cv2.VideoCapture(cam_num, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return "无法打开摄像头"
    ret, frame = cap.read()
    cap.release()
    _, buffer = cv2.imencode('.jpg', frame)
    base64_image = b64encode(buffer).decode('utf-8')
    data = {"image": f"data:image/jpeg;base64,{base64_image}", "msg": question}
    response = rq.post(f"http://{local_server_ip}:8086/qwen_vl", json=data)
    return response.json()["answer"]


def qwen_vlm_screen(question):
    screenshot = pag.screenshot()
    screenshot.save(img_path, "JPEG")
    with open(img_path, "rb") as image_file:
        base64_image = b64encode(image_file.read()).decode('utf-8')
    data = {"image": f"data:image/jpeg;base64,{base64_image}", "msg": question}
    os.remove(img_path)
    response = rq.post(f"http://{local_server_ip}:8086/qwen_vl", json=data)
    return response.json()["answer"]


def glm_v_cam(question):
    cap = cv2.VideoCapture(cam_num, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return "无法打开摄像头"
    ret, frame = cap.read()
    cap.release()
    _, buffer = cv2.imencode('.jpg', frame)
    base64_image = b64encode(buffer).decode('utf-8')
    data = {"image": f"data:image/jpeg;base64,{base64_image}", "msg": question}
    response = rq.post(f"http://{local_server_ip}:8085/glm_edge_v", json=data)
    return response.json()["answer"]


def glm_v_screen(question):
    screenshot = pag.screenshot()
    screenshot.save(img_path, "JPEG")
    with open(img_path, "rb") as image_file:
        base64_image = b64encode(image_file.read()).decode('utf-8')
    data = {"image": f"data:image/jpeg;base64,{base64_image}", "msg": question}
    os.remove(img_path)
    response = rq.post(f"http://{local_server_ip}:8085/glm_edge_v", json=data)
    return response.json()["answer"]


def janus_cam(question):
    cap = cv2.VideoCapture(cam_num, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return "无法打开摄像头"
    ret, frame = cap.read()
    cap.release()
    _, buffer = cv2.imencode('.jpg', frame)
    files = {'file': ('image.jpg', buffer.tobytes(), 'image/jpeg')}
    data = {'question': question, 'seed': 42, 'top_p': 0.95, 'temperature': 0.1}
    response = rq.post(f"http://{local_server_ip}:8082/understand_image_and_question/", files=files, data=data)
    return response.json()['response']


def janus_screen(question):
    screenshot = pag.screenshot()
    screenshot.save(img_path, "JPEG")
    with open(img_path, 'rb') as image_file:
        files = {'file': image_file}
        data = {'question': question, 'seed': 42, 'top_p': 0.95, 'temperature': 0.1}
        response = rq.post(f"http://{local_server_ip}:8082/understand_image_and_question/", files=files, data=data)
    os.remove(img_path)
    return response.json()['response']


def encode_image(image):  # 图片转base64
    _, buffer = cv2.imencode('.png', image)
    return b64encode(buffer).decode('utf-8')


def custom_vlm_cam(question):
    cap = cv2.VideoCapture(cam_num, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return "无法打开摄像头"
    ret, frame = cap.read()
    cap.release()
    base64_image = encode_image(frame)
    messages = [{"role": "user", "content": [{"type": "text", "text": question}, {"type": "image_url", "image_url": {
        "url": f"data:image/png;base64,{base64_image}"}}]}]
    vlm_client = OpenAI(base_url=custom_url, api_key=custom_key)
    completion = vlm_client.chat.completions.create(model=custom_vlm, messages=messages)
    return completion.choices[0].message.content


def custom_vlm_screen(question):
    screenshot = pag.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    base64_image = encode_image(screenshot_bgr)
    messages = [{"role": "user", "content": [{"type": "text", "text": question}, {"type": "image_url", "image_url": {
        "url": f"data:image/png;base64,{base64_image}"}}]}]
    vlm_client = OpenAI(base_url=custom_url, api_key=custom_key)
    completion = vlm_client.chat.completions.create(model=custom_vlm, messages=messages)
    return completion.choices[0].message.content


def glm_4v_photo(question):
    with open(photo_path, "rb") as image_file:
        base64_image = b64encode(image_file.read()).decode('utf-8')
    messages = [{"role": "user", "content": [{"type": "text", "text": question}, {"type": "image_url", "image_url": {
        "url": f"data:image/png;base64,{base64_image}"}}]}]
    vlm_client = OpenAI(base_url=glm_url, api_key=glm_key)
    completion = vlm_client.chat.completions.create(model="glm-4v-flash", messages=messages)
    return completion.choices[0].message.content


def ollama_vlm_photo(question):
    try:
        rq.get(f'http://{local_server_ip}:{ollama_port}')
    except:
        Popen(f"ollama pull {ollama_vlm_name}", shell=False)
    with open(photo_path, 'rb') as file:
        image = file.read()
    client = Client(host=f'{local_server_ip}:{ollama_port}')
    response = client.chat(model=ollama_vlm_name,
                           messages=[{'role': 'user', 'content': question, 'images': [image]}])
    return response['message']['content']


def qwen_vlm_photo(question):
    with open(photo_path, "rb") as image_file:
        base64_image = b64encode(image_file.read()).decode('utf-8')
    data = {"image": f"data:image/jpeg;base64,{base64_image}", "msg": question}
    response = rq.post(f"http://{local_server_ip}:8086/qwen_vl", json=data)
    return response.json()["answer"]


def glm_v_photo(question):
    with open(photo_path, "rb") as image_file:
        base64_image = b64encode(image_file.read()).decode('utf-8')
    data = {"image": f"data:image/jpeg;base64,{base64_image}", "msg": question}
    response = rq.post(f"http://{local_server_ip}:8085/glm_edge_v", json=data)
    return response.json()["answer"]


def janus_photo(question):
    with open(photo_path, 'rb') as image_file:
        files = {'file': image_file}
        data = {'question': question, 'seed': 42, 'top_p': 0.95, 'temperature': 0.1}
        response = rq.post(f"http://{local_server_ip}:8082/understand_image_and_question/", files=files, data=data)
    return response.json()['response']


def custom_vlm_photo(question):
    with open(photo_path, "rb") as image_file:
        base64_image = b64encode(image_file.read()).decode('utf-8')
    messages = [{"role": "user", "content": [{"type": "text", "text": question}, {"type": "image_url", "image_url": {
        "url": f"data:image/png;base64,{base64_image}"}}]}]
    vlm_client = OpenAI(base_url=custom_url, api_key=custom_key)
    completion = vlm_client.chat.completions.create(model=custom_vlm, messages=messages)
    return completion.choices[0].message.content
