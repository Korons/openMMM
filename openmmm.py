#!/usr/bin/python3

import sys
import os
import shutil
import re
import argparse

parser = argparse.ArgumentParser(description='Manage openMW mods')
parser.add_argument("-a", help="Mod to add",)
parser.add_argument("-l", help="List mods", action="store_true")
args = parser.parse_args()

home = os.getenv("HOME")

openmw_config_path = home + '/.config/openmw/'
openmw_config_file_path = home + '/.config/openmw/openmw.cfg'

def list_mods():
    with open(openmw_config_file_path) as f:
        print ('Opening config ifle')
        lines = f.read().splitlines()
    for i in lines:
        if bool(re.findall("data=", i)) == True:
            print (i)

if args.a:
    mod_name = args.a
    mod_dir = home + '/MWmods/'
    mod_dir_copy_path = home + '/MWmods/' + mod_name
    data_string = 'data="{0}{1}"'.format(mod_dir, mod_name)
    os.makedirs(mod_dir,exist_ok=True)
    shutil.copytree(mod_name, mod_dir_copy_path)

    # We make a back up of the config file
    shutil.copy(openmw_config_file_path, openmw_config_path + 'openmw.cfg.bak')

    with open(openmw_config_file_path, mode='a') as config:
        print (data_string, file=config)


elif args.l:
    list_mods()
