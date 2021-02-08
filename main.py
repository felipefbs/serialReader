#!/usr/bin/python3

import serial
import serial.tools.list_ports
import logging

logging.basicConfig(filename="test.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%d-%m-%Y|%H:%M:%S',
                    level=logging.DEBUG)
logging.info("Started log")


while True:
    ports = serial.tools.list_ports.comports()

    serialPortList = []

    for port, desc, hwid in sorted(ports):
        serialPortList.append({"serialPort": port, "verified": False})

    for serialPort in serialPortList:
        s = serial.Serial(serialPort["serialPort"], timeout=10)
        message = s.readline()
        print(message)
        if message == b'hello\n':
            serialPort["verified"] = True

    logging.debug(serialPortList)
    print(serialPortList)
