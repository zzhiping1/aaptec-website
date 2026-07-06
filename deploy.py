import paramiko
import os

HOST = "121.43.35.58"
USER = "root"
PASS = "Cptbtptp99"
REMOTE_DIR = "/opt/aaptec"
LOCAL_DIR = r"D:\claude\aaptec"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, 22, USER, PASS)
sftp = ssh.open_sftp()

# Upload HTML files
for f in ["index.html", "services.html", "training.html", "products.html", "about.html", "contact.html"]:
    local = os.path.join(LOCAL_DIR, f)
    remote = f"{REMOTE_DIR}/{f}"
    sftp.put(local, remote)
    print(f"Uploaded {f}")

# Upload images
os.makedirs(os.path.join(LOCAL_DIR, "images"), exist_ok=True)
for f in os.listdir(os.path.join(LOCAL_DIR, "images")):
    local = os.path.join(LOCAL_DIR, "images", f)
    if os.path.isfile(local):
        remote = f"{REMOTE_DIR}/images/{f}"
        sftp.put(local, remote)
        print(f"Uploaded images/{f}")

sftp.close()

# Kill existing server and restart
stdin, stdout, stderr = ssh.exec_command("pkill -f 'python3 -m http.server 8088' || true")
stdout.read()
stdin, stdout, stderr = ssh.exec_command(f"cd {REMOTE_DIR} && nohup python3 -m http.server 8088 --bind 0.0.0.0 > /dev/null 2>&1 &")
stdout.read()
print("Server restarted on port 8088")

# Verify
stdin, stdout, stderr = ssh.exec_command("curl -s -o /dev/null -w '%{http_code}' http://localhost:8088/")
code = stdout.read().decode().strip()
print(f"Local check: HTTP {code}")

ssh.close()
print("Deployment complete!")
