import xlsxwriter

def create_data_template():
    hostname = ['IDCR1','IDSW1','IDN3K1','IDASA1','IDWLC1',]
    ip_address = ['192.168.1.1','192.168.1.2','192.168.1.3','192.168.1.4','192.168.1.5',]
    username = ['Admin','Admin','Admin','Admin','Admin',]
    password = ['P@s4word','P@s4word','P@s4word','P@s4word','P@s4word',]
    os_type = ['cisco_ios','cisco_ios','cisco_nxos','cisco_asa','cisco_wlc']
    hardware_type = ['WS-C3850','WS-C3850','WS-C3850','WS-C3850','WS-C3850',]

    wb = xlsxwriter.Workbook('devices_data.xlsx')
    ws = wb.add_worksheet('summary')

    count_row=0
    for i in hostname:
        ws.write(count_row,0,i)
        count_row+=1

    count_row=0
    for i in ip_address:
        ws.write(count_row,1,i)
        count_row+=1

    count_row=0
    for i in username:
        ws.write(count_row,2,i)
        count_row+=1

    count_row=0
    for i in password:
        ws.write(count_row,3,i)
        count_row+=1

    count_row=0
    for i in os_type:
        ws.write(count_row,4,i)
        count_row+=1

    count_row=0
    for i in hardware_type:
        ws.write(count_row,5,i)
        count_row+=1

    wb.close()