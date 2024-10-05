#!/usr/bin/env python

import tkinter as tk
import pytz
import random
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

main_city = os.getenv('MAIN_CITY')
main_tz = os.getenv('MAIN_TZ')

random_city_tz_list = [(os.getenv(f'CITY{i}'), os.getenv(f'TZ{i}')) for i in range(1, 53)]
random_city_tz_list.remove((main_city, main_tz))

clock_background_color = os.getenv('WINDOW_BG_COLOR', 'black')
city_font_family = os.getenv('CITY_FONT_FAMILY', 'Helvetica')
city_font_color = os.getenv('CITY_FONT_COLOR', 'white')

date_font_family = os.getenv('DATE_FONT_FAMILY', 'Helvetica')
date_font_size = os.getenv('DATE_FONT_SIZE', 60)
date_font_color = os.getenv('DATE_FONT_COLOR', 'white')

clock_font_family = os.getenv('CLOCK_FONT_FAMILY', 'Helvetica')
clock_font_color = os.getenv('CLOCK_FONT_COLOR', 'white')

main_city_font_size = os.getenv('MAIN_CITY_FONT_SIZE', 200)
main_clock_font_size = os.getenv('MAIN_CLOCK_FONT_SIZE', 200)
main_clock_format = os.getenv('MAIN_CLOCK_FORMAT', '%H:%M:%S')

lower_city_font_size = os.getenv('LOWER_CITY_FONT_SIZE', 100)
lower_clock_font_size = os.getenv('LOWER_CLOCK_FONT_SIZE', 100)
lower_clock_format = os.getenv('LOWER_CLOCK_FORMAT', '%H:%M:%S')

inner_padding = 10
lower_clock_update_milliseconds = os.getenv('LOWER_CLOCKS_UPDATE_EVERY_X_MILLISECONDS', 60000)

date_format = os.getenv('DATE_FORMAT', "%A, %B %d, %Y")  # Ex: "Friday, October 04, 2024"

root = tk.Tk()
root.attributes('-fullscreen', os.getenv('FULLSCREEN', False))
root.geometry(os.getenv('WINDOW_SIZE', '1024x768'))
root.configure(bg=os.getenv('WINDOW_BG_COLOR', 'black'))


def get_time_in_timezone(timezone_str, time_format_str):
    tz = pytz.timezone(timezone_str)
    time_now = datetime.now(tz)
    return time_now.strftime(time_format_str)


def get_date_in_timezone(timezone_str, dateformat_str):
    tz = pytz.timezone(timezone_str)
    date_now = datetime.now(tz)
    return date_now.strftime(dateformat_str)


class ClockFrame:
    def __init__(self, parent, city, tz, row, col, colspan, city_font_family, city_font_size, city_font_color,
                 date_font_family,
                 date_font_size, date_font_color, clock_font_family, clock_font_size, clock_font_color, clock_format,
                 show_date=False):
        self.city = city
        self.tz = tz
        self.city_font_family = city_font_family
        self.city_font_size = city_font_size
        self.city_font_color = city_font_color
        self.date_font_family = date_font_family
        self.date_font_size = date_font_size
        self.date_font_color = date_font_color
        self.clock_font_family = clock_font_family
        self.clock_font_size = clock_font_size
        self.clock_font_color = clock_font_color
        self.clock_format = clock_format
        self.show_date = show_date

        self.frame = tk.Frame(parent, bg='black', padx=inner_padding, pady=inner_padding)
        self.frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew")

        self.city_label = tk.Label(self.frame, text=self.city.replace("_", " "),
                                   font=(self.city_font_family, self.city_font_size, 'bold'),
                                   fg=self.city_font_color, bg='black')
        self.city_label.pack(pady=inner_padding)

        if self.show_date:
            self.date_label = tk.Label(self.frame, font=(date_font_family, date_font_size), fg=date_font_color,
                                       bg='black')
            self.date_label.pack(pady=inner_padding)
            self.update_date()

        self.time_label = tk.Label(self.frame, font=(clock_font_family, self.clock_font_size), fg=clock_font_color,
                                   bg='black')
        self.time_label.pack(pady=inner_padding)

        self.update_time()

    def update_time(self):
        current_time = get_time_in_timezone(self.tz, self.clock_format)
        self.time_label.config(text=current_time)
        self.time_label.after(1000, self.update_time)  # Update clock every second

    def update_date(self):
        current_date = get_date_in_timezone(self.tz, date_format)
        self.date_label.config(text=current_date)

    def update_city_and_timezone(self, new_city, new_tz):
        self.city = new_city.replace("_", " ")
        self.tz = new_tz
        self.city_label.config(text=self.city)


def update_lower_clocks(lower_clocks):
    def refresh_clocks():
        available_city_tz = random_city_tz_list[:]

        for clock_frame in lower_clocks:
            city, tz = random.choice(available_city_tz)
            available_city_tz.remove((city, tz))
            clock_frame.update_city_and_timezone(city, tz)

        root.after(lower_clock_update_milliseconds, refresh_clocks)

    refresh_clocks()


root.grid_rowconfigure(0, weight=2)  # Upper clock 2/3 of height
root.grid_rowconfigure(1, weight=1)  # Lower clocks 1/3 of height
for i in range(4):
    root.grid_columnconfigure(i, weight=1)  # Lower clocks 4 equal columns

upper_frame = ClockFrame(root, main_city, main_tz, 0, 0, 4, city_font_family, main_city_font_size, city_font_color,
                         date_font_family, date_font_size, date_font_color, clock_font_family, main_clock_font_size,
                         clock_font_color, main_clock_format, show_date=True)

available_city_tz = random_city_tz_list[:]
lower_clocks = []
for i in range(4):
    lower_city, lower_tz = random.choice(available_city_tz)
    available_city_tz.remove((lower_city, lower_tz))
    lower_clocks.append(
        ClockFrame(root, lower_city, lower_tz, 1, i, 1, lower_city_font_size, lower_city_font_size, city_font_color,
                   date_font_family, date_font_size, date_font_color, clock_font_family, lower_clock_font_size,
                   clock_font_color, lower_clock_format, show_date=False))

update_lower_clocks(lower_clocks)

root.bind('<Escape>', lambda e: root.destroy())

root.mainloop()
