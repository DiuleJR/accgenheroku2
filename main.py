import amino, string, random, secmail
import os
import json
import threading
import requests
import wget
import heroku3
from new import emaill, passwordd, custompwd, chatlink, key, app_name, deviceid, nickname, url
from time import sleep
from bs4 import BeautifulSoup


def gerar_aleatorio(size=16, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def gerar_email():
    email = "xmega-" + gerar_aleatorio() + "@wwjmp.com"
    return email


def deviceId():
    return requests.get("https://device-xmega.herokuapp.com/").text


def restart():
    heroku_conn = heroku3.from_key(key)
    botapp = heroku_conn.apps()[app_name]
    botapp.restart()


def send(data):
    requests.post(f"{url}/save", data=data)


client = amino.Client(deviceid)
client.login(emaill, passwordd)
bb = client.get_from_code(chatlink)
chatId = bb.objectId
cid = bb.path[1:bb.path.index("/")]
client.join_community(cid)
sub = amino.SubClient(comId=cid, profile=client.profile)
sub.join_chat(chatId)


def find():
    while True:
        p = sub.get_chat_messages(chatId=chatId, size=1).content
        # print(p)
        for j in p:
            g = j
        # print(g)
        l = f"{g}"
        length = str(len(l))
        if "6" == length:
            break
    return g


def link_codigo(email):
    try:
        mail = secmail.SecMail()
        sleep(3)
        inbox = mail.get_messages(email)
        for Id in inbox.id:
            msg = mail.read_message(email=email, id=Id).htmlBody
            bs = BeautifulSoup(msg, 'html.parser')
            images = bs.find_all('a')[0]
            url = (images['href'])
            if url is not None:
                return url
    except:
        pass


password = custompwd
de = deviceId()
client = amino.Client(de)
for _ in range(3):
    try:
        os.remove("code.png")
    except:
        pass
    dev = client.device_id
    email = gerar_email()
    print(email)
    client.request_verify_code(email=email)
    link = client.get_message(email)
    wget.download(url=link, out="code.png")
    with open("code.png", "rb") as file:
        sub.send_message(chatId=chatId, fileType="image", file=file)
    p = sub.get_chat_messages(chatId=chatId, size=1).content
    code = find()

    try:
        client.register(email=email, password=password, nickname=nickname, verificationCode=code, deviceId=dev)
        sub.send_message(chatId=chatId, message="vercel")
        d = {}
        d["email"] = str(email)
        d["password"] = str(password)
        d["device"] = str(dev)
        t = json.dumps(d)
        data = {"data": t}
        send(data)
    except Exception as l:
        print(l)
        pass

de = deviceId()
client = amino.Client(de)
for _ in range(2):
    try:
        os.remove("code.png")
    except:
        pass
    dev = deviceId()
    email = gerar_email()
    print(email)
    client.request_verify_code(email=email)
    link = client.get_message(email)
    wget.download(url=link, out="code.png")
    with open("code.png", "rb") as file:
        sub.send_message(chatId=chatId, fileType="image", file=file)
    code = find()

    try:
        client.register(email=email, password=password, nickname=nickname, verificationCode=code, deviceId=dev)
        sub.send_message(chatId=chatId, message="vercel")
        d = {}
        d["email"] = str(email)
        d["password"] = str(password)
        d["device"] = str(dev)
        t = json.dumps(d)
        data = {"data": t}
        send(data)
    except Exception as k:
        print(k)
        pass

restart()
