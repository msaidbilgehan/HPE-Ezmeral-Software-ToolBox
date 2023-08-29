import logging
import os
import sys
from CLI.commands import cleanup, fqdn_setup, log_collection
from Flask_App.Libraries.logger_module import logger


root_path_log_folder = "CLI/app_logs"

if not os.path.exists(root_path_log_folder):
    os.mkdir(root_path_log_folder)

root_path_logs = root_path_log_folder + '/logs.log'
global_logger:logging.Logger



def logger_configuration(logger):
    # Logger
    # logger = logging.getLogger("HPE Ezmeral Data Fabric ToolBox Project CLI Logger")
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()
        
    logger_stdout_formatter = logging.Formatter('%(levelname)s | %(message)s')
    logger_file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

    logger_stdout_handler = logging.StreamHandler(sys.stdout)
    logger_stdout_handler.setLevel(logging.DEBUG)
    logger_stdout_handler.setFormatter(logger_stdout_formatter)

    logger_file_handler = logging.FileHandler(root_path_logs)
    logger_file_handler.setLevel(logging.DEBUG)
    logger_file_handler.setFormatter(logger_file_formatter)

    logger.addHandler(logger_file_handler)
    logger.addHandler(logger_stdout_handler)
    return logger



def initialize_message(logger):
    logger.info('-----------------------------------')
    logger.info('HPE Ezmeral Data Fabric ToolBox Project')
    logger.info('Reference: https://docs.ezmeral.hpe.com/')
    logger.info('Created By Muhammed Said BİLGEHAN and Mirza ÖZER')
    logger.info('All Rights reserved.')
    logger.info('Version 1.11')
    logger.info('-----------------------------------')
    logger.info('TREO Information Technologies')
    logger.info('https://www.treo.com.tr/')
    logger.info('-----------------------------------')
    



def menu(logger):
    logger.info("1. FQDN Setup")
    logger.info("2. Cleanup Node")
    logger.info("3. Log Collection")
    logger.info("4. Exit")
    option = input("Please select an option: ")
    return option



def menu_action_selection(logger):
    option = ""
    
    while option != "4":
        option = menu(logger)
        
        if option == "1":
            logger.info("FQDN Setup Starting...")
            fqdn_setup()
            
        elif option == "2":
            logger.info("Cleanup Starting...")
            cleanup("./MAPR_Tools/cleanup.py")
            
        elif option == "3":
            logger.info("Collecting logs from nodes...")
            log_collection()

        elif option == "4":
            logger.info("Exiting...")
            exit()
            
        else:
            logger.warning("Invalid option. Please try again.")



if __name__ == "__main__":
    global_logger = logger_configuration(logger)
    initialize_message(global_logger)
    menu_action_selection(global_logger)
    global_logger.info("Exiting...")
    exit()