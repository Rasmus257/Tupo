import random
import time

x = 6  # this is a variable


def main():
    '''
    This is the main function.
    '''
    hello = "hello"
    if x < 10:
        time.sleep(random.randint(1, 3))
        print(hello + " world!")


if __name__ == '__main__':
    main()
