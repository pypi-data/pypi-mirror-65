import sqlite3
from netoprmgr.templates.show_env.env_WS_C3850_12S import env_WS_C3850_12S
class get_env:
    def __init__(self,files):
        self.files=files

    def get_env(self):
        #destroy table summarytable
        try:
            db = sqlite3.connect('env_pmdb')
            cursor = db.cursor()
            cursor.execute('''DROP TABLE envtable''')
            db.commit()
            db.close()
        except:
            pass
        #open db connection to table summary table
        try:
            db = sqlite3.connect('env_pmdb')
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE envtable(id INTEGER PRIMARY KEY, devicename TEXT,
                                psu TEXT, psu_cond TEXT, fan TEXT, fan_cond TEXT, temp TEXT, temp_cond TEXT)
            ''')
            db.close()
        except:
            pass

        for file in self.files:
            try:
                read_file = open(file, 'r')
                read_file_list = read_file.readlines()
                #len(read_file_list)
                for i in read_file_list:
                    if 'env-WS-C3850-12S' in i:
                        try:
                            env_WS_C3850_12S(file)
                        #except NameError:
                            #raise
                        except:
                            pass
            #except NameError:
            # raise
            except:
                pass
