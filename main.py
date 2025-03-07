#!/usr/bin/python3

import serial.tools.list_ports
import threading
import logging
import serial
import os

# Log file config
logging.basicConfig(filename="test.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%d-%m-%Y | %H:%M:%S',
                    level=logging.DEBUG)
logging.info("Started log")


def printAndLog(text: str, level: str):
    # printAndLog fuction to help logging and print messages
    print(text)
    if level == "debug":
        logging.debug(text)
    elif level == "info":
        logging.info(text)
    elif level == "warning":
        logging.warning(text)
    elif level == "error":
        logging.error(text)
    elif level == "critical":
        logging.critical(text)


def readPort(port: str):
    printAndLog(f'Thread Reading {port}', "info")


def main():
    while True:
        # get a list of all serial ports
        ports = serial.tools.list_ports.comports()

        serialPortList = []

        for port, desc, hwid in sorted(ports):
            printAndLog(port, "debug")
            serialPortList.append(
                {"port": port, "verified": False, "inUse": False})

        # Loop through all serial ports and test if they are being used
        for serialPort in serialPortList:
            try:
                s = serial.Serial(serialPort["port"], timeout=10)
                message = s.readline()
                printAndLog(
                    f'Port: {serialPort["port"]}\n  message: {message}', "info")
                if message == b'olleh\n':
                    serialPort["verified"] = True
            except:
                serialPort["inUse"] = True
                printAndLog(
                    f'Serial Port {serialPort["port"]} cannot be read', "warning")

        printAndLog(serialPortList, "info")

        for serialPort in serialPortList:
            # if the port is not in use and contains the right message it begin to be read in a separate thread
            if serialPort["verified"] == True and not serialPort["inUse"]:
                t = threading.Thread(
                    target=readPort, args=(serialPort["port"],))
                t.start()
                printAndLog(
                    f'Verified serial port: {serialPort["port"]}', "info")


if __name__ == "__main__":
    main()
