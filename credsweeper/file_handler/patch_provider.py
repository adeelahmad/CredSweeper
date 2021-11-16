from typing import Dict, List, Optional

from credsweeper.file_handler.files_provider import FilesProvider
from credsweeper.file_handler.diff_content_provider import DiffContentProvider
from credsweeper.utils import Util


class PatchProvider(FilesProvider):
    """Provider of patch files class

    Attributes:
        paths: list of string, list of path of patch files to scan
        change_type: string, type of analyses changes in patch (added or deleted)
        skip_ignored: boolean variable, Checking the directory to the list
            of ignored directories from the gitignore file
    """
    def __init__(self,
                 paths: List[str],
                 change_type: Optional[str] = None,
                 skip_ignored: Optional[bool] = None) -> None:
        """Initialize Files Patch Provider for patch files from 'paths'

        Args:
            paths: list of string, list of path of patch files to scan
            change_type: string, type of analyses changes in patch (added or deleted)
            skip_ignored: boolean variable, Checking the directory to the list
                of ignored directories from the gitignore file
        """
        self.paths = paths
        self.change_type = change_type

    def load_patch_data(self) -> List[List[str]]:
        raw_patches = []
        for file_path in self.paths:
            raw_patches.append(Util.read_patch_file(file_path))
        return raw_patches

    def get_files_sequence(self, raw_patches: List[str]) -> List[DiffContentProvider]:
        files = []
        for raw_patch in raw_patches:
            files_data = Util.patch2files_diff(raw_patch, self.change_type)
            for file_path, file_diff in files_data.items():
                files.append(DiffContentProvider(file_path=file_path, change_type=self.change_type, diff=file_diff))
        return files

    def get_scannable_files(self, config: Dict) -> List[DiffContentProvider]:
        """Get list of file object for analysis based on initial value "paths"

        Args:
            config: dict of credsweeper configuration

        Return:
            files: list of DiffContentProvider, file objects for analysis
        """
        diff_data = self.load_patch_data()
        files = self.get_files_sequence(diff_data)
        return files
