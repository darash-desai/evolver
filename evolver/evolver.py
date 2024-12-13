import logging
import serial


class Evolver:
    """Singleton class for the eVOLVER control software."""

    _instance = None
    _serial = None

    def __new__(singletonClass):
        if singletonClass._instance is None:
            singletonClass._instance = super().__new__(singletonClass)
        return singletonClass._instance

    def __init__(self):
        self._serial = serial.Serial("/dev/serial0", 9600)
        logging.info("Creating eVOLVER singleton instance")

    def send(self, command):
        logging.info(f"Sending eVOLVER command: {command}")

    def disconnect(self):
        logging.info("Closing eVOLVER connection")
        self._serial.close()
