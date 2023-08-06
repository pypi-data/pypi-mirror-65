import xlrd
import xlsxwriter
import paramiko
from paramiko_expect import SSHClientInteraction

def device_identification(raw_data_dir):
    book = xlrd.open_workbook(raw_data_dir)
    first_sheet = book.sheet_by_index(0)
    cell = first_sheet.cell(0,0)

    wb = xlsxwriter.Workbook('devices_data.xlsx')
    ws = wb.add_worksheet('summary')

    count_row = 0
    for i in range(first_sheet.nrows):
        
        hostname = first_sheet.row_values(i)[0]
        ip = first_sheet.row_values(i)[1]
        username = first_sheet.row_values(i)[2]
        password = first_sheet.row_values(i)[3]

        try:
            remote_conn_pre = paramiko.SSHClient()
            remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            remote_conn_pre.connect(ip, username=username, password=password, allow_agent=False, look_for_keys=False)
            print ("SSH connection established to %s" % ip)

            remote_conn = remote_conn_pre.invoke_shell()   
            output = remote_conn.recv(1000).decode("utf-8")
            prompt = output.strip()
            remote_conn.close()

            remote_conn_pre.connect(ip, username=username, password=password, allow_agent=False, look_for_keys=False)
            interact = SSHClientInteraction(remote_conn_pre, timeout=20, display=False)

            interact.expect(prompt)

            interact.send('terminal length 0')
            interact.expect(prompt)

            cmd_output = interact.current_output_clean

            interact.send('show ver')
            interact.expect(prompt)
            cmd_output = interact.current_output_clean
            
            remote_conn_pre.close()

            if 'Cisco Adaptive Security Appliance Software' in cmd_output:                                                   
                ws.write(count_row,0,hostname)
                ws.write(count_row,1,ip)
                ws.write(count_row,2,username)
                ws.write(count_row,3,password)
                ws.write(count_row,4,'cisco_asa')

            elif 'Cisco IOS XE Software' in cmd_output:                                                    
                ws.write(count_row,0,hostname)
                ws.write(count_row,1,ip)
                ws.write(count_row,2,username)
                ws.write(count_row,3,password)
                ws.write(count_row,4,'cisco_xe')

            elif 'Cisco IOS Software' in cmd_output:
                ws.write(count_row,0,hostname)
                ws.write(count_row,1,ip)
                ws.write(count_row,2,username)
                ws.write(count_row,3,password)
                ws.write(count_row,4,'cisco_ios')                           
                
            elif 'Cisco Nexus Operating System (NX-OS) Software' in cmd_output:                         
                ws.write(count_row,0,hostname)
                ws.write(count_row,1,ip)
                ws.write(count_row,2,username)
                ws.write(count_row,3,password)
                ws.write(count_row,4,'cisco_nxos')                          
                
            elif 'Series Wireless LAN Controller' in cmd_output:                         
                ws.write(count_row,0,hostname)
                ws.write(count_row,1,ip)
                ws.write(count_row,2,username)
                ws.write(count_row,3,password)
                ws.write(count_row,4,'cisco_wlc')
            else:
                ws.write(count_row,0,hostname)
                ws.write(count_row,1,ip)
                ws.write(count_row,2,username)
                ws.write(count_row,3,password)
                ws.write(count_row,4,'unidentified')     

            if 'WS-C3850-12S' in cmd_output:
                ws.write(count_row,5,'WS-C3850-12S')
        

        except:
            pass
        #except NameError:
           # raise

    count_row+=1
    wb.close()