from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class File:
    """A class to manage S3 file as a local file.

    Parameters
    ----------
    path : str | Path
        The path of the file. A local path or path to the S3 (s3://...) can be used.
    s3_profile : str | None
        Profile name for S3 session.
    max_trials : int
        The maximum number of trials to download the file from S3.
        If the download fails by CredentialRetrievalError (it can occur by
        failing to access meta data API while multi-processing),
        the file is downloaded again.
    """

    path: str | Path
    s3_profile: str | None = None
    max_trials: int = 10

    def __post_init__(self) -> None:
        self.orig_path = self.path
        self.path = self.fix_path(self.path)
        self.tmp_file: tempfile._TemporaryFileWrapper[bytes] | None = None
        if self.path.startswith("s3:"):
            self.path = self.download_s3_file()

    def __del__(self) -> None:
        if self.tmp_file is not None:
            self.tmp_file.close()

    @staticmethod
    def fix_path(path: str | Path) -> str:
        if not path:
            return ""
        # remove double slash during the path (other than starting of s3://)
        if ":/" in str(path):
            pathes = str(path).split(":/")
            return f"{pathes[0]}:/{Path(pathes[1])}"
        return str(Path(path))

    @staticmethod
    def extract_s3_info(path: str | Path) -> tuple[str, str, str]:
        path = str(path)
        split_path = path.split("/")
        bucket_name = split_path[2]
        file_name = "/".join(split_path[3:])
        file_extension = split_path[-1].split(".")[-1]
        return bucket_name, file_name, file_extension

    def download_s3_file(self) -> str:
        # boto3.session.Session(profile_name=self.s3_profile).resource("s3") uses random.
        # To avoid unnoticed change of random state, restore random state after the process.
        import random

        import boto3
        from botocore.config import Config

        state = random.getstate()

        bucket_name, file_name, file_extension = self.extract_s3_info(
            self.path
        )
        temp_file = tempfile.NamedTemporaryFile(suffix=f".{file_extension}")

        s3 = boto3.session.Session(profile_name=self.s3_profile).resource(
            "s3", config=Config(retries={"mode": "standard"})
        )
        bucket = s3.Bucket(bucket_name)
        bucket.download_file(file_name, temp_file.name)
        self.tmp_file = temp_file

        random.setstate(state)

        return temp_file.name
