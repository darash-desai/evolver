import logging


class Evolver:
    """Singleton class for the eVOLVER control software."""

    _instance = None

    def __new__(singletonClass):
        if singletonClass._instance is None:
            singletonClass._instance = super().__new__(singletonClass)
        return singletonClass._instance

    def __init__(self):
        logging.info("Creating eVOLVER singleton instance")
