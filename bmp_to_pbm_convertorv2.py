from PIL import Image
import sys
import os
import PySimpleGUI as psg
import time

pathname = os.path.dirname(sys.argv[0])
DEFAULT_WINDOW_ICON = (str(os.path.abspath(pathname)) + '\\b2p.ico')

def main():
    if len(sys.argv)>1 and sys.argv[1] == '-i':
        command_line_convert()
        sys.exit()
    show_instructions()
    import_folder, export_folder = get_import_export_folders()
    convert_files(import_folder, export_folder)

def show_instructions():


    psg.Popup('Instructions',
             'Step 1: Select folder with .bmp, .png, or .jpg files to convert.',
             'Step 2: Select an export folder for pbm files to be exported to.',
             'Step 3: Select name stripping.',
             'Step 4: Select a filename prifix and suffix if desired.\n', line_width=70, icon=DEFAULT_WINDOW_ICON
    )

def get_import_export_folders():
    file_import_folder = psg.PopupGetFolder('Select image(s) import folder','Select import folder:', icon=DEFAULT_WINDOW_ICON)
    if not file_import_folder:
        psg.Popup('Closing','Image import folder not selected!')
        sys.exit()
    elif not os.path.isdir(file_import_folder):
        psg.Popup('Closing','Image import folder not valid!')
        sys.exit()

    file_export_folder = psg.PopupGetFolder('Select image(s) export folder','Select export folder:', icon=DEFAULT_WINDOW_ICON)
    if not file_export_folder:
        psg.Popup('Closing','Image export folder not selected!')
        sys.exit()    
    elif not os.path.isdir(file_export_folder):
        psg.Popup('Closing','Image export folder not valid!')
        sys.exit()

    return file_import_folder, file_export_folder

def convert_files(file_import_folder, file_export_folder):
    strip_filename = psg.PopupYesNo('Strip original file name?','Useful when converting a sequence of images\n\nExample: test.bmp -> 1.pbm\n', icon=DEFAULT_WINDOW_ICON)
    error_list = []
    file_name_prefix = psg.PopupGetText('Set saved image name prefix\nLeave blank for none','Set saved image name prefix','', icon=DEFAULT_WINDOW_ICON)
    file_name_suffix = psg.PopupGetText('Set saved image name suffix\nLeave blank for none','Set saved image name suffix','', icon=DEFAULT_WINDOW_ICON)
    if file_name_prefix == None:
        file_name_prefix = ''
    if file_name_suffix == None:
        file_name_suffix = ''
    converted_counter = 1
    failed_counter = 0
    files_to_convert = [(file, (str(file_import_folder) + '/' + str(file))) for file in os.listdir(file_import_folder) if '.bmp' in file or '.jpg' in file or '.png' in file]
    for file_to_convert in files_to_convert:        
        try:
            img = Image.open(file_to_convert[1])
            img = img.convert('1')
            new_img = img.point(lambda x: bool(x))
            new_name = ''
            for extention in ('.jpg','.bmp','.png'):
                if extention in file_to_convert[0] and strip_filename == 'No':
                    new_name += file_to_convert[0].replace(extention, '')
            new_name += str(file_name_suffix) + '.pbm'
            prefix = str(converted_counter) + file_name_prefix
            new_img.save(file_export_folder + '/'  + prefix + new_name)
            converted_counter +=1
        except IOError as e:
            error_list.append(f"I/O error({e.errno}): {e.strerror} - {file_to_convert[0]}")
            failed_counter +=1
        except ValueError as e:
            error_list.append(f"Value Error {e} - {file_to_convert[0]}")
            failed_counter +=1
        except:
            error_list.append("Unexpected error:" + str(sys.exc_info()[0]) + ' - ' + str(file_to_convert[0]))
            failed_counter +=1
    
    if failed_counter > 0:
        psg.Popup('Errors Detected', f'Unable to convert {failed_counter} files...',str(*error_list), icon=DEFAULT_WINDOW_ICON)
    else:
        psg.Popup('Completed!', f'{converted_counter-1} files converted!', icon=DEFAULT_WINDOW_ICON)

def command_line_convert():
    command_line_help_message = '''Incorrect commandline format!
Expected Format:
-i "import folder" -e "export folder" -p "prefix" -s "suffix" -st

Example:
python bmp_to_pbm_converterv2.py -f "c:\imgs" -e "c:\imgs" -p "new_" -s "_testing" -st'''

    file_import_folder = ''
    file_export_folder = ''
    file_name_prefix = ''
    file_name_suffix = ''
    strip_filename = 'No'

    if len(sys.argv) < 4:
        print(command_line_help_message)
        sys.exit()

    if len(sys.argv)>1 and sys.argv[1] == '-i':
        file_import_folder = sys.argv[2]
    else:
        print(command_line_help_message)
        sys.exit()           
    if len(sys.argv)>3 and sys.argv[3] == '-e':
        file_export_folder = sys.argv[4]
    else:
        print(command_line_help_message)
        sys.exit()   
    if len(sys.argv)>5 and sys.argv[5] == '-p':
        file_name_prefix = sys.argv[6]
    elif len(sys.argv)>5 and sys.argv[5] == '-s':
        file_name_suffix = sys.argv[6]
    elif len(sys.argv)>5 and sys.argv[5] == '-st':
        strip_filename = 'Yes'
    if len(sys.argv)>7 and sys.argv[7] == '-s':
        file_name_suffix = sys.argv[8]
    elif len(sys.argv)>7 and sys.argv[7] == '-st':
        strip_filename = 'Yes'
    if len(sys.argv)>9 and sys.argv[9] == '-st':
        strip_filename = 'Yes'

    error_list = []
    converted_counter = 1
    failed_counter = 0
    files_to_convert = [(file, (str(file_import_folder) + '/' + str(file))) for file in os.listdir(file_import_folder) if '.bmp' in file or '.jpg' in file or '.png' in file]
    for file_to_convert in files_to_convert:        
        try:
            img = Image.open(file_to_convert[1])
            img = img.convert('1')
            new_img = img.point(lambda x: bool(x))
            new_name = ''
            for extention in ('.jpg','.bmp','.png'):
                if extention in file_to_convert[0] and strip_filename == 'No':
                    new_name += file_to_convert[0].replace(extention, '')
            new_name += str(file_name_suffix) + '.pbm'
            prefix = str(converted_counter) + file_name_prefix
            new_img.save(file_export_folder + '/'  + prefix + new_name)
            converted_counter +=1
        except IOError as e:
            error_list.append(f"I/O error({e.errno}): {e.strerror} - {file_to_convert[0]}")
            failed_counter +=1
        except ValueError as e:
            error_list.append(f"Value Error {e} - {file_to_convert[0]}")
            failed_counter +=1
        except:
            error_list.append("Unexpected error:" + str(sys.exc_info()[0]) + ' - ' + str(file_to_convert[0]))
            failed_counter +=1
    
    if failed_counter > 0:
        print('Errors Detected', f'Unable to convert {failed_counter} files...',str(*error_list))
    else:
        print('Completed!', f'{converted_counter-1} files converted!')


if __name__ == "__main__":
    main()