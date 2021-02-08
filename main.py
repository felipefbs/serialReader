import serial
import serial.tools.list_ports

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

print(serialPortList)
