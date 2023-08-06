from curses import wrapper

def main(window):
    key = '0'
    while key != 27:
        key = window.getch()
        print(key)

if __name__ == '__main__':
    wrapper(main)

