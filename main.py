password = "23051401@"  # <---Mude a senha

import requests, random, string, secmail, pyshorteners, amino, names, json, os
from bs4 import BeautifulSoup
from time import sleep
from amino.lib.util.exceptions import ActionNotAllowed, IncorrectVerificationCode, ServiceUnderMaintenance
from pyfiglet import figlet_format
from urllib.request import urlopen
from flask import Flask
import heroku3

abertura = figlet_format("a c c g e n  X\n       p t - b r")
print(abertura)


# ===============Funções==================
def restart():
    heroku_conn = heroku3.from_key("95fd8d7f-8d53-42c7-a22f-c0d7ea84bb43")
    botapp = heroku_conn.apps()["herokux20"]
    botapp.restart()


def nome_aleatorio():
    nome = ''
    for i in names.get_first_name():
        nome += i
    return nome


def api(url):
    return requests.post("https://api-xmega11.herokuapp.com/", data={"text": url}).json()['captcha']


def deviceId():
    return requests.get("http://forevercynical.com/generate/deviceid").text


def gerar_aleatorio(size=16, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def gerar_email():
    email = "xmega-" + gerar_aleatorio() + "@wwjmp.com"
    return email


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


def encurtar_link(link):
    ps = pyshorteners.Shortener()
    return ps.tinyurl.short(fr"{link}")


def salvar(data):
    requests.post("https://salvarcontas.0010101001101001010100101001.repl.co/save", data=data)


# ==================Gerador=============================
print("="*60)
print("                                  accgen X Heroku 24/7")
print("="*60)

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def home():
    while True:
        contador = 0
        try:
            with open("device.json", "w") as f:
                f.close()

            client = amino.Client()
            email = gerar_email()
            nickname = nome_aleatorio() + '⁹⁹⁹'
            print(f"\nGerando email {email}")
            client.request_verify_code(email=email)
            link = encurtar_link(link_codigo(email))
            codigo = api(link)
            # codigo = input("[\033[1;37mCódigo\033[m]: ")
            # slk = api(link)

            device = deviceId()
            client.register(nickname, email, password, codigo, device)
            client.login(email=email, password=password)
            # client.join_community("39276113")  # <----- Sua cid da comunidade
            # img = urlopen(f"{link}").read()
            # open(f"G:/AMINO COINS/FOLLOW/bd_captcha/{codigo}.png", "wb").write(img)

            contador += 1

            d = {
                "email": str(email),
                "password": str(password),
                "device": str(device)
            }

            j = json.dumps(d)
            data = {'data': j}
            salvar(data)
            print("Conta salva!")

        except ActionNotAllowed:
            # print("\n[\033[1;31mAtenção\033[m] \033[1;33mLimite de contas criadas atingido, mude o VPN!\033[m")
            restart()

        except IncorrectVerificationCode:
            # print("\n[\033[1;31mAtenção\033[m] \033[1;33mVocê digitou o código errado, reinicie o script!\033[m")
            restart()

        except ServiceUnderMaintenance:
            # print("\n[\033[1;31mAtenção\033[m] \033[1;33mParece que o serviço está em manutenção, tente mais tarde!")
            restart()

        except:
            # print("\n[\033[1;31mAtenção\033[m] \033[1;33mErro desconhecido, tente reiniciar o script!")
            restart()


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == "__main__":
    home()
