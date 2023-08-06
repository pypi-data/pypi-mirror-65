import matplotlib.pyplot as plt; plt.rcdefaults()
from matplotlib import pyplot as plt
import numpy as np
import sqlite3
import re

class to_chart:
    @staticmethod
    def to_chart():
        #open db connection
        db = sqlite3.connect('pmdb')
        cursor = db.cursor()
        
        #SOFTWARE SUMMARY
        #sql query
        cursor.execute('''SELECT version, COUNT(*) FROM summarytable GROUP BY version''')
        count_version = cursor.fetchall()
        cursor.execute('''SELECT COUNT(version) FROM summarytable''')
        total = cursor.fetchall()
        total=(str(total))
        total=re.sub("\D", "", total)
        total=int(total)
        #create list
        percentage=[]
        for row in count_version:
            percentage.append((row[1]/int(total))*100)
        plt.style.use("fivethirtyeight")
        labels=[]
        for row in count_version:
            labels.append(row[0])
        #create pie chart     
        patches, texts = plt.pie(percentage, shadow=True, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.tight_layout()
        #save image
        print('Saving Image')
        plt.savefig('Software Summary.png')
        plt.close()
        print('Image saved to Software Summary.png')
        
        #HARDWARE SUMMARY
        #sql query
        cursor.execute('''SELECT model, COUNT(*) FROM summarytable GROUP BY model''')
        count_model = cursor.fetchall()
        cursor.execute('''SELECT COUNT(model) FROM summarytable''')
        total = cursor.fetchall()
        total=(str(total))
        total=re.sub("\D", "", total)
        total=int(total)
        #create list
        percentage=[]
        for row in count_model:
            percentage.append((row[1]/int(total))*100)
        plt.style.use("fivethirtyeight")
        labels=[]
        for row in count_model:
            labels.append(row[0])
        #create pie chart     
        patches, texts = plt.pie(percentage, shadow=True, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.tight_layout()
        #save image
        print('Saving Image')
        plt.savefig('Hardware Summary.png')
        plt.close()
        print('Image saved to Hardware Summary.png')
        
        #CPU Summary
        #sql query
        cursor.execute('''SELECT devicename, cpu_total FROM summarytable''')
        cpu = cursor.fetchall()
        #create list
        devicename=[]
        for row in cpu:
            devicename.append(row[0])
        cpu_total=[]
        for row in cpu:
            cpu_total.append(row[1])
        #create bar chart
        y_pos = np.arange(len(devicename))
        plt.barh(y_pos, cpu_total, align='center', alpha=0.5)
        plt.yticks(y_pos, devicename)
        plt.tight_layout()
        #save image
        print('Saving Image')
        plt.show
        plt.savefig('CPU Summary.png')
        plt.close()
        print('Image saved to CPU Summary.png')
        
        #Memory Summary
        #sql query
        cursor.execute('''SELECT devicename, memory_percentage FROM summarytable''')
        memory = cursor.fetchall()
        #create list
        devicename=[]
        for row in memory:
            devicename.append(row[0])
        memory_total=[]
        for row in memory:
            memory_total.append(row[1])
        #create bar chart
        y_pos = np.arange(len(devicename))
        plt.barh(y_pos, memory_total, align='center', alpha=0.5)
        plt.yticks(y_pos, devicename)
        plt.tight_layout()
        #save image
        print('Saving Image')
        plt.show
        plt.savefig('Memory Summary.png')
        plt.close()
        print('Image saved to Memory Summary.png')
        
        #close database
        db.close()