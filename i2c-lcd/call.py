import os

import time
from lcd1602 import *
from datetime import datetime

# run command
def run_cmd(cmd):
    p = os.popen(cmd).readline().strip().split()
    return p


def now():
    return datetime.now().strftime('%Y-%m-%d %a \n%H:%M:%S')

def cpu():
    cpu_temp = run_cmd('vcgencmd measure_temp')
    cpu_info = run_cmd("top -bn1 | awk '/Cpu\(s\)/'")
    cpu_usage = 1 - float(cpu_info[7])/100.0

    status = 'CPU Temp: {}\n'.format(cpu_temp[0].replace("temp=", ""))
    status += 'Used: {:.2%}'.format(cpu_usage)
    return status

def ram():
    ram_info = run_cmd("free -m | awk '/Mem/'")
    ram_usage = (int(ram_info[1]) - int(ram_info[6])) / float(ram_info[1])

    status = 'RAM Totl: {}M\n'.format(ram_info[1])
    status += 'Used: {:.2%}'.format(ram_usage)
    return status

def ip():
    ip = run_cmd("sudo ifconfig wlan0 | awk '/inet/'")
    return 'IP:\n{}'.format(ip[1])

print(now(), cpu(), ram(), ip(), sep='\n')


def output(msg):
    clear_lcd()
    lines = msg.split('\n', 2)
    print_lcd(0, 0, lines[0])
    if lines[1]:
        print_lcd(0, 1, lines[1])


init_lcd()
funcs = [now, cpu, ram, ip]

while(1):
    try:
        for func in funcs:
            output(func())
            time.sleep(2)
    except Exception as ex:
        print(ex)
        time.sleep(5)
        try:
            init_lcd()
        except Exception:
            print('init failed')
