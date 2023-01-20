import network
import socket
import time
from machine import Pin, PWM


class DCMotor:
    def __init__(self, pin1, pin2, enable_pin1, min_duty=750, max_duty=1023):
        self.pin1 = pin1 
        self.pin2 = pin2 
        self.enable_pin1 = enable_pin1
        self.min_duty = min_duty
        self.max_duty = max_duty

    def forward(self, speed):
        self.speed = speed
        self.enable_pin1.duty(self.duty_cycle(self.speed))
        self.pin1.value(1)
        self.pin2.value(0)

    def backwards(self, speed):
        self.speed = speed
        self.enable_pin1.duty(self.duty_cycle(self.speed))
        self.pin1.value(0)
        self.pin2.value(1)

    def stop(self):
        self.enable_pin1.duty(0)
        self.pin1.value(0)
        self.pin2.value(0)

    def duty_cycle(self, speed):
        if self.speed <= 0 or self.speed > 100:
            duty_cycle = 0
        else:
            duty_cycle = int(self.min_duty + (self.max_duty - self.min_duty) * ((self.speed - 1) / (100 - 1)))
            return duty_cycle


frequency = 1000
pin1 = Pin(5, Pin.OUT)
pin2 = Pin(4, Pin.OUT)
enable1 = PWM(Pin(0), frequency)
pin3 = Pin(14, Pin.OUT)
pin4 = Pin(12, Pin.OUT)
enable2 = PWM(Pin(13), frequency)
dc_motor1 = DCMotor(pin1, pin2, enable1)
dc_motor1 = DCMotor(pin1, pin2, enable1, 350, 1023)
dc_motor2 = DCMotor(pin3, pin4, enable2)
dc_motor2 = DCMotor(pin3, pin4, enable2, 350, 1023)


port = 20001
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Ssid", "password")

while (wlan.isconnected() == False):
    time.sleep(1)

ip = wlan.ifconfig()[0]
print(ip)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((ip, port))

print('waiting....')

while True:
    data, addr = s.recvfrom(1024)
    data = str(data, 'UTF-8')  # decode et
    print('received:', data, 'from', addr)
    s.sendto(data, addr)

    if (data == 'Center' or data== 'Empty Package'):
        dc_motor1.stop()
        dc_motor2.stop()
    if (data == 'Up'):
        dc_motor1.forward(100)
        dc_motor2.forward(100)
    if (data == 'Down'):
        dc_motor1.backwards(100)
        dc_motor2.backwards(100)
    if(data == 'Right'):
        dc_motor2.forward(50)
        dc_motor1.backwards(50)
    if (data == 'Left' ):
        dc_motor1.forward(50)
        dc_motor2.backwards(50)

    time.sleep(0.01)




