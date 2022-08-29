# Author: Aqeel Anwar(ICSRL)
# Created: 9/20/2019, 12:43 PM
# Email: aqeel.anwar@gatech.edu

import os

from configparser import ConfigParser
from dotmap import DotMap


def ConvertIfStringIsInt(input_string):
    try:
        float(input_string)

        try:
            if int(input_string) == float(input_string):
                return int(input_string)
            else:
                return float(input_string)
        except ValueError:
            return float(input_string)

    except ValueError:
        return input_string


def read_cfg(mask_type="surgical", verbose=False):
    # fix path
    module_base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    config_filename = os.path.join(module_base_dir, "masks", "masks.cfg")
    
    parser = ConfigParser()
    parser.optionxform = str
    parser.read(config_filename)
    cfg = DotMap()
    section_name = mask_type

    if verbose:
        hyphens = "-" * int((80 - len(config_filename)) / 2)
        print(hyphens + " " + config_filename + " " + hyphens)

    # for section_name in parser.sections():

    if verbose:
        print("[" + section_name + "]")
    for name, value in parser.items(section_name):
        value = ConvertIfStringIsInt(value)
        if name != "template":
            cfg[name] = tuple(int(s) for s in value.split(","))
        else:
            # set proper path
            cfg[name] = os.path.join(module_base_dir, value)
            # cfg[name] = value
        spaces = " " * (30 - len(name))
        if verbose:
            print(name + ":" + spaces + str(cfg[name]))

    return cfg
