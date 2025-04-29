import logging

from evolver import Evolver
from yaml_validate import validate_yaml
from growth_test import growth_protocol

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def main():
    """Main function for the application."""
    logging.info("Starting eVOLVER system.")

    evolver = Evolver()

    print("Command options:")
    print("\t- exit: Disconnect from the eVOLVER")
    print("\t- command [command]: Send [command] to the eVOLVER")
    print("\t- run growth protocol")

    userInput = ""
    while userInput != "exit":
        userInput = input(">")
        print("Accepted input", userInput)

        if userInput.startswith("command"):
            command = userInput.replace("command ", "").strip()
            evolver.send(command)
        elif userInput.startswith("run"):
            growth_protocol()
            
        else:
            print("Invalid command. Please try again.")

    evolver.disconnect()
    logging.info("eVOLVER system stopped.")


if __name__ == "__main__":
    setup_logging()
    main()

