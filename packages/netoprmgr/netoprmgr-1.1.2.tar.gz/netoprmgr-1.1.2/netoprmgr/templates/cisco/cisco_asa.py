import sqlite3
import re
from netoprmgr.script.get_data import get_data



class cisco_asa:
    def __init__(self,file):
        #open db connection
        db = sqlite3.connect('pmdb')       
        
        #SOFTWARE TABLE 
        #get device name
        self.file=file
        #regex_word=get_data.get_device_name(self.file)
        line, read_file_list = get_data.get_line(self.file,'hostname')
        word_position, devicename=get_data.get_word_one(self.file,read_file_list,line,'0','hostname','1')
        #get model
        line, read_file_list = get_data.get_line(self.file,'Hardware:')
        word_position, model=get_data.get_word_one(self.file,read_file_list,line,'0','Hardware:','1')
        #get ios version
        line, read_file_list = get_data.get_line(self.file,'System image file is')
        word_position, iosversion=get_data.get_word_one(self.file,read_file_list,line,'0','System','4')
        #get uptime
        line, read_file_list = get_data.get_line(self.file,'hours')
        uptime=get_data.get_word_regex(self.file,read_file_list,line,'0',"^.*up(.*)")
        uptime=uptime[0]
        #get configuration register
        line, read_file_list = get_data.get_line(self.file,'Configuration register')
        word_position, confreg=get_data.get_word_one(self.file,read_file_list,line,'0','Configuration','3')
        
        #SOFTWARE TABLE SUMMARY
        line, read_file_list = get_data.get_line(self.file,'Cisco Adaptive Security Appliance Software')
        word_position, version=get_data.get_word_one(self.file,read_file_list,line,'0','Version','1')
        
        #CPU
        line, read_file_list = get_data.get_line(self.file,'CPU utilization')
        word_position, cpu=get_data.get_word_one(self.file,read_file_list,line,'0','seconds','2')
        #cpu interrupt
        cpu_interrupt = '0'
        #cpu process
        cpu = re.findall("(.*)%;$", cpu)
        cpu = cpu[0]
        #cpu total
        cpu_total = int(cpu) + int(cpu_interrupt)
        #cpu status
        if cpu_total<21 :
            cpu_status='Low'
        elif cpu_total<81 :
            cpu_status='Medium'
        else:
            cpu_status='High'

        #MEMORY
        line, read_file_list = get_data.get_line(self.file,'Used memory:')
        #memory used
        word_position, memory_used=get_data.get_word_one(self.file,read_file_list,line,'0','bytes','1')
        #memory percentage
        memory_percentage = re.findall("\((.*)%\)", memory_used)
        memory_percentage = float(memory_percentage[0])
        #memory top three
        memory_top_1=''
        memory_top_2=''
        memory_top_3=''
        memory_top_three = (memory_top_1+'\n'+memory_top_2+'\n'+memory_top_3)
        #memory status
        if float(memory_percentage)<21 :
            memory_status='Low'
        elif float(memory_percentage)<81 :
            memory_status='Medium'
        else:
            memory_status='High'
        
        #HARDWARE
        #convert show inven into list
        multiline = get_data.get_multiline_hardware(self.file,'show inventory','#')
        #get card list
        card = get_data.get_word_hardware(multiline,'PID:',1,'PID:')
        #get serial number list
        serial_number = get_data.get_word_hardware(multiline,'PID:',1,'SN:')
        #merge card list and serial_number list into dictionary
        dict = {serial_number[i]: card[i] for i in range(len(serial_number))}

        #APPEND DATA TO SQL 
        cursor = db.cursor()
        #devicename = regex_word[0] 
        model = model
        iosversion =  iosversion
        uptime=uptime
        confreg=confreg
        version=version
        cursor.execute('''INSERT INTO summarytable(devicename, model, iosversion, uptime, confreg, version, cpu, cpu_interrupt, cpu_total, cpu_status, memory_percentage, memory_top_three, memory_status)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''', (devicename,model,iosversion,uptime,confreg,version,(cpu+'%'),(cpu_interrupt+'%'),cpu_total,cpu_status,memory_percentage,memory_top_three,memory_status,))
        for line in dict:
            cursor.execute('''INSERT INTO hardware(devicename, model, card, serial_number)
                      VALUES(?,?,?,?)''', (devicename,model,dict[line],line,))
        db.commit()             
        db.close()


         

        
        