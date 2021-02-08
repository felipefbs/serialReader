import serial
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

serialPortList = []

for port, desc, hwid in sorted(ports):
    serialPortList.append({"serialPort": port, "verified": False})

print(serialPortList)
