import datetime
import re


def valid_link(url):
   re_equ = r"((https:\/\/)(www\.)?github\.com\/.*)"
   ck_url = re.findall(re_equ, url)
   if ck_url:
      return True
   else:
      return False

def valid_date(date):
   re_date = r"((0[1-9]|1[0-2])[\/](0[1-9]|[12][0-9]|3[01])[\/](\d{4})$)"
   rs_date = re.findall(re_date,date)
   if(rs_date):
      ls = rs_date[0][0].split("/")
      is_correct = None
      try:
         newDate = datetime.datetime(int(ls[2]),int(ls[0]),int(ls[1]))
         is_correct = True
         print(newDate)
      except ValueError:
         is_correct = False
      return is_correct
   return False
