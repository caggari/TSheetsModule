from TSheets_utils import TSheets
from datetime import datetime

myTSheets = TSheets('S.5__056427cf8cc35ee637bc87a1a395f80e96e4bb78')
current_date = datetime(2020, 3, 31)
myTSheets.save_csv_file(file_base_path='C:/Users/Christian Aggari/dockerFolder/scale-marketing/data', current_datetime=current_date)