#!/usr/bin/env python
import sys
import os
import json
from datetime import datetime
from .easydcer_modules import config, basicChecks, dcer

bcolors = basicChecks.bcolors
subscription = ""
base_path = ""
entity_type = ""


def usage():
    print(f"\n{bcolors.WARNING}Usage: pyeasydcer <entity_type> <id's of entities separated by a comma(,){bcolors.ENDC}")
    print(f"\n{bcolors.WARNING}A Python script to automate default content export in Drupal 8.{bcolors.ENDC}")
    print(f"\n{bcolors.WARNING}This script stores subscription and path in a config file so as user does not need to type them everytime they use the script{bcolors.ENDC}")
    print(f"\n{bcolors.WARNING}Positional arguments:{bcolors.ENDC}")
    print(f"\t{bcolors.WARNING}There are no positional arguments for this script,\n\tyou can use arguments in any combination{bcolors.ENDC}")
    print(f"\n{bcolors.WARNING}Optional arguments:{bcolors.ENDC}")
    print(f"\t{bcolors.WARNING}lando   If you are using a lando environment use lando argument{bcolors.ENDC}")
    print(f"\t{bcolors.WARNING}-force   Force change configuration stored by script{bcolors.ENDC}")
    print(f"\t{bcolors.WARNING}-config   View the config stored by the script {bcolors.ENDC}\n")


def configCheck():
    try:
        local_config_file = os.path.join(
            os.environ["HOME"], ".pydcer_config/pydcer_settings.json"
        )
        with open(local_config_file) as file_read_object:
            pydcer_saved_config = json.load(file_read_object)
            subscription = pydcer_saved_config["subscription"]
            base_path = pydcer_saved_config["path"]
            config_saved_time = datetime.strptime(
                pydcer_saved_config["time_stamp"], "%c"
            )
            current_time = datetime.now()
            difference_in_time = (current_time - config_saved_time).seconds

            print(f"\n{bcolors.OKGREEN}{bcolors.BOLD}Found a config already saved, This is the config script will use::\n\nSubscription: {subscription}\nbase_path: {base_path}\nConfig save time: {str(config_saved_time)}{bcolors.ENDC}")
            if difference_in_time >= 21600:
                print(f"\n{bcolors.WARNING}Saved config is more than an hour old, so the script will again \nask you to the change the config when you run the script, \nor you can use '-force' argument to change the config whenever you need{bcolors.ENDC}\n")
            else:
                print(f"\n{bcolors.WARNING}If you want to change the config, Please use '-force' argument \nwhen you run the script so you can change the config when ever you want!!{bcolors.ENDC}\n")
    except FileNotFoundError:
        print(f"\n{bcolors.FAIL}{bcolors.BOLD}Cannot find a saved config file, Please continue with running the script normally \nand the script will create a config file for you{bcolors.ENDC}\n")


def forceChangeConfig():
    pydcerConfig = config.checkConfig("force_change")

    pydcer_saved_config = pydcerConfig.getInfo()
    subscription = pydcer_saved_config["subscription"]
    base_path = pydcer_saved_config["path"]
    config_saved_time = datetime.strptime(pydcer_saved_config["time_stamp"], "%c")

    print(f"\n{bcolors.OKGREEN}Config saved::\n\nSubscription: {subscription}\nbase_path: {base_path}\nConfig save time: {str(config_saved_time)}{bcolors.ENDC}\n")


def getAvailEntities():
    available_entities_config_file = os.path.join(
        os.environ["HOME"], ".pydcer_config/available_entities.txt"
    )
    with open(available_entities_config_file) as read_entity:
        avail_entities = read_entity.read().splitlines()
        print(f"\n")
        for item in avail_entities:
            print(f"{bcolors.OKGREEN}{item}{bcolors.FAIL}")
        print("\n")


def main():
    global subscription, base_path, entity_type
    if len(sys.argv) is 2:
        if "-help" in sys.argv or "-h" in sys.argv:
            usage()
            sys.exit(1)
        elif "-config" in sys.argv:
            configCheck()
            sys.exit(1)
        elif "-force" in sys.argv:
            forceChangeConfig()
            sys.exit(1)

    if basicChecks.basicChecks() and basicChecks.checkForAvailableEntitiesText():
        if "-force" in sys.argv:
            pydcerConfig = config.checkConfig("force_change")
            sys.argv.remove("-force")
        else:
            pydcerConfig = config.checkConfig()

        pydcer_saved_config = pydcerConfig.getInfo()
        subscription = pydcer_saved_config["subscription"]
        base_path = pydcer_saved_config["path"]

        if basicChecks.rootCheck(base_path, subscription):
            arguments_array = sys.argv[1:]
            entity_type = ""
            available_entities_config_file = os.path.join(
                os.environ["HOME"], ".pydcer_config/available_entities.txt"
            )
            with open(available_entities_config_file) as entity:
                available_entities = entity.read().splitlines()
                for entry in available_entities:
                    if entry in arguments_array:
                        entity_type = entry
                        arguments_array.remove(entity_type)
                        break
                if not entity_type:
                    print(f"{bcolors.FAIL}{bcolors.BOLD}\nWrong entity type detected{bcolors.ENDC}\n")
                    sys.exit(1)

            if "lando" in arguments_array:
                landoEnv = True
                arguments_array.remove("lando")
            else:
                landoEnv = False

            if len(arguments_array) == 1:
                ids_array = arguments_array[0]
            else:
                print(f"{bcolors.FAIL}{bcolors.BOLD}\nWrong input given to the script, Please use -help section{bcolors.ENDC}\n")
                sys.exit(1)

            if landoEnv:
                dcer.dcer(entity_type, ids_array.split(","), subscription, base_path, landoEnv)
            else:
                dcer.dcer(entity_type, ids_array.split(","), subscription, base_path)
        else:
            print(f"\n{bcolors.FAIL}Look's like Drupal is not properly installed, Cannot find a project with the name: {subscription} in the mentioned path: {base_path}{bcolors.ENDC}")
            sys.exit(1)
    else:
        print(f"{bcolors.FAIL}{bcolors.BOLD}\nCannot proceed further because one of the above checks failed\n{bcolors.ENDC}")
        sys.exit(1)
