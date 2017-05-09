#!/usr/bin/env python3

"""
Verwendete Dateien:
current_line: die aktuelle Zeile im email-File
emails: eine liste an emails, die zugeordnet wird
output: die zuordnung ID zu email
"""

import os
import time
from subprocess import check_output

time.sleep(2)
wd = os.path.dirname(os.path.realpath(__file__))

"""
Schritt 1: neue E-mail zum Zuordnen auslesen
"""
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

"""
Schritt 2: Flashen
"""
check_output(os.path.join(wd, 'venv', 'bin', 'esptool.py') + ' --port /dev/ttyUSB0 chip_id', shell=True)
sensor_flash_status = check_output(os.path.join(wd, 'venv', 'bin', 'esptool.py') + ' --port /dev/ttyUSB0  write_flash 0x00000 ' + os.path.join(wd, 'latest.bin'), shell=True)
sensor_flash_status = sensor_flash_status.decode('utf-8')
if not "100 %" in sensor_flash_status or not "Wrote" in sensor_flash_status:
  print("error flashing")
  print(sensor_flash_status)
  
"""
Schritt 3: Auslesen der ID
"""
sensor_id = check_output(os.path.join(wd, 'venv', 'bin', 'esptool.py') + ' --port /dev/ttyUSB0 chip_id', shell=True)

sensor_id = int(sensor_id.decode('utf-8').split("\n")[2][9:], 0)

"""
Schritt 4: Wenn Flashen und Auslesen der ID erfolgreich ist: current_line und output schreiben
"""
current_line += 1
with open(os.path.join(wd, "current_line"), 'w') as current_line_file:
  current_line_file.write("%s" % (current_line))
with open(os.path.join(wd, "output"), 'a') as output_file:
  output_file.write("%s %s\n" % (sensor_id, email))

"""
Schritt 5: Kernelmodule rauswerfen, um Fehler zu lösen
"""

time.sleep(2)
check_output('modprobe -r ch341', shell=True)
check_output('modprobe -r usbserial', shell=True)
