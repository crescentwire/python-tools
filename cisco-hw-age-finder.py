# Add the datetime library
from datetime import datetime, timedelta
import calendar
import re

today = datetime.today().strftime('%Y-%m-%d')

todays_date = datetime.today()#.strftime('%m/%d/%Y')

print(f'Today is {todays_date}.')

print()

# Ask for serial number input

sn = input("Enter the device's serial number (in format LLLYYWWSSSS): ")

# Try using a index slice operation to match digits instead of RegEx; string in use is LLLYYWWSSSS

sn_year = sn[3:5]  # Match positions 3 and 4 - "YY"
sn_week = sn[5:7]  # Match positions 5 and 6 - "WW"

# Next, we need to convert the year and week values to meaningful dates

sn_mfg_year = int(sn_year) + 1996  # 1996 corresponds to a year code of 00

# Remove leading zero for weeks < 10

if sn_week.startswith('0'):
    sn_week = sn_week[1]

# Inspect the relevant part of the serial number, assuming a format of FCW1950A4N4

if int(sn_week) in range(1, 6):
    sn_mfg_month = 'January'
elif int(sn_week) in range(6, 10):
    sn_mfg_month = 'February'
elif int(sn_week) in range(10, 15):
    sn_mfg_month = 'March'
elif int(sn_week) in range(15, 19):
    sn_mfg_month = 'April'
elif int(sn_week) in range(19, 23):
    sn_mfg_month = 'May'
elif int(sn_week) in range(23, 28):
    sn_mfg_month = 'June'
elif int(sn_week) in range(28, 32):
    sn_mfg_month = 'July'
elif int(sn_week) in range(32, 36):
    sn_mfg_month = 'August'
elif int(sn_week) in range(36, 41):
    sn_mfg_month = 'September'
elif int(sn_week) in range(41, 45):
    sn_mfg_month = 'October'
elif int(sn_week) in range(45, 49):
    sn_mfg_month = 'November'
elif int(sn_week) in range(49, 53):
    sn_mfg_month = 'December'
else:
    print('Invalid week number. Please check SN and run again.')

print(f'Device Manufacture Date: {sn_mfg_month} {sn_mfg_year}')

manf_date = f'{sn_mfg_month} 1 {sn_mfg_year}'

def time_elapsed(date_start, date_end):
    date_start = datetime.strptime(date_start, '%B %d %Y')
    date_end = datetime.strptime(date_end, '%Y-%m-%d')
    print(f'Age is {abs((date_end - date_start).days)} days.')

date_choice = input("Enter 1 to use today's date or 2 to enter a date (YYYY-MM-DD) ")

if date_choice == '1':
    time_elapsed(manf_date, today)
elif date_choice == '2':
    date_end = input('Enter your desired starting date in format YYYY-MM-DD: ')
    time_elapsed(manf_date, date_end)
else:
    print('Invalid entry. Please enter 1 or 2.')
