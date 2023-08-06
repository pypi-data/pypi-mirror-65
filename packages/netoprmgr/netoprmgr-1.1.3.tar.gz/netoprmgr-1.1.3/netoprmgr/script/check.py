import os

from netmiko import Netmiko
import xlrd
import xlsxwriter
import shutil

def function_check(data_dir,capture_path):

    book = xlrd.open_workbook(data_dir)
    first_sheet = book.sheet_by_index(0)
    cell = first_sheet.cell(0,0)

    wb = xlsxwriter.Workbook('device_availability_check.xlsx')
    ws = wb.add_worksheet('summary')
    ws.write(0,0,'Host')
    ws.write(0,1,'Status')
    ws.write(0,2,'Authentication')
    count_row=1
    for i in range(first_sheet.nrows):
        host=first_sheet.row_values(i)[1]
        my_device = {
            "host": first_sheet.row_values(i)[1],
            "username": first_sheet.row_values(i)[2],
            "password": first_sheet.row_values(i)[3],
            "device_type": first_sheet.row_values(i)[4],
        }
        response = os.system("ping -n 1 " + host)
    
        if response == 0:
            ws.write(count_row,0,host)
            ws.write(count_row,1,'Up')
            try:
                net_connect = Netmiko(**my_device)
                ws.write(count_row,2,'Valid')
            except:
                ws.write(count_row,2,'Not Valid')
        else:
            print (host, 'is down')
            ws.write(count_row,0,host)
            ws.write(count_row,1,'Down')
            ws.write(count_row,2,'-')
        count_row+=1
    wb.close()

'''
    for i in range(first_sheet.nrows):
        my_device = {
            "host": first_sheet.row_values(i)[1],
            "username": first_sheet.row_values(i)[2],
            "password": first_sheet.row_values(i)[3],
            "device_type": first_sheet.row_values(i)[4],
        }
        print('Device Executed :')
        print(first_sheet.row_values(i)[0]+' '+my_device["host"])
        write=open(capture_path+'/'+first_sheet.row_values(i)[0]+'-'+first_sheet.row_values(i)[1]+'.txt','w')
        
        try:
            net_connect = Netmiko(**my_device)
            #key information about device
            write.write(first_sheet.row_values(i)[4]+'\n')
            #show ver
            count_column = 5
            while count_column < 105:
                output = net_connect.send_command(first_sheet.row_values(i)[count_column])
                print(output)
                write.write(first_sheet.row_values(i)[count_column]+'\n')
                write.write(output+'\n')
                count_column+=1
            #show run
           
            
            #disconnect netmiko
            net_connect.disconnect()
        
        except:
            write.write('Cannot Remote Device')
'''