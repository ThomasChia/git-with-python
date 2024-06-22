from dataclasses import dataclass


@dataclass
class LitTree:
    parent: str
    object_name: str
    object_type: str


@dataclass
class LitTreeEntry:
    object_type: str
    object_reference: str
    object_name: str


@dataclass
class LitCommit:
    type: str
    message: str
    tree_reference: str
    past_commit_reference: str
