from machine import UART, Pin, ADC
from time import sleep

uart0 = UART(0, 9600)
uart0.init(baudrate=9600, bits=8, parity=None, stop=1, tx=0, rx=1)
moisture_read = ADC(27)
read_moisture_switch = Pin(26, mode=Pin.OUT)
on_off_switch = Pin(20, mode=Pin.IN, pull=Pin.PULL_UP)
on_off_status = True

def main():
    while True:
        moisture_raw = moisture_read.read_u16()
        moisture_print = str(moisture_raw)
        uart0.write('moisture raw reading:' + moisture_print +'\r\n')
        uart0.write('on_off_status:' + str(on_off_status) +'\r\n')
        sleep(1)

def moisture_control_switch(pin):
    global on_off_status
    on_off_status = not on_off_status
    if on_off_status==True:
        read_moisture_switch.low()
    elif on_off_status==False:
        read_moisture_switch.high()

on_off_switch.irq(moisture_control_switch, trigger=on_off_switch.IRQ_FALLING)

if __name__ == '__main__':
    main()

''' 
    Pin reference & note
    maker port 1:           Gnd, 3v3, gp26(ao), gp27(a1)
    maker moisture sensor:  Gnd, Vcc, Dis(High = disable), Output
    moisture read range: 30k-42k
'''