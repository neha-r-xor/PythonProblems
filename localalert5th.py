
import paramiko
import time
import re

HOST = "10.81.1.116"
USERNAME = "interns"
PASSWORD = "123123"
LOG_FILE = "alerts.log"

# def get_metrics(ssh):

#     stdin, stdout, stderr = ssh.exec_command("top -bn1 | head -5")
#     cpu_output = stdout.read().decode()

#     stdin, stdout, stderr = ssh.exec_command("free -m")
#     mem_output = stdout.read().decode()

#     stdin, stdout, stderr = ssh.exec_command("df -h | tail -1")
#     disk_output = stdout.read().decode()
    
#     return cpu_output, mem_output, disk_output

# def parse_cpu(cpu_output):
#     # Look for "Cpu(s):  xx.x id" line
#     match = re.search(r"Cpu\(s\):\s+(\d+\.\d+)\s+us", cpu_output)
#     if match:
#         return float(match.group(1))
#     return 0.0

# def parse_disk(disk_output):
#     # Last column before mount point is usage %
#     match = re.search(r"(\d+)%", disk_output)
#     if match:
#         return int(match.group(1))
#     return 0

def log_alert(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.ctime()} - ALERT: {message}\n")

# def main():
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(HOST, username=USERNAME, password=PASSWORD)
    
#     while True:
#         cpu_output, mem_output, disk_output = get_metrics(ssh)
#         cpu_usage = parse_cpu(cpu_output)
#         disk_usage = parse_disk(disk_output)
        
#         if cpu_usage > 80 or disk_usage > 90:
#             log_alert(f"CPU: {cpu_usage}%, Disk: {disk_usage}%")
        
#         time.sleep(5)


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USERNAME, password=PASSWORD)
    
    channel = ssh.invoke_shell()
    time.sleep(1)

    while True:
        channel.send("top -bn1 | head -5\n")
        time.sleep(1)
        cpu_output = channel.recv(4096).decode()

        channel.send("df -h | tail -1\n")
        time.sleep(1)
        disk_output = channel.recv(4096).decode()

        match_cpu = re.search(r"Cpu\(s\):\s+(\d+\.\d+)\s+us", cpu_output)
        cpu_usage = float(match_cpu.group(1)) if match_cpu else 0.0
        
        match_disk = re.search(r"(\d+)%", disk_output)
        disk_usage = int(match_disk.group(1)) if match_disk else 0
        
        if cpu_usage > 80 or disk_usage > 90:
            log_alert(f"CPU: {cpu_usage}%, Disk: {disk_usage}%")
        
        time.sleep(5)

if __name__ == "__main__":
    main()


