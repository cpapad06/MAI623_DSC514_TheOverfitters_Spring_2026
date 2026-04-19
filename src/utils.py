from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from pyspark.sql import DataFrame as SparkDataFrame
    from pyspark.sql import SparkSession

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
            if path.exists():
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


class SparkData(Data):
    """Mirror of ``Data`` backed by Spark DataFrames."""

    __slots__ = ("spark",)
    DATA_DIR: Path = DATA_DIR

    def __init__(
        self,
        spark: "SparkSession",
        /,
        agents: "SparkDataFrame | None" = None,
        comments: "SparkDataFrame | None" = None,
        posts: "SparkDataFrame | None" = None,
        submolts: "SparkDataFrame | None" = None,
    ):
        super().__init__(agents=agents, comments=comments, posts=posts, submolts=submolts)
        self.spark = spark

    def load(self, tag: str):
        for d in Data.__slots__:
            path = self.DATA_DIR / f"{d}-{tag}.parquet"
            if path.exists():
                try:
                    sdf = self.spark.read.parquet(str(path))
                except Exception as exc:
                    if "TIMESTAMP(NANOS" not in str(exc):
                        raise
                    print(f"Spark parquet reader hit nanos timestamps for {d}; using pandas fallback.")
                    pdf = pd.read_parquet(path)
                    for c in pdf.columns:
                        if pd.api.types.is_datetime64_any_dtype(pdf[c]):
                            pdf[c] = pd.to_datetime(pdf[c], errors="coerce").dt.floor("us")
                    sdf = self.spark.createDataFrame(pdf)
                setattr(self, d, sdf)
                print("Loaded:", path)
        return self

    def save(self, tag: str):
        for d in Data.__slots__:
            df = getattr(self, d)
            if df is None:
                continue
            path = self.DATA_DIR / f"{d}-{tag}.parquet"
            df.write.mode("overwrite").parquet(str(path))
            print("Saved:", path)

    def copy(self):
        # Spark DataFrames are immutable plans; shallow reference copy is typically enough.
        return SparkData(
            self.spark,
            agents=self.agents,
            comments=self.comments,
            posts=self.posts,
            submolts=self.submolts,
        )