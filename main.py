#!/usr/bin/python3

import serial
import serial.tools.list_ports
import logging
import os

logging.basicConfig(filename="test.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%d-%m-%Y | %H:%M:%S',
                    level=logging.DEBUG)
logging.info("Started log")


def main():
    while True:
        ports = serial.tools.list_ports.comports()

        serialPortList = []

        for port, desc, hwid in sorted(ports):
            print(port)
            serialPortList.append(
                {"port": port, "verified": False, "inUse": False})

        for serialPort in serialPortList:
            try:
                s = serial.Serial(serialPort["port"], timeout=10)
                message = s.readline()
                print(f'Port: {serialPort["port"]}\n  message: {message}')
                if message == b'olleh\n':
                    serialPort["verified"] = True
            except:
                serialPort["inUse"] = True
                print(
                    f'Serial Port {serialPort["port"]} cannot be read')

        print(serialPortList)

        for serialPort in serialPortList:
            if serialPort["verified"] == True and not serialPort["inUse"]:
                print(f'Serial Port: {serialPort["port"]}')
                # os.system(f'python3 serialReader.py {serialPort["port"]}')


if __name__ == "__main__":
    main()
