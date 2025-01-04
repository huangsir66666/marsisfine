import threading
import time
import requests
from loguru import logger
from solders.keypair import Keypair

def wallet():
    keypair = Keypair()
    pubkey = str(keypair.pubkey())
    prikey = str(keypair.from_json(keypair.to_json()))
    return pubkey, prikey


def submit(addr, captcha):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "dnt": "1",
        "origin": "https://marsisfine.xyz",
        "priority": "u=1, i",
        "referer": "https://marsisfine.xyz/",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    url = "https://api.marsisfine.xyz/white-list/create"
    data = {
        "address": addr,
        "captcha": captcha
    }
    response = requests.post(url, headers=headers, json=data)
    logger.debug(response.text)


def nocaptcha_init(token):
    session = requests.session()
    session.headers.update({
        "User-Token": token,
        "Content-Type": "application/json",
        "Developer-Id": "hQxLji"
    })
    return session


def hcaptcha(captcha_session):
    while True:
        try:
            data = {
                "sitekey": "d54cd98e-337a-4572-9dac-067c1d509610",
                "referer": "https://marsisfine.xyz/",
            }
            response = captcha_session.post("http://api.nocaptcha.io/api/wanda/hcaptcha/universal", json=data)
            logger.debug(response.text.encode('utf-8').decode('unicode_escape'))
            result = response.json()['data']['generated_pass_UUID']
            return result
        except:
            time.sleep(1)
            continue


def main(captcha_session):
    while True:
        try:
            pubkey, prikey = wallet()
            captcha_result = hcaptcha(captcha_session)
            submit(pubkey, captcha_result)
            with open("wallet.txt", "a") as f:
                f.write(f"{pubkey}----{prikey}\n")
        except Exception as e:
            logger.error(e)



if __name__ == '__main__':
    nocaptcha_token = "nocaptcha的token"
    captcha_session = nocaptcha_init(nocaptcha_token)
    # 线程数
    for i in range(10):
        threading.Thread(target=main, args=(captcha_session,)).start()
