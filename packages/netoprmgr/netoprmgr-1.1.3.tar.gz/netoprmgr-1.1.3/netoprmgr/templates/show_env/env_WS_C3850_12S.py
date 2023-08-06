import re
import sqlite3

class env_WS_C3850_12S:
    def __init__(self,file):
        db = sqlite3.connect('env_pmdb')
        self.file = file
        read_file = open(self.file,'r')
        #print(read_file)
        read_file_list  = read_file.readlines()
        #print(read_file_list)
        list_psu_capture = []
        list_fan = []
        list_fan_cond_cp = []
        list_temp = []
        list_temp_cond = []
        list_psu = []
        list_psu_cond = []
        psu_line_start = 0
        psu_line_end = 0
        count_line=0
        for i in read_file_list:
            if re.findall('^hostname (.*)',i):
                regex_devicename = re.findall('^hostname (.*)',i)
                devicename = regex_devicename[0]
                print(devicename)
            if re.findall('^(Switch.*FAN.*)is',i):
                regex_fan = re.findall('^(Switch.*FAN.*)is',i)
                fan = regex_fan[0]
                list_fan.append(fan)
                #print(fan)
            if re.findall('(?=^((?!.*PS.*).*)$)(?=^.*FAN.*is(.*))', i):
                regex_fan_cond = re.findall('(?=^((?!.*PS.*).*)$)(?=^.*FAN.*is(.*))', i)
                list_fan_cond = regex_fan_cond[0]
                fan_cond = list_fan_cond[1]
                list_fan_cond_cp.append(fan_cond)
                #print(fan_cond)
            if re.findall('^(Switch.*):.*SYSTEM TEMPERATURE',i):
                regex_temp = re.findall('^(Switch.*):.*SYSTEM TEMPERATURE',i)
                temp = regex_temp[0]
                list_temp.append(temp)
                #print(temp)
            if re.findall('^Switch.*:.*SYSTEM TEMPERATURE is(.*)', i):
                regex_temp_cond = re.findall('^Switch.*:.*SYSTEM TEMPERATURE is(.*)', i)
                temp_cond = regex_temp_cond[0]
                list_temp_cond.append(temp_cond)
                #print(temp_cond)
            if 'Sys Pwr' in i:
                psu_line_start = count_line
            if  psu_line_start != 0:
                if re.findall('^#',i) :
                    psu_line_end=count_line
                    psu_line_start = (psu_line_start+2)
                    while psu_line_start < psu_line_end:
                        list_psu_capture.append(read_file_list[psu_line_start])
                        psu_line_start+=1
                    psu_line_start=0
            count_line+=1

        for i in list_psu_capture:
            #print(i.split()[0])
            list_psu.append(i.split()[0])
            try:
                #print(i.split()[3])
                list_psu_cond.append(i.split()[3])
            except:
                #print('-')
                list_psu_cond.append('-')
        
        print('device '+devicename)
        print(list_fan)
        print(list_fan_cond_cp)
        print(list_temp)
        print(list_temp_cond)
        print(list_psu)
        print(list_psu_cond)
        

        #connect DB
        cursor = db.cursor()
        count_sql = 0
        for psu in list_psu:
            cursor.execute('''INSERT INTO envtable(devicename, system, item, status)
                      VALUES(?,?,?,?)''', (devicename,'Power Supply',psu,list_psu_cond[count_sql],))
            count_sql+=1

        count_sql = 0
        for fan in list_fan:
            cursor.execute('''INSERT INTO envtable(devicename, system, item, status)
                      VALUES(?,?,?,?)''', (devicename,'Fan',fan,list_fan_cond_cp[count_sql],))
            count_sql+=1

        count_sql = 0
        for temp in list_temp:
            cursor.execute('''INSERT INTO envtable(devicename, system, item, status)
                      VALUES(?,?,?,?)''', (devicename,'Temperature',temp,list_temp_cond[count_sql],))
            count_sql+=1

        db.commit()             
        db.close()
       

