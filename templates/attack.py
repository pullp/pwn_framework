#coding:utf-8
import subprocess

TIMEOUT = 10
FLAG_PATTERN = "flag{"
EXP_PATH = "./exp.py"

def runcmd(command):
    p = subprocess.Popen(
        command,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"
    )
    lines = p.stdout.readlines()
    res = False
    for l in lines:
        if FLAG_PATTERN in l:
            print(l)
            res = True
        if b"INFO" in l:
            print(l)
    return res

targets = []

import time

time.sleep(60)
print(time.strftime("%m-%d %H:%M:%S", time.localtime()))

for i in range(20):
    cmd = f"timeout {TIMEOUT} python {EXP_PATH} {i}"
    runcmd(cmd)



# import requests
# import json
# def submit_flag(flag, token=""):
#     import requests
#     url = "https://172.20.1.1/Answerapi/sub_answer_api"
#     r = requests.post(url, data={"answer":flag, "playertoken":token}, verify=False)
#     print("INFO", json.loads(r.text)['msg'])
#     return r.text
