import logging

logging.basicConfig(filename="fundoo.log", encoding="utf-8", level=logging.INFO,
                    format='%(asctime)s:%(filename)s:%(levelname)s:%(lineno)d:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()