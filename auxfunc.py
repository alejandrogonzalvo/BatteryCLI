from time import sleep
import curses

CYAN = 1
RED = 2
BLACK = 3
WHITE = 4
YELLOW = 5

def filter_serial_data(data: list[str]) -> list[str]:
    return data.split(",")[1:]

def center_text(text: str, width: int) -> int:
    return (width // 2) - (len(text) // 2) - len(text) % 2

def get_battery_number(i: int) -> int:
    return i // 6 +1

def get_cell_number(i: int) -> int:
    return (i%6) + 1

def get_adc_number(i: int) -> int:
    return i // 12

def print_cell_voltages(stdscr, voltages: list[str], balancing: list[str]):
    height, width = stdscr.getmaxyx()
    marginx: int = width // 20
    marginy: int = height // 15
    
    x: int = 0
    y: int = 0 
    for i in range(len(voltages)):
        battery: int = get_battery_number(i)
        cell: int = get_cell_number(i)

        battery_cell_str: str = f"cell{cell} "
        cell_balancing_str: str = f"{balancing[i]} " 
        cell_value_str: str = f"{voltages[i]} V"
        
        if i % 12 == 0 and i != 0:
            x += len(battery_cell_str + cell_balancing_str + cell_value_str) + 4
            y = 0

        elif i%6 == 0 and i != 0:
            y += 2
        
        x_start: int = marginx + x
        y_start: int = marginy + y

        if i % 12 == 0:
            stdscr.addstr(y_start, x_start, f"Battery {battery}")
            y_start += 2
            y += 2

        elif i%6 == 0:
            stdscr.addstr(y_start, x_start, f"Battery {battery}")
            y_start += 2
            y += 2

        stdscr.addstr(y_start, x_start, battery_cell_str)
        if (balancing[i] == "B"):
            stdscr.attron(curses.A_BOLD)
            set_color(stdscr, YELLOW)
            stdscr.addstr(y_start, x_start + len(battery_cell_str), cell_balancing_str)
            unset_color(stdscr, YELLOW)
            stdscr.attroff(curses.A_BOLD)
        else:
            stdscr.addstr(y_start, x_start + len(battery_cell_str), cell_balancing_str)
        
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(y_start, x_start+len(battery_cell_str+cell_balancing_str), cell_value_str)
        stdscr.attroff(curses.A_BOLD)


        y += 1

def set_color(stdscr, color: int):
    stdscr.attron(curses.color_pair(color))
def unset_color(stdscr, color: int):
    stdscr.attroff(curses.color_pair(color)) 

def print_adc_temperatures(stdscr, internal_temp: list[str]):
    height, width = stdscr.getmaxyx()
    marginx: int = width // 20
    marginy: int = height // 15
    
    y: int = height // 2
    x: int = 0
    for i in range(len(internal_temp)):
        x_start = marginx + x
        y_start = marginy + y
        
        adc_number_str: str = f"ADC{i+1} "
        adc_temperature_str: str = f"{internal_temp[i]} °C"

        stdscr.addstr(y_start, x_start, adc_number_str)

        if (float(internal_temp[i]) > 60):
            set_color(stdscr, RED)
        elif (float(internal_temp[i]) > 40):
            set_color(stdscr, YELLOW)
        
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(y_start, x_start+len(adc_number_str), adc_temperature_str)
        stdscr.attroff(curses.A_BOLD)

        if (float(internal_temp[i]) > 60):
            unset_color(stdscr, RED)
        elif (float(internal_temp[i]) > 40):
            unset_color(stdscr, YELLOW)

        x += len(adc_temperature_str+adc_temperature_str) + 4

def print_status_bar(stdscr):
    height, width = stdscr.getmaxyx()
    
    statusbarstr = "Press 'q' to exit"
    stdscr.addstr(height-1, 0, statusbarstr)
    stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))

def get_user_char(stdscr, view: int) -> tuple[int, str]:
    c: int = stdscr.getch()

    if c == -1: # No key pressed
        pass
    else:
        c = chr(c)
    
        if c == '1':
            view = 1
        
        elif c == '2':
            view = 2
        
        elif c == 'q':
            exit(0)

        else:
            pass # Wrong key pressed

    return view

