from machine import Pin, PWM
import time

r = PWM(Pin(15))
g = PWM(Pin(14))
b = PWM(Pin(13))

r.freq(1000)
g.freq(1000)
b.freq(1000)

def set_color(red, green, blue):
    r.duty_u16(red * 257)
    g.duty_u16(green * 257)
    b.duty_u16(blue * 257)

def off():
    set_color(0, 0, 0)

while True:
    print("red")
    set_color(255, 0, 0)
    time.sleep(1)

    print("green")
    set_color(0, 255, 0)
    time.sleep(1)

    print("blue")
    set_color(0, 0, 255)
    time.sleep(1)

    print("off")
    off()
    time.sleep(1)
