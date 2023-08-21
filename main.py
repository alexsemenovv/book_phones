from loguru import logger
import interface
import datetime


if __name__ == '__main__':
    logger.add(f'logs/debug.{datetime.datetime.now().date()}.log',
               format="{time} {level} {message}",
               level='DEBUG', rotation='10 MB', compression='zip')
    logger.info(f"main.py - start program")
    interface.greetings()