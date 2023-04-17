import sys, os
import curses
from serial import Serial
from auxfunc import *
from time import sleep

def draw_menu(stdscr):

    view: int = 1
    stdscr = curses.initscr()
    
    try:
        data_stream: Serial = Serial("/dev/ttyUSB0")
        data_stream.baudrate = 115200
    except:
        return -1

    # Non blocking getch
    stdscr.nodelay(True)
    c: int = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    counter = 0
    while True:
        counter = round(counter + 0.2, 2)
        data_line: str = str(data_stream.readline()).strip() 
        # data_line: str = f",3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3@,{counter},{counter}@,B,B,B,N,B,B,B,N,B,N,B,B,B,B,B,B,N,B,B,B,B,B,B,B"
        data: list[str] = data_line.split("@")
        voltages = filter_serial_data(data[0])
        internal_temp = filter_serial_data(data[1])
        balancing = filter_serial_data(data[2])

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Declaration of strings
        title = "Battery GUI"

        # Centering calculations
        start_x_title = center_text(title, width)
        start_y = 1

        set_color(stdscr, BLACK)
        print_status_bar(stdscr)
        unset_color(stdscr, BLACK)

        # Turning on attributes for title
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(start_y, start_x_title, title)
        stdscr.attroff(curses.A_BOLD)

        print_cell_voltages(stdscr, voltages, balancing)
        print_adc_temperatures(stdscr, internal_temp)
            

        view = get_user_char(stdscr, view)

        sleep(0.1)
        stdscr.refresh()
def main():
    error = curses.wrapper(draw_menu)

    if error == -1:
        print("\nNo UART port detected.\t Check connections! \n")

if __name__ == "__main__":
    main()

