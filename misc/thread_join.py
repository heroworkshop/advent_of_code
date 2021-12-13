from threading import Thread
from time import sleep


def main():

    delay = 0.5
    def counter():
        n = 10
        while n:
            print(n)
            sleep(delay)
            n -= 1

    t = Thread(target=counter, daemon=True)
    t.start()
    t.join(1.5)
    if t.is_alive():
        print("thread was alive")


if __name__ == "__main__":
    main()
