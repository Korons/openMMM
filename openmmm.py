#!/usr/bin/python3

import sys
import os
import shutil
import re
import argparse

parser = argparse.ArgumentParser(description='Manage openMW mods')
parser.add_argument("-a", help="Mod to add",)
parser.add_argument("-l", help="List mods", action="store_true")
parser.add_argument("-r", help="Reinstalls all mods from the moddir", action="store_true")
args = parser.parse_args()

# We get the users home
home = os.getenv("HOME")
openmw_config_path = home + '/.config/openmw/'
openmw_config_file_path = home + '/.config/openmw/openmw.cfg'
mod_dir = home + '/MWmods/'



def list_mods():
    with open(openmw_config_file_path) as f:
        print('Opening config file')
        lines = f.read().splitlines()
    for i in lines:
        if bool(re.findall("data=", i)) == True:
            print(i)

def install_mod(name, reinstall=False):
    mod_name = name
    # This is the dir your mods will be stored in
    mod_dir_copy_path = home + '/MWmods/' + mod_name
    data_string = 'data="{0}{1}"'.format(mod_dir, mod_name)
    os.makedirs(mod_dir, exist_ok=True)
    if reinstall == False:
        print("Copying mod")
        shutil.copytree(mod_name, mod_dir_copy_path)

    # We make a back up of the config file
    shutil.copy(openmw_config_file_path, openmw_config_path + 'openmw.cfg.bak')
    print("Editing MW config")
    with open(openmw_config_file_path, mode='a') as config:
        print(data_string, file=config)


if args.r:
    for i in os.listdir(mod_dir):
        install_mod(i, True)


if args.a:
    install_mod(args.a)



elif args.l:
    list_mods()
