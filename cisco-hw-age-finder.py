# This is a work in progress and not complete!

# Add the datetime library
from datetime import datetime, timedelta
import calendar
import re
  
date_cur = datetime.now()
  
year_cur = date_cur.year
month_cur = date_cur.month
day_cur = date_cur.day
  
print(f'Today is {date_cur.month}/{date_cur.day}/{date_cur.year}')
  
print()
  
# Ask for serial number input
  
sn = input("Enter the device's serial number (in format LLLYYWWSSSS): ")
  
# Try using a index slice operation to match digits instead of RegEx; string in use is LLLYYWWSSSS
  
sn_year = sn[3:5] # Match positions 3 and 4 - "YY"
sn_week = sn[5:7] # Match positions 5 and 6 - "WW"
  
# Next, we need to convert the year and week values to meaningful dates
  
sn_mfg_year = int(sn_year) + 1996 # 1996 corresponds to a year code of 00
  
# ? What if we use a dictionary to assign the manufacture month?
  
sn_mfg_month_dict = {1-6:'January',6-10:'February',10-15:'March',15-19:'April',19-23:'May',23-28:'June',28-32:'July',32-36:'August',36-41:'September',41-45:'October',45-49:'November',49-53:'December'}
  
for sn_week in sn_mfg_month_dict:
    sn_mfg_month = sn_mfg_month_dict
    print()

# Inspect the relevant part of the serial number, assuming a format of FCW1950A4N4
  
if int(sn_week) in range(1,6):
    sn_mfg_month = 'January'
  
elif int(sn_week) in range(6,10):
    sn_mfg_month = 'February'
  
elif int(sn_week) in range(10,15):
    sn_mfg_month = 'March'
  
elif int(sn_week) in range(15,19):
    sn_mfg_month = 'April'
  
elif int(sn_week) in range(19,23):
    sn_mfg_month = 'May'
  
elif int(sn_week) in range(23,28):
    sn_mfg_month = 'June'
  
elif int(sn_week) in range(28,32):
    sn_mfg_month = 'July'
  
elif int(sn_week) in range(32,36):
    sn_mfg_month = 'August'
  
elif int(sn_week) in range(36,41):
    sn_mfg_month = 'September'
  
elif int(sn_week) in range(41,45):
    sn_mfg_month = 'October'
  
elif int(sn_week) in range(45,49):
    sn_mfg_month = 'November'
  
elif int(sn_week) in range(49,53):
    sn_mfg_month = 'December'
  
else:
    print('Invalid week number. Please check SN and run again.')
  
print('Device Manufacture Date: ' + str(sn_mfg_month) + ' ' + str(sn_mfg_year))
  
date_choice = input("Enter 1 to use today's date or 2 to enter a date (YYYY-MM-DD) ")
