# Cam serial communication speed test - By: @pvadam - Thu Aug 2 2018

import sensor, image, time
from pyb import LED, UART, USB_VCP

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

led_blue = LED(3)
led_green = LED(2)
usb = USB_VCP()

clock = time.clock()

uart = UART(1)
uart.init(1152000, bits=8, parity=None, stop=1, timeout=1000, flow=0, timeout_char=0, read_buf_len=64)

USE_USB_CONVERTER = True

def send(data):
    if USE_USB_CONVERTER:
        uart.write(data)
    else:
        usb.send(data)

i = 0
start_signal = '____start____'
end_signal = '____end____'
while(True):
    clock.tick()
    i += 1
    led_blue.on()
    img = sensor.snapshot()         # Take a picture and return the image.
    img_compressed = img.compress(quality=60)
    send(b'{0}save_image{1}'.format(start_signal, end_signal))
    send(start_signal)
    send(img_compressed)
    send(end_signal)
    led_blue.off()
