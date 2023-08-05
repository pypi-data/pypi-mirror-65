import os
import time
import pkg_resources
import shutil

from preventivemaintenance.script.capture import function_capture

capture_path = pkg_resources.resource_filename('preventivemaintenance', 'capture/')
data_path = pkg_resources.resource_filename('preventivemaintenance', 'data/')
result_path = pkg_resources.resource_filename('preventivemaintenance', 'result/')

print(capture_path)

answer=input(
    'Press Number for Menu\n'
    '1. Capture\n'
    '2. Create Report\n'
    '3. Analyze Capture with NTC_template(Dev)\n'
    '4. Ping(Still not Work)\n'
    'Type "quit" to quit program\n'
    )
if answer == '1':
    data_dir = (data_path+'/devices_data.xlsx')
    function_capture=function_capture(data_dir,capture_path)
elif answer == '2':
    try:
        chg_dir = os.chdir(capture_path)
        #current_dir = os.path.dirname(os.path.realpath(__file__))
        current_dir=os.getcwd()
        from preventivemaintenance.script.file_identification import file_identification
        from preventivemaintenance.script.to_docx import to_docx
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
elif answer == '3':
    current_dir = os.path.dirname(os.path.realpath(__file__))
    src_mv = (current_dir+'/Capture/result.xls')
    dst_mv = (current_dir+'/Result/result.xls')
    chg_dir = os.chdir(current_dir+'/Capture')
    files = os.listdir(chg_dir)
    function_analyze_capture=function_analyze_capture(files)
    time.sleep(3)
    shutil.move(src_mv,dst_mv)