"""Class to manage writing to files."""

from pathlib import PosixPath


class FileOutput:
    """Class Object for file output"""

    write_to_file = False
    path = None

    def __init__(self) -> None:
        self.file_name = None

    @staticmethod
    def __path_is_valid(output_path: PosixPath) -> bool:
        """Check if the path provided is valid."""
        return output_path.exists()

    def set_output_path(self, output_path: str) -> None:
        """Set the output path for FileOutput class."""
        path = PosixPath(output_path).expanduser()
        if self.__path_is_valid(path):
            FileOutput.path = path

    def set_write_to_file_flag(self, flag: bool) -> None:
        """Set the write to file flag."""
        FileOutput.write_to_file = flag

    def set_file_name(self, playlist_name: str) -> None:
        """Set the file name to be playlist name."""
        self.file_name = f"{playlist_name.replace(' ', '_').replace('/', '-')}_analysis"

    def create_file(self) -> None:
        """Create empty file."""
        if FileOutput.write_to_file:
            with open(
                self.path.joinpath(f"{self.file_name}.txt"),
                "w",
                encoding="utf-8",
            ) as f:
                f.writelines("")
                f.close()
        return

    def write(self, to_write: str) -> None:
        """Write string to the file."""
        if FileOutput.write_to_file:
            with open(
                self.path.joinpath(f"{self.file_name}.txt"),
                "a",
                encoding="utf-8",
            ) as f:
                f.writelines(to_write)
                f.close()
        return
