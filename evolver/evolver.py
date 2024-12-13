import logging
import serial

from time import time


class Evolver:
    """Singleton class for the eVOLVER control software."""

    _instance = None

    def __new__(singletonClass, serialPort="/dev/serial0", readTimeout=2) -> None:
        if singletonClass._instance is None:
            logging.info("Creating eVOLVER singleton instance")
            singletonClass._instance = super().__new__(
                singletonClass, serialPort, readTimeout
            )

        return singletonClass._instance

    def __init__(self, serialPort: str, readTimeout: float) -> None:
        """
        Creates a new eVOLVER instances and connects to it.

        Parameters:
          serialPort (str): The serial port the eVOLVER is available on. Defaults to
                            /dev/serial0.
          readTimeout (float): The timeout for read operations in seconds.
        """

        self._serial = serial.Serial(serialPort, 9600)
        self._readTimeout = readTimeout
        self._serial.timeout = self._readTimeout
        self._serialInput = ""

    def send(self, command: str) -> str:
        """
        Sends a command the eVOLVER communication bus.

        Parameters:
          command (str): The command to send.

        Returns:
          str: The command response or an empty string if no response was received.
        """

        logging.info(f"Sending eVOLVER command: {command}")
        self._serial.write(command.encode())
        self._serial.flush()

        response = self.__readResponse()
        logging.info(f"Received response: {response}")
        return response

    def disconnect(self) -> None:
        """
        Disconnects from the eVOLVER system and closes the serial port.
        """

        logging.info("Closing eVOLVER connection")
        self._serial.close()

    def __readResponse(self) -> str:
        """
        Reads serial data from the eVOLVER until a complete response for a
        command is received or the read timeout limit is met.

        Returns:
          str: A command response or an empty string if the read timed out.
        """

        endTime = time() + self._readTimeout
        while time() < endTime:
            self._serialInput += self._serial.read_all().decode()
            response, endSeq, remainder = self._serialInput.partition("end")
            if endSeq != "":
                self._serialInput = remainder
                return f"{response}end"

        logging.error(f"Received incomplete response: {self._serialInput}")
        return ""
