from logging import Formatter, StreamHandler, INFO, FileHandler, getLogger
from os import path
import sys


sys.path.append('../')
from system.config import LOGGING_LEVEL

# создаём формировщик логов (formatter):
client_formatter = Formatter(
    '%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
path_1 = path.dirname(path.abspath(__file__))
path = path.join(path_1, 'client.log')

# создаём потоки вывода логов
steam = StreamHandler(sys.stderr)
steam.setFormatter(client_formatter)
steam.setLevel(INFO)
log_file = FileHandler(path, encoding='utf8')
log_file.setFormatter(client_formatter)

# создаём регистратор и настраиваем его
logger = getLogger('client')
logger.addHandler(steam)
logger.addHandler(log_file)
logger.setLevel(LOGGING_LEVEL)
