"""Utils module"""
import os

from ticketreader import exceptions

class FileHandlerMixin():
    """File handler mixin"""

    VALID_EXTENSIONS = []

    @property
    def file_path(self) -> os.PathLike:
        """File path"""
        if not hasattr(self, "_file_path"):
            raise AttributeError("File path not set")
               
        return self._file_path
    
    @file_path.setter
    def file_path(self, file_path: os.PathLike) -> None:
        """File path"""
        self._validate_file_path(file_path=file_path)
        
        self._file_path = file_path

    def _validate_file_path(self, file_path: os.PathLike) -> None:
        """Validate file path"""
        if not isinstance(file_path, os.PathLike):
            raise TypeError("File path must be a PathLike")
        
        if not os.path.exists(file_path):
            raise ValueError("File path does not exist")
        
        self._validate_file_extension(file_path=file_path)

    def _validate_file_extension(self, file_path: os.PathLike) -> None:
        """Validate file extension"""
        _, file_extension = os.path.splitext(file_path)
        if file_extension not in self.VALID_EXTENSIONS:
            raise exceptions.WrongFileExtension(f"File extension {file_extension} not valid. Valid extensions are: {self.VALID_EXTENSIONS}")