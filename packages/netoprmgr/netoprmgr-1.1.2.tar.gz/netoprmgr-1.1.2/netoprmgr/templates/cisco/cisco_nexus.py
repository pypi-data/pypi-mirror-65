import sqlite3
import re
from netoprmgr.script.get_data import get_data



class cisco_nexus:
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
        line, read_file_list = get_data.get_line(self.file,'Hardware')
        word_position, model=get_data.get_word_one(self.file,read_file_list,line,'1','cisco','0')
        #get ios version
        line, read_file_list = get_data.get_line(self.file,'system image file is:')
        word_position, iosversion=get_data.get_word_one(self.file,read_file_list,line,'0','system','4')
        #get uptime
        line, read_file_list = get_data.get_line(self.file,'uptime')
        uptime=get_data.get_word_regex(self.file,read_file_list,line,'0',"^.*uptime is(.*)")
        uptime=uptime[0]
        #get configuration register
        confreg=''

        #SOFTWARE TABLE SUMMARY
        line, read_file_list = get_data.get_line(self.file,'system:')
        word_position, version=get_data.get_word_one(self.file,read_file_list,line,'0','version','1')
        
        #CPU
        line, read_file_list = get_data.get_line(self.file,'CPU util')
        word_position, cpu=get_data.get_word_one(self.file,read_file_list,line,'0',':','1')
        word_position, cpu_kernel=get_data.get_word_one(self.file,read_file_list,line,'0',':','3')
        #cpu interrupt
        cpu_interrupt = '0'
        #cpu process
        cpu = re.findall("^(.*)%", cpu)
        cpu = cpu[0]
        cpu_kernel = re.findall("^(.*)%", cpu_kernel)
        cpu_kernel = cpu_kernel[0]
        cpu = str(float(cpu)+float(cpu_kernel))
        #cpu total
        cpu_total = float(cpu) + float(cpu_interrupt)
        #cpu status
        if cpu_total<21 :
            cpu_status='Low'
        elif cpu_total<81 :
            cpu_status='Medium'
        else:
            cpu_status='High'

        #MEMORY
        line, read_file_list = get_data.get_line(self.file,'Memory usage:')
        #memory total
        word_position, memory_total=get_data.get_word_one(self.file,read_file_list,line,'0','usage:','1')
        #memory used
        word_position, memory_used=get_data.get_word_one(self.file,read_file_list,line,'0','usage:','3')
        #memory percentage
        memory_total=re.sub("\D", "", memory_total)
        memory_used=re.sub("\D", "", memory_used)
        memory_percentage = (int(memory_used)/int(memory_total))*100
        memory_percentage = re.findall("(^.{5})*", str(memory_percentage))
        memory_percentage = float(memory_percentage[0])        
        #memory top three
        memory_top_three = ''
        #memory status
        if float(memory_percentage)<21 :
            memory_status='Low'
        elif float(memory_percentage)<81 :
            memory_status='Medium'
        else:
            memory_status='High'
        
        #HARDWARE
        #convert show inven into list
        multiline = get_data.get_multiline_hardware_regex(self.file,'^.*#.*sh.*inven','#')
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