from typing import Callable
import board
import busio
from adafruit_pn532.i2c import PN532_I2C
import logging
import sys
import threading

class RFIDReader():
    def __init__(self) -> None:
        """starts connection to rfid chip"""
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
    
    def __del__(self) -> None:
        """stops detection thread when object is deleted"""
        self.stop()

    def _chip_detection(self) -> None:
        """loop which triggeres the _on_uid function every time a new chip is recognized."""
        self._last_uid = None
        logging.info("starting detection ...")
        while not self._abort_detection:
            uid = self._chip.read_passive_target(timeout=0.5)
            uid = self._bytearray_to_hexstring(uid)
            if uid is None or uid == self._last_uid:
                continue
            logging.info(f"Detected new token with uid: {[i for i in uid]}")
            self._on_uid(uid, *self._on_uid_args)
            self._last_uid = uid
    
    def _bytearray_to_hexstring(self, byte_array: bytearray) -> str:
        """converts the byte array received from nfc module to hex string

        Args:
            byte_array (bytearray): bytes read from nfc module

        Returns:
            str: hex string
        """
        return "".join(f"{i:02x}" for i in byte_array)
    
    def reset_last_uid(self) -> None:
        """Normally a token is only recognized once when it is near the nfc module to prevent multiple
        triggers of the _on_uid function. this function releases this lock. It should be called on user lockout.
        """
        self._last_uid = None

    def start(self) -> None:
        """starts the detection thread"""
        self._thread = threading.Thread(target=self._chip_detection)
        self._thread.start()
        self._abort_detection = False
    
    def stop(self) -> None:
        """stops the detection thread"""
        self._abort_detection = True
    
    def on_uid(self, function: Callable, args: list = []) -> None:
        """executes the stored function when a new token uid has been detected.

        Args:
            function (Callable): function to call
            args (list, optional): args to pass to given function. Defaults to [].
        """
        self._on_uid = function
        self._on_uid_args = args
