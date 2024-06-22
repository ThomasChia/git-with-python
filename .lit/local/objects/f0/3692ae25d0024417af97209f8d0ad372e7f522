import os

from loguru import logger


def create_dot_lit_directory():
    if os.path.exists(".lit"):
        logger.info(".lit directory already exists.")
    else:
        os.system("mkdir .lit")
        logger.info("Created .lit directory")

        os.system(f"mkdir -p .lit/staging/objects")
        logger.info(f"Created objects directory within staging.")

        os.system(f"mkdir -p .lit/local/objects")
        logger.info(f"Created objects directory within local.")

        os.system(f"touch .lit/HEAD")
        logger.info("Created the HEAD file.")
