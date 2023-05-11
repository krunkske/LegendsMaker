import os
import sys
import zipfile
import io
import shutil
import json
import subprocess
import pkg_resources

required = {'requests'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    install_lib_yn = str(input("The requierd libraries are not installed. Install them? (Y/n): "))
    if install_lib_yn == "y" or install_lib_yn == "Y" or install_lib_yn == "yes" or install_lib_yn == "Yes":
        python = sys.executable
        subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
    else:
        pass

import requests

#vars
appdata = os.getenv('APPDATA')
temp_directory = appdata + '/Minecraft Legends/internalStorage/premium_cache/TEMP'
bp_end_path = appdata + '/Minecraft Legends/internalStorage/premium_cache/behavior_packs'
rp_end_path = appdata + '/Minecraft Legends/internalStorage/premium_cache/resource_packs'
exec_path = appdata + '/Minecraft Legends/internalStorage/premium_cache'
name_myth = ""
what_template = ""
what_to_do = 0
open_what = 0
delete_what = 0
all_available_templates = ["Base template [1],", "Single block [2]", "Custom [3]"]

#functions needed before 
def download_and_install():

    global name_myth

    print("Downloading and unzipping files")
    response = requests.get(url)
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    zip_file.extractall(appdata + '/Minecraft Legends/internalStorage/premium_cache/TEMP')

    
    print("Copying files")

    dirs = [name for name in os.listdir(temp_directory) if os.path.isdir(os.path.join(temp_directory, name))]
    if dirs:
        path_to_mod_folder = os.path.join(temp_directory, dirs[0])

    all_folders_in_mod = os.listdir(path_to_mod_folder)

    if not name_myth:
        name_myth = dirs[0]
        if os.path.isdir(bp_end_path + '/' + name_myth + '_bp'):
            print("Folder already exist!")
            input("Press enter to exit")
            sys.exit()
        elif os.path.isdir(rp_end_path + '/' + name_myth + '_rp'):
            print("Folder already exist!")
            input("Press enter to exit")
            sys.exit()

    for folder in all_folders_in_mod:
        if folder.endswith('bp'):
            bp_path = path_to_mod_folder + '/' + folder
            print('bp path: ' + bp_path)

            #copy the files from TEMP to the proper folder
            shutil.copytree(bp_path, bp_end_path + '/' + name_myth + '_bp')

        elif folder.endswith('rp'):
            rp_path = path_to_mod_folder + '/' + folder
            print('rp path: ' + rp_path)

            #copy the files from TEMP to the proper folder
            shutil.copytree(rp_path, rp_end_path + '/' + name_myth + '_rp')

    #deleting TEMP folder
    print("Deleting TEMP folder")
    shutil.rmtree(temp_directory)

def name_of_myth():
    print("Setting the name of the Myth")
    #change name in manifest.json to name provided
    with open(bp_end_path + '/' + name_myth + '_bp' + '/' + 'manifest.json', 'r') as f:
        json_data = json.load(f)
    json_data['header']['name'] = name_myth

    with open(bp_end_path + '/' + name_myth + '_bp' + '/' + 'manifest.json', 'w') as f:
        json.dump(json_data, f, indent=2)

    #change name in manifest.json to name provided
    with open(rp_end_path + '/' + name_myth + '_rp/manifest.json', 'r') as f:
        json_data = json.load(f)
    json_data['header']['name'] = name_myth

    with open(rp_end_path + '/' + name_myth + '_rp' + '/' + 'manifest.json', 'w') as f:
        json.dump(json_data, f, indent=2)

    #change name in en_US.lang file
    with open(rp_end_path + '/' + name_myth + '_rp' + '/texts/en_US.lang', 'r') as f:
        file_contents = f.read()
    file_contents = file_contents.replace('Mod Template', name_myth)

    with open(rp_end_path + '/' + name_myth + '_rp' + '/texts/en_US.lang', 'w') as f:
        f.write(file_contents)



#check if file is dropped on exe
if len(sys.argv) > 1:
    pass

what_to_do = int(input("Make new [1], Install [2] or Delete [3]: "))

if what_to_do == 1:
    name_myth = str(input("Name of the Myth: "))

    if name_myth:
        if os.path.isdir(bp_end_path + '/' + name_myth + '_bp'):
            print("Name already exists!")
            input("Press enter to exit")
            sys.exit()
        elif os.path.isdir(rp_end_path + '/' + name_myth + '_rp'):
            print("Name already exists!")
            input("Press enter to exit")
            sys.exit()
    else:
        print("no valid name!")
        input("Press enter to exit")
        sys.exit()

    print(*all_available_templates)
    what_template = int(input("What template: "))

    if os.path.isdir(temp_directory):
        print("TEMP already exist: " + temp_directory)
    else:
        os.mkdir(temp_directory)
        print("making directory TEMP: " + temp_directory)


    if what_template == 1:
        url = 'https://github.com/Luminoso-256/legends_template/archive/refs/heads/main.zip'
    elif what_template == 2:
        url = 'https://github.com/Luminoso-256/mcl_singleblock/archive/refs/heads/main.zip'
    elif what_template == 3:
        url = str(input("Link to the download. Link needs to be a direct link: "))
    else:
        print("No valid link or Template was given")
        input("press enter to exit")
        sys.exit()
    
    download_and_install()
    name_of_myth()

    open_what = int(input("Open vscode [1], file explorer [2] or none [3]: "))

    if open_what == 1:
        #opening vscode
        vscode_exec = 'code ' + '"' + exec_path + '"'

        print('opening vscode in ' + exec_path)
        print(vscode_exec)
        subprocess.run(vscode_exec, shell=True)
    elif open_what == 2:
        print("opening Premium cache: " + exec_path)
        os.startfile(exec_path)
    elif open_what == 3:
        pass
    else:
        print("no valid option was given. Closing program.")
elif what_to_do == 2:
    url = str(input("Link to the download. Link needs to be a direct link: "))
    if not url:
        print("No valid link was given")
        input("press enter to exit")
        sys.exit()
    
    download_and_install()
elif what_to_do == 3:

    #list all folders in bp path
    all_mods_in_bp = os.listdir(bp_end_path)
    print(all_mods_in_bp)
    delete_what = int(input("Wich Behaivior pack do you want to delete (only numbers, type 0 if you want to continue without selecting one): "))

    #delete folder in bp path
    if delete_what == 0:
        pass
    else:
        folders = [f for f in os.listdir(bp_end_path) if os.path.isdir(os.path.join(bp_end_path, f))]
        path_to_del = os.path.join(bp_end_path, folders[delete_what - 1])
        really_delete_yn = str(input("Do you want to delete " + path_to_del + " ? (Y/n): "))
        if really_delete_yn == "y" or really_delete_yn == "Y" or really_delete_yn == "yes" or really_delete_yn == "Yes":
            shutil.rmtree(path_to_del)
            print("Deleted " + path_to_del)
        else:
            print("Canceled")
        

    #list all folders in rp path
    all_mods_in_rp = os.listdir(rp_end_path)
    print(all_mods_in_rp)
    delete_what = int(input("Wich Resource pack do you want to delete (only numbers, type 0 if you want to continue without selecting one): "))

    #delete folder in rp path
    if delete_what == 0:
        pass
    else:
        folders = [f for f in os.listdir(rp_end_path) if os.path.isdir(os.path.join(rp_end_path, f))]
        path_to_del = os.path.join(rp_end_path, folders[delete_what - 1])
        really_delete_yn = str(input("Do you want to delete " + path_to_del + " ? (Y/n): "))
        if really_delete_yn == "y" or really_delete_yn == "Y" or really_delete_yn == "yes" or really_delete_yn == "Yes":
            shutil.rmtree(path_to_del)
            print("Deleted " + path_to_del)
        else:
            print("Canceled")

        

print("Done!")
input("Press enter to exit!")