from openpyxl import *

wb = load_workbook(r'C:\Users\WYQ\Desktop\04成本各科损益汇总表2\www\kcs423.xlsx')

ws = wb['kcs4233 (4)']

ca1 = ws['A1'].value

print(str(ca1))
