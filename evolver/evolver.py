import logging
import serial

from time import time


class Evolver:
    """Singleton class for the eVOLVER control software."""

    _instance = None
    _serial = None
    _serialInput = ""
    _readTimeout = 2

    def __new__(singletonClass):
        if singletonClass._instance is None:
            singletonClass._instance = super().__new__(singletonClass)
        return singletonClass._instance

    def __init__(self):
        self._serial = serial.Serial("/dev/serial0", 9600)
        self._serial.timeout = 5
        logging.info("Creating eVOLVER singleton instance")

    def send(self, command):
        logging.info(f"Sending eVOLVER command: {command}")
        self._serial.write(command.encode())
        self._serial.flush()

        response = self.__readResponse()
        logging.info(f"Received response: {response}")

    def disconnect(self):
        logging.info("Closing eVOLVER connection")
        self._serial.close()

    def __readResponse(self):
        endTime = time() + self._readTimeout
        while time() < endTime:
            self._serialInput += self._serial.read_all().decode()
            response, endSeq, remainder = self._serialInput.partition("end")
            if endSeq != "":
                self._serialInput = remainder
                return f"{response}end"

        logging.error(f"Received incomplete response: {self._serialInput}")
        return ""
