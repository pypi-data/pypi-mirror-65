#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Update Aoki shortwave frequency database.

Shortwave broadcast are identified using a 3 character code
that refers to the summer season (abbreviated as 'A') and
the winter season (abbreviated as 'B') and a 2 digit year.
For example schedule B19 refers to the Winter 2019/2020 schedule.

Updates the frequency table with the latest data file.
1. Convert the fixed width file to CSV format.
2. Import the CSV into the database
3. Update the frequency table and the schedule table

If a ``tkinter`` related error occurs, the Tcl/Tk (python3-tk)
graphical user interface toolkit might not be installed on the system.
Refer to https://tkdocs.com/tutorial/install.html for guidance.

Aoki frequency database:
http://www1.s2.starcat.ne.jp/ndxc/

"""

# standard library modules
import os
import sys
import csv
import re
import sqlite3
import itertools
import calendar
import datetime

# system modules
import tkinter as tk
from tkinter import filedialog, simpledialog

# local modules
from swtools.database import Database

DATABASE = os.path.join(os.path.dirname(__file__), 'data/shortwave.sqlite3')


def main():
    """Main entry point."""

    # prompt for an update file (returns dict)
    info = get_file()

    # start update process
    print('\n--> \033[93mSWTools Frequency Database\033[0m update process started')

    # parse fixed-width into proper csv
    print('... Parsing and formatting file into CSV')
    parse_file(info['read'], info['write'])

    # import data
    print('... Importing CSV file into database')
    import_file(info['write'])

    # update tables
    print('... Updating the frequency table')
    update_data(info['schedule'], info['season'])

    # if we get here it worked!
    print(':-) Update process completed!\n')


def parse_file(read, write):
    """Parse and convert the fixed width file to CSV format."""

    file_to_read = None
    file_to_write = None

    # column headers
    header = 'FREQ|STATION|UTC|DOW|LANG|POWER|AZIMUTH|LOCATION|ADM|GEO|REMARKS\n'

    # a tuple-of-tuples (!) with column starting locations and lengths
    ranges = ((0, 5), (6, 32), (38, 9), (48, 7), (56, 19), (76, 4), (81, 3), (85, 21), (107, 3), (111, 15), (127, 21))

    try:
        file_to_read = open(read, 'r', encoding='ISO-8859-1')
        file_to_write = open(write, 'w', encoding='ISO-8859-1')
        file_to_write.write(header)
        for line in itertools.islice(file_to_read, 2, None):  # start=2, stop=None
            parts = []
            for rng in ranges:
                parts.append(line[rng[0]:rng[0] + rng[1]].strip())
            file_to_write.write('|'.join(parts) + '\n')
        print('... File parsed and converted')
    except IOError as error:  # handle IO errors
        print(':-( \033[31mParsing error\033[0m\n', error)
        sys.exit(1)
    except Exception as e:  # handle other exceptions such as attribute errors
        print('Unexpected error parsing file:', e)
        sys.exit(1)
    finally:
        file_to_read.close()
        file_to_write.close()


def update_data(schedule, season):
    """Update data using SQL script file.

    This will execute several statements:
    1. Reset frequency table
    2. Reset frequency table sequence
    3. Copy imported data into the frequeny table
    4. Update the time columns to fix the day crossover lookup gap issue
    5. Update the schedule info
    """
    conn = None
    sqlfile = os.path.join(os.path.dirname(__file__), 'swupdate.sql')
    try:
        db = Database(DATABASE)
        with open(sqlfile) as sqlscript:
            db.cursor.executescript(sqlscript.read().format(schedule, season))
        db.conn.commit()
        db.close()
    except sqlite3.Error as error:
        print(':-( \033[31mSQLite error:\033[0m', error)
        sys.exit(1)
    finally:
        if conn:
            db.close()


def import_file(csv_file):
    """Import into database.

    Data is imported into a temp table first.
    """

    # initialize connection variable
    conn = None

    # try to import the CSV file into the database
    try:

        # connect to database
        # conn = sqlite3.connect(DATABASE)

        # create a cursor
        # cursor = conn.cursor()
        db = Database(DATABASE)

        # reset temp table first
        db.cursor.execute("DELETE from aoki_temp;")
        db.conn.commit()

        # field mapping for DictReader
        fields = (
            'frequency',
            'station',
            'broadcast_time',
            'days_of_operation',
            'language',
            'transmitter_power',
            'transmitter_azimuth',
            'transmitter_location',
            'transmitter_adm',
            'geocoordinates',
            'remarks'
        )

        # sql for database insert
        sql_statement = '''
        INSERT INTO aoki_temp (
            frequency,
            station,
            broadcast_time,
            days_of_operation,
            language,
            transmitter_power,
            transmitter_azimuth,
            transmitter_location,
            transmitter_adm,
            geocoordinates,
            remarks
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''

        # open the csv file and read the data into the DictReader
        with open(csv_file, 'r', encoding='ISO-8859-1') as f:
            reader = csv.DictReader(f, fieldnames=fields, delimiter='|')
            next(f)  # ignore headers
            to_db = [(
                i['frequency'],
                i['station'],
                i['broadcast_time'],
                i['days_of_operation'],
                i['language'],
                i['transmitter_power'],
                i['transmitter_azimuth'],
                i['transmitter_location'],
                i['transmitter_adm'],
                i['geocoordinates'],
                i['remarks']
            ) for i in reader]

        # execute the insert statements
        db.cursor.executemany(sql_statement, to_db)

        # commit the transactions
        db.conn.commit()
        print('...', db.cursor.rowcount, 'records imported')

        # close the cursor
        db.close()

    # catch SQLite errors
    except sqlite3.Error as error:
        print(':-( \033[31mSQLite error:\033[0m', error)
        sys.exit(1)

    # close the connection
    finally:
        if conn:
            db.close()


def get_file():
    """Prompt to pick a file for update.

    The Aoki file is a simple fixed width text file
    that uses a specific naming convention.
    """

    # create a tkinter root window
    application_window = tk.Tk()

    application_window.geometry('300x200-5+40')

    # hide the root window so we only show dialogs
    application_window.withdraw()

    # prompt string
    prompt = """
    Shortwave broadcast schedules are identified using a 3 character
    code that refers to the summer season (abbreviated as 'A') or
    the winter season (abbreviated as 'B') plus a 2 digit year.
    For example schedule B19 refers to the Winter 2019/2020 schedule.\n
    Please specify the schedule identifier below?\n"""

    while True:
        # prompt the user for the schedule indentifier
        schedule = simpledialog.askstring(
            title='SWTools Shortwave Frequency Updater',
            prompt=prompt,
            initialvalue=get_default(),
            parent=application_window
        )

        # the user clicked cancel or closed the dialog
        if not schedule:
            print(':-| Update Cancelled!\n')
            sys.exit(0)

        # validate the identifier
        p = re.compile(r'[ab]\d{2}', re.MULTILINE | re.IGNORECASE)
        m = p.match(schedule)

        # continue if valid
        if m:
            # print('Match found: ', m.group())
            break

    # build schedule information  B19 (Winter 2019/2020)
    year1 = int(''.join(filter(str.isdigit, schedule)))
    year2 = year1 + 1
    schedule_name = schedule.upper()
    if 'A' in schedule_name:
        schedule_season = schedule_name + ' (Summer 20' + str(year1) + ')'
    else:
        schedule_season = schedule_name + ' (Winter 20' + str(year1) + '/20' + str(year2) + ')'

    # allowed file types
    file_types = [('text files', '.txt')]

    # create a standard open file dialog to pick the Aoki update file
    answer = filedialog.askopenfilename(
        parent=application_window,
        initialdir=os.getcwd(),
        title='Please select Aoki update file:',
        filetypes=file_types
    )

    # the user clicked cancel or closed the dialog
    if not answer:
        print(':-| Update Cancelled!\n')
        sys.exit(0)

    # the user picked a file
    # TODO: how can we validate the file name at least
    data = {}
    data['path'] = os.path.dirname(os.path.realpath(answer))
    data['name'] = os.path.basename(os.path.realpath(answer))
    data['read'] = answer
    data['write'] = answer.replace('.txt', '.csv')
    data['schedule'] = schedule_name
    data['season'] = schedule_season

    # return dictionary
    return data


def get_default():
    """Get default schedule identifier.

    Based on current date.
    """
    now = datetime.datetime.now()
    # now = datetime.datetime(2019, 11, 1)
    yr = now.year
    mo = now.month

    # Summer season starts on the last Sunday in
    # March and ends on the last Sunday in October
    sunday = max(week[-1] for week in calendar.monthcalendar(yr, 3))
    summer = datetime.datetime(yr, 3, sunday)

    # Winter season starts on the last Sunday in
    # October and ends on the last Sunday in March
    sunday = max(week[-1] for week in calendar.monthcalendar(yr, 10))
    winter = datetime.datetime(yr, 10, sunday)

    # compare
    isSummer = now > summer and now < winter
    isWinter = not(isSummer)
    if isSummer:
        schedule = 'A' + str(yr)[2:]
    elif isWinter and mo in [1, 2, 3]:
        schedule = 'B' + str(yr - 1)[2:]
    elif isWinter and mo in [11, 12]:
        schedule = 'B' + str(yr)[2:]
    else:
        schedule = None

    return schedule


if __name__ == '__main__':
    main()
