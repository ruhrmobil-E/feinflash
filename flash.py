#!/usr/bin/env python3

import os
import time
from subprocess import check_output

time.sleep(2)
wd = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(wd, "current_line")) as current_line_file:
  current_line_file_data = current_line_file.readlines()
  if len(current_line_file_data):
    if current_line_file_data[0]:
      current_line = int(current_line_file_data[0])
    else:
      current_line = 0
  else:
    current_line = 0
with open(os.path.join(wd, "emails")) as email_file:
  for i, line in enumerate(email_file):
    if i == current_line:
      email = line.strip()

check_output(os.path.join(wd, 'venv', 'bin', 'esptool.py') + ' --port /dev/ttyUSB0 chip_id', shell=True)

sensor_flash_status = check_output(os.path.join(wd, 'venv', 'bin', 'esptool.py') + ' --port /dev/ttyUSB0  write_flash 0x00000 ' + os.path.join(wd, 'latest.bin'), shell=True)
sensor_flash_status = sensor_flash_status.decode('utf-8')
if not "100 %" in sensor_flash_status or not "Wrote" in sensor_flash_status:
  print("error flashing")
  print(sensor_flash_status)
sensor_id = check_output(os.path.join(wd, 'venv', 'bin', 'esptool.py') + ' --port /dev/ttyUSB0 chip_id', shell=True)

sensor_id = int(sensor_id.decode('utf-8').split("\n")[2][9:], 0)

current_line += 1
with open(os.path.join(wd, "current_line"), 'w') as current_line_file:
  current_line_file.write("%s" % (current_line))
with open(os.path.join(wd, "output"), 'a') as output_file:
  output_file.write("%s %s\n" % (sensor_id, email))

# reset everything
time.sleep(2)
check_output('modprobe -r ch341', shell=True)
check_output('modprobe -r usbserial', shell=True)
