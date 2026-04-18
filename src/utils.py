from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pandas as pd

def repo_root() -> Path:
    """Directory that contains `requirements.txt` (repository root)."""
    env = os.environ.get("QUARTO_PROJECT_ROOT")
    if env:
        p = Path(env).resolve()
        if (p / "requirements.txt").is_file():
            return p
    cwd = Path.cwd().resolve()
    if (cwd / "requirements.txt").is_file():
        return cwd
    if (cwd.parent / "requirements.txt").is_file():
        return cwd.parent
    return cwd


ROOT = repo_root()
DATA_DIR = ROOT / "data"
PROCESSED_DATA_PATH = DATA_DIR / "moltbook_cleaned.parquet"
RAW_POSTS_PATH = DATA_DIR / "posts-raw.parquet"
POSTS_NORMALIZED_PATH = DATA_DIR / "posts-normalized.parquet"


class Data:
    DATA_DIR: Path = DATA_DIR

    __slots__ = ('agents', 'comments', 'posts', 'submolts')
    
    def __init__(self, /, agents: pd.DataFrame | None = None, comments: pd.DataFrame | None = None, posts: pd.DataFrame | None = None, submolts: pd.DataFrame | None = None):
        self.agents = agents
        self.comments = comments
        self.posts = posts
        self.submolts = submolts

    def __getitem__(self, key):
        if key not in self.__slots__:
            raise KeyError(f"'{key}' is not a valid field in {self.__class__.__name__}")
        return getattr(self, key)

    def __setitem__(self, key, value):
        if key not in self.__slots__:
            raise KeyError(f"'{key}' is not a valid field in {self.__class__.__name__}")
        setattr(self, key, value)

    def keys(self):
        return self.__slots__

    def load(self, tag: str):
        for d in self.__slots__:
            path = self.DATA_DIR / f'{d}-{tag}.parquet'
            if path.is_file():
                setattr(self, d, pd.read_parquet(path))
                print('Loaded:', path)

        return self
    
    def save(self, tag:str):
        for d in self.__slots__:
            if getattr(self, d) is None:
                continue

            path = self.DATA_DIR / f'{d}-{tag}.parquet'
            getattr(self, d).to_parquet(path, index=True)
            print('Saved:', path)

    def copy(self):
        return Data(
            agents=self.agents if self.agents.copy() is not None else None,
            comments=self.comments if self.comments.copy() is not None else None,
            posts=self.posts if self.posts.copy() is not None else None,
            submolts=self.submolts if self.submolts.copy() is not None else None,
        )