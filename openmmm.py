#/bin/python3

import sys
import os
import shutil

home = os.getenv("HOME")
mod_name = sys.argv[1]

openmw_config_path = home + '/.config/openmw/'
openmw_config_file_path = home + '/.config/openmw/openmw.cfg'
mod_dir = home + '/MWmods/'
mod_dir_copy_path = home + '/MWmods/' + mod_name
data_string = 'data="{0}{1}"'.format(mod_dir, mod_name)

os.makedirs(mod_dir,exist_ok=True)
shutil.copytree(mod_name, mod_dir_copy_path)

# We make a back up of the config file
shutil.copy(openmw_config_file_path, openmw_config_path + 'openmw.cfg.bak')

with open(openmw_config_file_path, mode='a') as config:
    print (data_string, file=config)
