import os
import time
import pkg_resources
import shutil

from netoprmgr.script.capture import function_capture
from netoprmgr.script.check import function_check
from netoprmgr.script.device_identification import device_identification

capture_path = pkg_resources.resource_filename('netoprmgr', 'capture/')
data_path = pkg_resources.resource_filename('netoprmgr', 'data/')
result_path = pkg_resources.resource_filename('netoprmgr', 'result/')

print(capture_path)

answer=input(
'Press Number for Menu\n'
    '0. Device Identification\n'
    '1. Device Availability Check\n'
    '2. Capture\n'
    '3. Create Report\n'
    '4. Show Environment Report\n'
    'Type "quit" to quit program\n'
    )
if answer == '0':
    chg_dir = os.chdir(data_path)
    raw_data_dir = (data_path+'/raw_data.xlsx')
    device_identification = device_identification(raw_data_dir)
elif answer == '1':
    chg_dir = os.chdir(capture_path)
    current_dir=os.getcwd()
    data_dir = (data_path+'/devices_data.xlsx')
    function_check=function_check(data_dir,capture_path)
    src_mv = (capture_path+'device_availability_check.xlsx')
    dst_mv = (result_path+'device_availability_check.xlsx')
    shutil.move(src_mv,dst_mv)
elif answer == '2':
    data_dir = (data_path+'/devices_data.xlsx')
    command_dir = (data_path+'/show_command.txt')
    function_capture=function_capture(data_dir,command_dir,capture_path)
elif answer == '3':
    try:
        chg_dir = os.chdir(capture_path)
        current_dir=os.getcwd()
        from netoprmgr.script.file_identification import file_identification
        from netoprmgr.script.to_docx import to_docx
        files = os.listdir(current_dir)
        file_identification=file_identification(files)
        file_identification.file_identification()
        to_docx=to_docx()
        to_docx.to_docx()
        time.sleep(3)
        src_mv = (capture_path+'preventive_maintenance.docx')
        dst_mv = (result_path+'preventive_maintenance.docx')
        shutil.move(src_mv,dst_mv)
    except NameError:
        raise
elif answer == '4':
    try:
        chg_dir = os.chdir(capture_path)
        current_dir=os.getcwd()
        from netoprmgr.script.get_env import get_env
        #from netoprmgr.script.to_docx import to_docx
        files = os.listdir(current_dir)
        get_env=get_env(files)
        get_env.get_env()
        #to_docx=to_docx()
        #to_docx.to_docx()
        time.sleep(3)
        #src_mv = (capture_path+'env_report.docx')
        #dst_mv = (result_path+'env_report.docx')
        #shutil.move(src_mv,dst_mv)
    except NameError:
        raise