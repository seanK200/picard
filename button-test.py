import gpiozero as gpio

KEY_1 = 18
KEY_2 = 23
KEY_3 = 24
KEY_4 = 25


def get_handler(event, id):
    def handler():
        print(str(id) + " " + event)
    return handler


def main():
    b1 = gpio.Button(KEY_1)
    b2 = gpio.Button(KEY_2)
    b3 = gpio.Button(KEY_3)
    b4 = gpio.Button(KEY_4)
    b1.when_pressed = get_handler("PRESS", 1)
    b1.when_released = get_handler("RELEASE", 1)
    b2.when_pressed = get_handler("PRESS", 2)
    b2.when_released = get_handler("RELEASE", 2)
    b3.when_pressed = get_handler("PRESS", 3)
    b3.when_released = get_handler("RELEASE", 3)
    b4.when_pressed = get_handler("PRESS", 4)
    b4.when_released = get_handler("RELEASE", 4)

    print("Press 1:")
    b1.wait_for_press()
    
    print("Press 2:")
    b2.wait_for_press()

    print("Press 3:")
    b3.wait_for_press()

    print("Press 4:")
    b4.wait_for_press()

main()
