#!/bin/bash

# 获取脚本所在目录的绝对路径
script_dir=$(dirname "$(readlink -f "$0")")

# 指定Python脚本的相对路径（相对于脚本所在目录）
python_script="auto_connect_wifi_script.py"

# 检查Python环境
python_path=$(which python3)
if [ -z "$python_path" ]; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# 检查参数个数
if [ $# -lt 2 ]; then
    echo "Usage: $0 <SSID> <password>"
    exit 1
fi

# 接收参数
ssid=$1
password=$2

# 添加执行权限
chmod +x "$python_script"

# 删除现有的启动脚本（如果存在）
sudo rm /etc/init.d/myscript

# 创建新的启动脚本
cat <<EOF | sudo tee /etc/init.d/myscript > /dev/null
#!/bin/bash
### BEGIN INIT INFO
# Provides:          myscript
# Required-Start:    \$remote_fs \$syslog
# Required-Stop:     \$remote_fs \$syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start script at boot time
# Description:       Enable service provided by script.
### END INIT INFO

ssid="$ssid"
password="$password"

case "\$1" in
    start)
        echo "Starting myscript..."
        $python_path $script_dir/$python_script \$ssid \$password &
        ;;
    stop)
        echo "Stopping myscript..."
        pkill -f $python_script
        ;;
    restart)
        echo "Restarting myscript..."
        pkill -f $python_script
        sleep 2
        $python_path $script_dir/$python_script \$ssid \$password &
        ;;
    *)
        echo "Usage: \$0 {start|stop|restart}"
        exit 1
        ;;
esac

exit 0
EOF

# 添加执行权限
sudo chmod +x /etc/init.d/myscript

# 更新启动项
if command -v update-rc.d >/dev/null 2>&1; then
    sudo update-rc.d myscript defaults
elif command -v chkconfig >/dev/null 2>&1; then
    sudo chkconfig --add myscript
fi

echo "Script added to startup."
