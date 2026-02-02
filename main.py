import time
from mesh import bot, interface

def main():
    print("Bot running...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        interface.close()

if __name__ == "__main__":
    main()
