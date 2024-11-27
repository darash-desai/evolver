import logging

from evolver import Evolver


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def main():
    """Main function for the application."""
    logging.info("Started eVOLVER server.")

    # TODO: Create server instance
    evolver = Evolver()

    logging.info("eVOLVER server closed.")


if __name__ == "__main__":
    setup_logging()
    main()
