from pathlib import Path
from . import ConfigContainer


class PathContainer(ConfigContainer):
    """Container which converts all values with type ``str`` to ``Path`` objects.
    Relative paths will be resolved in relation to the folder where the config file is."""
    def __init__(self):
        super().__init__()
        self.parent_folder: Path = None

    def on_set_value(self, var_name: str, new_value):
        """"""  # Empty docstring otherwise autodoc shows the docstring from the base class
        if not isinstance(new_value, (str, Path)):
            return new_value

        # Make path from str
        path = Path(new_value) if isinstance(new_value, str) else new_value

        if not path.is_absolute():
            path = self.parent_folder / path
        return path.resolve()

    def _set_default_path(self, path: Path):
        if self.parent_folder is None:
            self.parent_folder = path
