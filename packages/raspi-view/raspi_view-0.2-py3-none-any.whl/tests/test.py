from gpiozero import LED, Button
from signal import pause

def pushed():
    print("pushed")

def init():
    button1 = Button(21)
    button2 = Button(5)
    button1.when_activated = pushed 
    button2.when_activated = pushed 

    led1 = LED(12)
    led2 = LED(6)


    led1.on()
    led2.on()

    pause()

if __name__ == "__main__":
    init()
