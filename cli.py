from Libraries.logger_module import logger
from CLI.commands import cleanup, fqdn_setup, log_collection


def initialize_message():
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
    



def menu():
    logger.info("1. FQDN Setup")
    logger.info("2. Cleanup Node")
    logger.info("3. Log Collection")
    logger.info("4. Exit")
    option = input("Please select an option: ")
    return option



def menu_action_selection():
    option = ""
    
    while option != "4":
        option = menu()
        
        if option == "1":
            logger.info("FQDN Setup Starting...")
            fqdn_setup()
            
        elif option == "2":
            logger.info("Cleanup Starting...")
            cleanup()
            
        elif option == "3":
            logger.info("Collecting logs from nodes...")
            log_collection()

        elif option == "4":
            logger.info("Exiting...")
            exit()
            
        else:
            logger.warning("Invalid option. Please try again.")


if __name__ == "__main__":
    initialize_message()
    menu_action_selection()
    logger.info("Exiting...")
    exit()