#!/usr/bin/python3

import sys
import os
import shutil
import re
import argparse
from distutils.util import strtobool
import fileinput
import fnmatch

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

def prompt_bool(question):
    sys.stdout.write('%s [y/n]: ' % question)
    while True:
        try:
            return strtobool(input().lower())
        except ValueError:
            sys.stdout.write('Please respond with \'y\' or \'n\'.\n')

def install_mod(name, reinstall=False):
    mod_name = name
    # This is the dir your mods will be stored in
    mod_dir_copy_path = home + '/MWmods/' + mod_name
    data_string = 'data="{0}{1}"'.format(mod_dir, mod_name)

    # Check if mod is already in config (prompt for re-install and new position)
    clean_config = False
    config_updated = False
    with open(openmw_config_file_path, mode='r') as config:
        if config.read().find(data_string + '\n') != -1:
            clean_config = prompt_bool('Mod directory "{}" already exists in config file. Replace (possibly changing install order)?'.format(mod_name))
            config_updated = not clean_config

    for line in fileinput.input(openmw_config_file_path, True, ".bak", 0, "r", None):
        if line != (data_string+'\n') or (not clean_config):
            sys.stdout.write(line)

    # Check if mod directory has already been installed
    if not reinstall and os.path.exists(mod_dir_copy_path):
        if prompt_bool('Mod Directory "{0}" exists. Replace with new version?'.format(mod_dir_copy_path)):
            shutil.rmtree(mod_dir_copy_path)
        else:
            reinstall = True

    os.makedirs(mod_dir, exist_ok=True)
    if reinstall == False:
        print("Copying mod")
        shutil.copytree(mod_name, mod_dir_copy_path)

    # Detect BSAs and add automatically
    bsa_string = ""
    for file in os.listdir(mod_dir_copy_path):
        if fnmatch.fnmatch(file, '*.bsa'):
            if bsa_string != "":
                bsa_string += '\n'
            bsa_string += 'fallback-archive={0}'.format(file)

    # We make a back up of the config file
    if not config_updated:
        shutil.copy(openmw_config_file_path, openmw_config_path + 'openmw.cfg.bak')
        print("Editing MW config")
        with open(openmw_config_file_path, mode='a') as config:
            print(data_string, file=config)
            if bsa_string:
                print(bsa_string, file=config)


if args.r:
    for i in os.listdir(mod_dir):
        install_mod(i, True)


if args.a:
    install_mod(args.a)



elif args.l:
    list_mods()
