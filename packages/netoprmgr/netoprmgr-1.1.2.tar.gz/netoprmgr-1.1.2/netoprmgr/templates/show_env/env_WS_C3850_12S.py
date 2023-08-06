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
        list_psu = []
        psu_line_start = 0
        psu_line_end = 0
        count_line=0
        for i in read_file_list: 
            if re.findall('(?=^((?!.*PS.*).*)$)(?=^.*FAN.*is(.*))', i):
                regex_fan_cond = re.findall('(?=^((?!.*PS.*).*)$)(?=^.*FAN.*is(.*))', i)
                list_fan_cond = regex_fan_cond[0]
                fan_cond = list_fan_cond[1]
                print(list_fan_cond)
            if 'Sys Pwr' in i:
                psu_line_start = count_line
            if  psu_line_start != 0:
                if re.findall('^#',i) :
                    psu_line_end=count_line
                    psu_line_start = (psu_line_start+2)
                    while psu_line_start < psu_line_end:
                        list_psu.append(read_file_list[psu_line_start])
                        psu_line_start+=1
                    psu_line_start=0
            count_line+=1

        for i in list_psu:
            print(i)
            
       

