import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

if os.name != 'posix':
    sys.exit('{} platform not supported'.format(os.name))

try:
    import psutil
except ImportError:
    print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
    sys.exit()

from luma.core.render import canvas
from PIL import ImageFont

from luma.core.interface.serial import i2c, spi
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106

try:
    import psutil
except ImportError:
    print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
    sys.exit()


# TODO: custom font bitmaps for up/down arrows
# TODO: Load histogram


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n

def cpu_speed():
    cmd = "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"
    freq = subprocess.check_output(cmd, shell = True )
    return "FREQ: " + str(freq)

def cpu_usage():
    # load average, uptime
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    av1, av2, av3 = os.getloadavg()
    return "Ld:%.1f %.1f %.1f Up: %s" \
        % (av1, av2, av3, str(uptime).split('.')[0])


def get_temp():
    # get cpu temperature
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as temp:
            tmpCel = int(temp.read()[:2])
            tmpPercent = (tmpCel / 55) * 100
    except:
        tmpCel = 0
    finally:
        return "Temp: %s°C" % \
        (str(tmpCel))

def mem_usage():
    usage = psutil.virtual_memory()
    return "Mem: %s %.0f%%" \
        % (bytes2human(usage.used), 100 - usage.percent)

def ip():
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    return "IP: " + str(IP)

def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx%s, Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))

def disk_usage():
    usage1 = psutil.disk_usage('/')
    usage2 = psutil.disk_usage('/srv/dev-disk-by-uuid-042CC2FF2CC2EB2E')
    return "SD: %s %.0f%% HDD1: %s %.0f%%" \
        % (bytes2human(usage1.used), usage1.percent, bytes2human(usage2.used), usage2.percent)

def stats(device):
    # use custom font
    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', 'C&C Red Alert [INET].ttf'))
    font2 = ImageFont.truetype(font_path, 12)

    with canvas(device) as draw:
        draw.text((0, 0), "Raspberry Pi 4 NAS", font=font2, fill="white")
        draw.text((0, 10), cpu_usage(), font=font2, fill="white")
        draw.text((0, 19), get_temp(), font=font2, fill="white")
        draw.text((0, 28), mem_usage(), font=font2, fill="white")
        draw.text((0, 37), ip(), font=font2, fill="white")
        try:
            draw.text((0, 46), network('wlan0'), font=font2, fill="white")
        except KeyError:
            draw.text((0, 46), network('eth0'), font=font2, fill="white")
            pass
        draw.text((0, 55), disk_usage(), font=font2, fill="white")


def main():
    while True:
        stats(device)
        time.sleep(1)


if __name__ == "__main__":
    try:
        serial = i2c(port=1, address=0x3C)
        device = sh1106(serial)
        main()
    except KeyboardInterrupt:
        pass

