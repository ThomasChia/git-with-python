import ast
import hashlib
import os
from dataclasses import asdict
from typing import Dict, List, NamedTuple

from dotenv import load_dotenv
from loguru import logger

from lit.lit_config import HEAD_DIRECTORY, IGNORED_DIRS, STAGING_DIRECTORY
from lit.utils import LitTree

load_dotenv()


class ObjectHash(NamedTuple):
    object_name: str
    relative_path: str
    hash: str
    object_type: str
    parent_path: str


def add_to_staging():
    path = os.getcwd()
    files_and_hashes = get_files_and_hashes(path, ignored_dirs=IGNORED_DIRS)

    current_tree = []
    current_tree_hash = hashlib.sha1()
    for file_hash in files_and_hashes:
        dir_path = file_hash.hash[:2]
        if not os.path.exists(f".lit/{STAGING_DIRECTORY}/objects/{dir_path}"):
            os.makedirs(f".lit/{STAGING_DIRECTORY}/objects/{dir_path}")
        if file_hash.object_type == "file":
            os.system(f"cp {file_hash.relative_path} .lit/{STAGING_DIRECTORY}/objects/{dir_path}/{file_hash.hash[2:]}")
        elif file_hash.object_type == "directory":
            # Find all objects with this directory as the parent and create a sub tree for all those elements
            sub_tree = []
            for sub_file in files_and_hashes:
                if sub_file.parent_path == file_hash.relative_path:
                    sub_tree.append((sub_file.object_type, sub_file.hash, sub_file.object_name))

            # Save file
            dir_path = file_hash.hash[:2]
            if not os.path.exists(f".lit/{STAGING_DIRECTORY}/objects/{dir_path}"):
                os.makedirs(f".lit/{STAGING_DIRECTORY}/objects/{dir_path}")
            with open(f".lit/{STAGING_DIRECTORY}/objects/{dir_path}/{file_hash.hash[2:]}", "w") as tree_file:
                for item in sub_tree:
                    tree_file.write(str(item) + "\n")

        if file_hash.parent_path == "":
            current_tree.append((file_hash.object_type, file_hash.hash, file_hash.object_name))
            current_tree_hash.update(file_hash.hash.encode())

    current_tree_reference = current_tree_hash.hexdigest()

    # Check if there are any changes to current state and remove from staging if not
    if os.path.isdir(f".lit/{HEAD_DIRECTORY}/head_reference"):
        with open(f".lit/{HEAD_DIRECTORY}/head_reference", "r") as head_reference:
            head_path = head_reference.read().split(": ")[-1]
            with open(f".lit/{head_path}", "r") as add_reference_file:
                add_reference = add_reference_file.read()

        if current_tree_reference == add_reference:
            os.system(f"rm -r .lit/{STAGING_DIRECTORY}/objects/*")
            logger.warning("Nothing new to add, removing files from staging.")
            return

    # Save file
    dir_path = current_tree_reference[:2]
    if not os.path.exists(f".lit/{STAGING_DIRECTORY}/objects/{dir_path}"):
        os.makedirs(f".lit/{STAGING_DIRECTORY}/objects/{dir_path}")
    with open(f".lit/{STAGING_DIRECTORY}/objects/{dir_path}/{current_tree_reference[2:]}", "w") as tree_file:
        for item in current_tree:
            tree_file.write(str(item) + "\n")

    # Create add reference object
    with open(".lit/add_reference", "w") as add_reference_file:
        add_reference_file.write(str(("tree", current_tree_reference)))


def get_files_and_hashes(path: str, ignored_dirs: List[str]) -> List[ObjectHash]:
    files_and_hashes = []
    for root, dirs, files in os.walk(path):
        files[:] = [f for f in files if f not in ignored_dirs]
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, path)
            file_reference = hash_file_sha1(full_path)
            logger.info(f"{relative_path}, {file_reference}")
            files_and_hashes.append(
                ObjectHash(
                    object_name=file,
                    relative_path=relative_path,
                    hash=file_reference,
                    object_type="file",
                    parent_path=os.path.dirname(relative_path),
                )
            )

        for dir in dirs:
            # Recursively get files and directories
            directory_hash_list = get_files_and_hashes(dir, ignored_dirs=ignored_dirs)

            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, path)
            sha1_hash = hashlib.sha1()
            for directory in directory_hash_list:
                sha1_hash.update(directory.hash.encode())
            directory_reference = sha1_hash.hexdigest()

            files_and_hashes.append(
                ObjectHash(
                    object_name=dir,
                    relative_path=relative_path,
                    hash=directory_reference,
                    object_type="directory",
                    parent_path=os.path.dirname(relative_path),
                )
            )

    return files_and_hashes


def hash_file_sha1(filepath):
    with open(filepath, "rb") as f:
        file = f.read()
        sha1_hash = hashlib.sha1()
        sha1_hash.update(file)
        hash_value = sha1_hash.hexdigest()
    return hash_value
