import random
import time

x = 6000000000000  # this is a variable
lol = True


def main():
    '''
    This is the main function.
    '''
    hello = "hello"
    if x < 10000000000000:
        time.sleep(random.randint(1, 3))
        print(hello + " world!")

    if lol:
        print("lol")


if __name__ == '__main__':
    main()
