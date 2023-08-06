from logging import Formatter, StreamHandler, INFO, FileHandler, getLogger, handlers
from os import path
import sys


sys.path.append('../')
from system.config import LOGGING_LEVEL

# создаём формировщик логов (formatter):
server_formatter = Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
path_1 = path.dirname(path.abspath(__file__))
path = path.join(path_1, 'server.log')

# создаём потоки вывода логов
steam = StreamHandler(sys.stderr)
steam.setFormatter(server_formatter)
steam.setLevel(INFO)
log_file = handlers.TimedRotatingFileHandler(path, encoding='utf8', interval=1, when='D')
log_file.setFormatter(server_formatter)

# создаём регистратор и настраиваем его
logger = getLogger('server')
logger.addHandler(steam)
logger.addHandler(log_file)
logger.setLevel(LOGGING_LEVEL)