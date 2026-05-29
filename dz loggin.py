import logging

logging.basicConfig(
    filename="dz.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S"
)

logging.info("Program started successfully")

try:
    a = 1 / 0
except ZeroDivisionError:
    logging.exception("User tried div by zero")
