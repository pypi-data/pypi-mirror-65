import os
import xlwt
from ntc_templates.parse import parse_output


current_directory = os.path.dirname(os.path.realpath(__file__))
files = os.listdir(current_directory)

wb = xlwt.Workbook()
ws = wb.add_sheet('Summary')

count_row = 0
for i in files:
	try:

		#open file
		read_file = open(i,'r')
		#melakukan read/baca terhadap file
		data = (read_file.read())
		#function nya si ntc_templates, parse_ouput
		parsed_file = parse_output(platform = 'cisco_ios', command = 'show ver', data=data)
		#print(parsed_file)

		#len_file = len(parsed_file)
		#print(len_file)

		list_file = parsed_file[0]
		#print(list_file)

		dic_file_ver = list_file['version']


		dic_file_hw = list_file['hardware']
		file_hw = dic_file_hw[0]
		print(str(count_row)+' '+dic_file_ver+' '+file_hw)
		
		#file name
		ws.write(count_row, 0, i)
		#version
		ws.write(count_row, 1, dic_file_ver)
		#hardware
		ws.write(count_row, 2, file_hw)



	except:
		#file name
		ws.write(count_row, 0, i)
		#version
		ws.write(count_row, 1, 'None')
		#hardware
		ws.write(count_row, 2, 'None')
	count_row+=1

wb.save('result.xls')