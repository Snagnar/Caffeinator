from typing import Callable
import board
import busio
from adafruit_pn532.i2c import PN532_I2C
import logging
import sys
import threading

class RFIDReader():
    def __init__(self):
        format = "%(asctime)s: %(message)s"

        logging.basicConfig(format=format, level=logging.INFO,

                            datefmt="%H:%M:%S")
        self._i2c = busio.I2C(board.SCL, board.SDA)
        self._chip = PN532_I2C(self._i2c, debug=False)
        self._ic, self._version, self._revision, self._support = self._chip.firmware_version
        if not all([self._ic, self._version, self._revision, self._support]):
            logging.error("PN532 RFID module was not found!")
            sys.exit(1)
        else:
            logging.info(f"Found PN532 RFID chip with firmare vesion: {self._version}.{self._revision}")
        self._on_uid = lambda uid: logging.info(f"Found chip with uid {uid}")
        self._abort_detection = True
    
    def __del__(self):
        self.stop()

    def _chip_detection(self):
        last_uid = None
        logging.info("starting detection ...")
        while not self._abort_detection:
            uid = self._chip.read_passive_target(timeout=0.5)
            if uid is None or uid == last_uid:
                continue
            logging.info(f"Detected new token with uid: {[i for i in uid]}")
            self._on_uid(uid, *self._on_uid_args)
            last_uid = uid

    def start(self):
        self._thread = threading.Thread(target=self._chip_detection)
        self._thread.start()
        self._abort_detection = False
    
    def stop(self):
        self._abort_detection = True
    
    def on_uid(self, function: Callable, args: list = []) -> None:
        self._on_uid = function
        self._on_uid_args = args
