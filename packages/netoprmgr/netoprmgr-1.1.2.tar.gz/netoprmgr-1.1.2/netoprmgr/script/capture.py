import os

from netmiko import Netmiko
import xlrd

def function_capture(data_dir,command_dir,capture_path):
    book = xlrd.open_workbook(data_dir)
    first_sheet = book.sheet_by_index(0)
    cell = first_sheet.cell(0,0)

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

            write.write('env-'+first_sheet.row_values(i)[5]+'\n')
            #show ver
            output = net_connect.send_command(first_sheet.row_values(i)[4])
            read_txt = open(command_dir,'r')
            list_txt = read_txt.readlines()
            for i in list_txt:
                output = net_connect.send_command(i)
                print(output)
                write.write('#'+i+'\n')
                write.write(output+'\n')

            #disconnect netmiko
            net_connect.disconnect()
        
        except:
            write.write('Cannot Remote Device')
        #except NameError:
            #raise
