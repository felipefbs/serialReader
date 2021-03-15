#!/usr/bin/python3

'''
@file       at86rf215-ping-pong.py
@author     Pere Tuset-Peiro  (peretuset@openmote.com) modified by felipefbs
@version    v0.1
@date       February, 2019
@brief      

@copyright  Copyright 2019, OpenMote Technologies, S.L.
            This file is licensed under the GNU General Public License v2.
'''
import os
import sys

pwd = os.getcwd()
pwd = os.path.join(pwd, 'openmote-py')
if pwd not in sys.path:
    sys.path.insert(0, pwd)

from struct import unpack
import argparse
import influxdb
import logging
import signal

import Serial

finished = False

timeout = 0.1


def signal_handler(sig, frame):
    global finished
    finished = True


def program(dbClient, port=None, baudrate=None):
    global finished

    # Create and start Serial manager

    serial = Serial.Serial(name=port, baudrate=baudrate, timeout=timeout)
    serial.start()

    print("Starting program at port {} with bauds {}.".format(port, baudrate))

    # Repeat until finish condition
    while not finished:
        # Try to receive a Serial message

        message, length = serial.receive(timeout=timeout)
        statistics = serial.get_statistics()

        # If we received a message
        if (length > 0):
            
            message = bytearray(bytes(message))
            _, deviceID, counter, txMode, txCounter, csmaRetries, csmaRSSI, _, rssi, _ = unpack(
                ">c6sIBBBb17sbc", message)

            data = [
                {
                    "measurement": "transmissionData",
                    "tags": {
                        "deviceID": chr(deviceID[0])
                    },
                    "fields":{
                        "counter":     counter,
                        "txMode":      txMode,
                        "txCounter":   txCounter,
                        "csmaRetries": csmaRetries,
                        "csmaRSSI":    csmaRSSI,
                        "rssi":        rssi
                    }

                },
                {
                    "measurement": "serialStatistic",
                    "tags": {
                        "deviceID": chr(deviceID[0])
                    },
                    "fields":{
                        "rx_bad_frames":   statistics["rx_bad_frames"],
                        "rx_good_frames":  statistics["rx_good_frames"],
                        "rx_total_frames": statistics["rx_total_frames"],
                    }

                }
            ]

            print(f'deviceID: {chr(deviceID[0])}, counter: {counter}, txMode: {txMode}, txCounter: {txCounter}, csmaRetries: {csmaRetries}, csmaRSSI: {csmaRSSI}, rssi: {rssi}\n\tRX bad {statistics["rx_bad_frames"]}, RX good {statistics["rx_good_frames"]}, RX total {statistics["rx_total_frames"]}')

            try:
                # Write data into Influxdb
                # dbClient.write_points(data)
                pass

            except Exception as e:
                logging.error(e)

    if finished:
        # Stop the serial port
        serial.stop()

        # Close db connection
        dbClient.close()


def main():
    # Set-up logging back-end
    logging.basicConfig(filename="log",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%d-%m-%Y|%H:%M:%S',
                        level=logging.DEBUG)

    # Set up SIGINT signal
    signal.signal(signal.SIGINT, signal_handler)

    # Create argument parser
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-p", "--port", type=str, required=True)
    parser.add_argument("-b", "--baudrate", type=int, default=115200)

    # Parse arguments
    args = parser.parse_args()

    # Create InfluxDB client
    clientTest = influxdb.InfluxDBClient(host='127.0.0.1', port=8086, database='openmoteTest')

    # Execute program
    program(clientTest, port=args.port, baudrate=args.baudrate)


if __name__ == "__main__":
    main()
