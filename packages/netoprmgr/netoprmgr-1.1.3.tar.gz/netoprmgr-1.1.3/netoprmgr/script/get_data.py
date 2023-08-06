import re
import os
import time

class get_data:
    #get device name by regexing file name
    @classmethod
    def get_device_name(self,file):
        #method to get device name by regexing file
        self.file=file
        regex_word = re.findall("(.*).txt.*$", self.file)
        return regex_word
    #get, where is the line?
    @classmethod
    def get_line(self,file,word_in_file):
        #method to find line where keyword is located
        self.file=file
        self.word_in_file=word_in_file
        read_file=open(file,'r', encoding='utf8', errors='ignore')
        read_file_list=read_file.readlines()
        count_line=0
        for every_line in read_file_list:
            if word_in_file in every_line:
                count_word=0
                line=count_line
                break
            count_line+=1
            
        read_file.close
        return line, read_file_list
    #get line where regex is located, example : show proc memory sorted
    @classmethod
    def get_line_regex(self,file,regex_in_file):
        #method to find line where keyword is located
        self.file=file
        self.regex_in_file=regex_in_file
        read_file=open(file,'r', encoding='utf8', errors='ignore')
        read_file_list=read_file.readlines()
        count_line=0
        for every_line in read_file_list:
            if re.findall(regex_in_file, every_line):
                count_word=0
                line=count_line
                break
            count_line+=1
            
        read_file.close
        return line, read_file_list
    #get line that contain hardware information
    @classmethod
    def get_multiline_hardware(self,file,word_in_file_1,word_in_file_2):
        #method to find line where keyword is located
        self.file=file
        self.word_in_file_1=word_in_file_1
        self.word_in_file_2=word_in_file_2
        read_file=open(file,'r', encoding='utf8', errors='ignore')
        read_file_list=read_file.readlines()
        count_line=0
        multiline=[]
        multiline2=[]
        self.logic_test=False
        for every_line in read_file_list:
            if word_in_file_1 in every_line:
                self.logic_test=True
                #print('count_line')
                #print(count_line)
            if self.logic_test==True:
                #print('every_line')
                #print(every_line)
                #time.sleep(10)
                multiline.append(every_line)
            count_line+=1
        for every_line in multiline[1:]:
            multiline2.append(every_line)
            if word_in_file_2 in every_line:
                break
        read_file.close
        return multiline2
    #method to find hardware with show environment being regexed
    @classmethod
    def get_multiline_hardware_regex(self,file,regex_in_file_1,word_in_file_2):
        #method to find hardware with show environment being regexed
        self.file=file
        self.regex_in_file_1=regex_in_file_1
        self.word_in_file_2=word_in_file_2
        read_file=open(file,'r', encoding='utf8', errors='ignore')
        read_file_list=read_file.readlines()
        count_line=0
        multiline=[]
        multiline2=[]
        self.logic_test=False
        for every_line in read_file_list:
            if re.findall(regex_in_file_1, every_line):
                self.logic_test=True
                #print('count_line')
                #print(count_line)
            if self.logic_test==True:
                #print('every_line')
                #print(every_line)
                #time.sleep(10)
                multiline.append(every_line)
            count_line+=1
        for every_line in multiline[1:]:
            multiline2.append(every_line)
            if word_in_file_2 in every_line:
                break
        read_file.close
        return multiline2
    #get word, with one keyword
    @classmethod
    def get_word_one(self,file,read_file_list,line,row_adjust,word_in_line,word_adjust):
        #method to find
        self.file=file
        self.row_adjust=row_adjust
        self.read_file_list=read_file_list
        self.word_in_line=word_in_line
        self.word_adjust=word_adjust
        count_word=0
        next_line=self.read_file_list[line+int(row_adjust)]
        every_words=next_line.split()
        for every_word in every_words:
            if word_in_line in every_word:                    
                word_position=count_word
                break
            count_word+=1
        word=every_words[word_position+int(word_adjust)]
        return word_position, word
    #get word, with two keyword    
    @classmethod
    def get_word_two(self,file,read_file_list,line,row_adjust,word_in_line,word_in_line2,word_adjust):
        #method to find
        self.file=file
        self.row_adjust=row_adjust
        self.read_file_list=read_file_list
        self.word_in_line=word_in_line
        self.word_adjust=word_adjust
        self.word_in_line2=word_in_line2
        count_word=0
        next_line=self.read_file_list[line+int(row_adjust)]
        every_words=next_line.split()
        for every_word in every_words:
            if word_in_line in every_word:                    
                word_position=count_word
                break
            elif word_in_line2 in every_word:
                word_position=count_word
                break
            count_word+=1
        word=every_words[word_position+int(word_adjust)]
        return word_position, word
    #get word for hardware category
    @classmethod
    def get_word_hardware(self,multiline,word_in_line,word_adjust,word_in_words):
        #method to find
        self.multiline=multiline
        self.word_in_line=word_in_line
        self.word_adjust=word_adjust
        multiline2=[]
        count_line=0
        for line in multiline:
            if word_in_line in line:
                every_words=line.split()
                count_word=0
                for every_word in every_words:
                    if word_in_words in every_word:
                        try:
                            multiline2.append(every_words[count_word+word_adjust])
                        except:
                            multiline2.append('No SN '+str(count_line))
                    count_word+=1
            count_line+=1
        return multiline2
    #get word, with one keyword
    @classmethod
    def get_word_regex(self,file,read_file_list,line,row_adjust,regex):
        #method to find
        self.file=file
        self.row_adjust=row_adjust
        self.read_file_list=read_file_list
        count_word=0
        every_words=self.read_file_list[line+int(row_adjust)]
        regex_words=re.findall(regex, every_words)
        return regex_words