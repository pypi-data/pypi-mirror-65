import re
import sqlite3
from netoprmgr.templates.cisco.cisco_ios import cisco_ios
from netoprmgr.templates.cisco.cisco_ios_xe import cisco_ios_xe
from netoprmgr.templates.cisco.cisco_asa import cisco_asa
from netoprmgr.templates.cisco.cisco_nexus import cisco_nexus
from netoprmgr.templates.cisco.cisco_wlc import cisco_wlc

#destroy table summarytable
try:
    db = sqlite3.connect('pmdb')
    cursor = db.cursor()
    cursor.execute('''DROP TABLE summarytable''')
    db.commit()
    db.close()
except:
    pass
#open db connection to table summary table
try:
    db = sqlite3.connect('pmdb')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE summarytable(id INTEGER PRIMARY KEY, devicename TEXT,
                           model TEXT, iosversion TEXT, uptime TEXT, confreg TEXT, version TEXT, cpu TEXT, cpu_interrupt TEXT, cpu_total INT, cpu_status TEXT, memory_percentage FLOAT, memory_top_three TEXT, memory_status TEXT)
    ''')
    db.close()
except:
    pass

#destroy table hardware
try:
    db = sqlite3.connect('pmdb')
    cursor = db.cursor()
    cursor.execute('''DROP TABLE hardware''')
    db.commit()
    db.close()
except:
    pass
#open db connection to table hardware
try:
    db = sqlite3.connect('pmdb')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE hardware(id INTEGER PRIMARY KEY, devicename TEXT,
                           model TEXT, card TEXT, serial_number TEXT)
    ''')
    db.close()
except:
    pass



class file_identification:
    
    def __init__(self,files):
        self.files=files

    def file_identification(self):
        print('PROGRAM IS PROCESSING FILE')
        for file in self.files:
            print('Current file processed : ')
            print(file)
            regex_file = re.findall(".py$", file)
            if regex_file:
                pass
            else:
                try:
                    #debug file that currently opened
                    read_file=open(file,'r', encoding='utf8', errors='ignore')
                    read_file_list=read_file.readlines()
                    for every_line in read_file_list:
                        #identification for IOS
                        if 'Cisco Adaptive Security Appliance Software' in every_line:                         
                            cisco_asa(file)                            
                            break
                        elif 'Cisco IOS XE Software' in every_line:                         
                            cisco_ios_xe(file)                            
                            break
                        elif 'Cisco IOS Software' in every_line:
                            cisco_ios(file)                            
                            break
                        elif 'Cisco Nexus Operating System (NX-OS) Software' in every_line:                         
                            cisco_nexus(file)                            
                            break
                        elif 'Series Wireless LAN Controller' in every_line:                         
                            cisco_wlc(file)                            
                            break

                            
                except:
                    pass
                #except NameError:
                #    raise



