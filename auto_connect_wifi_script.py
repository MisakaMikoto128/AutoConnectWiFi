import subprocess
import time
import sys
def check_wifi_interface():
    try:
        # 使用iwconfig命令检查无线网卡接口
        result = subprocess.run(['iwconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
        output = result.stdout

        # 检查输出中是否包含无线网卡接口（通常以"wl"开头）
        if 'wl' in output:
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error checking WiFi interface: {e}")
        return False

def connect_to_wifi(ssid, password):
    try:
        # 使用nmcli命令连接WiFi网络
        subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error connecting to WiFi: {e}")


def check_have_ssid(target_ssid):
    ret = False

    # 使用nmcli命令获取WiFi网络列表
    result = subprocess.run(['nmcli', '-f', 'SSID', 'dev', 'wifi', 'list'],  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    output = result.stdout

    # 检查输出中是否包含目标热点的SSID
    if target_ssid in output:
        ret = True
    
    return ret

def get_connected_wifi_ssid():
    try:
        # 使用nmcli命令获取已连接的WiFi信息
        result = subprocess.run(['iwgetid', '--raw'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
        output = result.stdout.strip()

        # 解析输出，提取已连接的WiFi热点的SSID
        ssid = output

        return ssid
    except subprocess.CalledProcessError as e:
        print(f"Error getting connected WiFi SSID: {e}")
        print(f"Command: {e.cmd}")
        print(f"Exit code: {e.returncode}")
        print(f"Output: {e.output}")
        return None
    
# 指定WiFi网络的SSID和密码
# 获取命令行参数
wifi_ssid = sys.argv[1]
wifi_password = sys.argv[2]

# 循环扫描并连接目标热点
while True:
    time.sleep(1)
    # 检查WiFi网卡接口是否存在
    if not check_wifi_interface():
        print("WiFi interface not found. Retrying...")
        continue
    else:
        print("WiFi interface found.")

    # 检查目标热点是否存在
    if not check_have_ssid(wifi_ssid):
        print(f"Target WiFi network '{wifi_ssid}' not found. Retrying...")
        continue
    else:
        print(f"Target WiFi network '{wifi_ssid}' found.")

    # 连接到目标热点
    connect_to_wifi(wifi_ssid, wifi_password)

    # 检查是否已连接到目标热点
    connected_ssid = get_connected_wifi_ssid()
    if connected_ssid != wifi_ssid:
        print(f"Error connecting to WiFi network '{wifi_ssid}'. Retrying...")
        continue
    else:
        print(f"Connected to WiFi network '{wifi_ssid}'.")

    time.sleep(10)

    
