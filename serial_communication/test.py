import serial

ser = serial.Serial('COM4', 9600, timeout=1)
ser.reset_input_buffer()
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        if(line[0:3] == 'PPM'):
            ppm = float(line[6:])
            print(ppm)