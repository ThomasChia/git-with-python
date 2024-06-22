import ast
import hashlib
import os

from loguru import logger

from lit.lit_config import LOCAL_REPOSITORY, STAGING_DIRECTORY


def commit_files_to_local(message: str):
    if not message:
        logger.error("Please provide a message with --m when committing files.")

    os.system(
        f"rsync -a .lit/{STAGING_DIRECTORY}/objects/ .lit/{LOCAL_REPOSITORY}/objects && rm -rf .lit/{STAGING_DIRECTORY}/objects/*"
    )

    logger.info("Moved files from staging to local repository.")

    with open(f".lit/HEAD", "r") as past_head_commit_hash:
        past_commit_hash = past_head_commit_hash.read()

    # Read "add_reference" and turn into commit message
    with open(".lit/add_reference", "r") as add_reference:
        add_reference_data = add_reference.read()
        add_reference_tuple = ast.literal_eval(add_reference_data)

    # Create commit object
    commit_file_data = str(
        ("commit", message[0], add_reference_tuple[0], add_reference_tuple[1], "past_commit", past_commit_hash)
    )
    commit_file_hash = hashlib.sha1()
    commit_file_hash.update(commit_file_data.encode())
    commit_file_hash = commit_file_hash.hexdigest()
    if not os.path.exists(f".lit/{LOCAL_REPOSITORY}/objects/{commit_file_hash[:2]}"):
        os.makedirs(f".lit/{LOCAL_REPOSITORY}/objects/{commit_file_hash[:2]}")

    with open(f".lit/{LOCAL_REPOSITORY}/objects/{commit_file_hash[:2]}/{commit_file_hash[2:]}", "w") as commit_file:
        commit_file.write(commit_file_data)

    os.system(f"rm .lit/add_reference")

    with open(f".lit/HEAD", "w") as head_file:
        head_file.write(commit_file_hash)
