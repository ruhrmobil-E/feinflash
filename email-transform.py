#!/usr/bin/env python3

import os

wd = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(wd, "emails_raw")) as email_raw_file:
  with open(os.path.join(wd, "emails"), 'w') as email_file:
    for i, line in enumerate(email_raw_file):
      email_raw = line.split()
      if len(email_raw) != 2 and line:
        print("Unbekannte Zeile: %s" % line)
      else:
        num = int(email_raw[1])
        for i in range(0, num):
          email_file.write("%s\n" % (email_raw[0].strip().lower()))
