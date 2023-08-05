import io
import typing
from pathlib import Path

import ruamel.yaml
import voluptuous

import EasyCo
from .yaml import yaml_rt as yaml


class ConfigFile(EasyCo.ConfigContainer):

    def __init__(self, path: Path = None):
        super().__init__()
        if path is not None:
            self.set_path(path)

    def set_path(self, path: typing.Union[Path, str]):
        """Set the path to the configuration file.
        If no file extension is specified ``.yml`` will be automatically appended.

        :param path: Path obj or str
        """
        if isinstance(path, str):
            path = Path(path)
        assert isinstance(path, Path), type(path)

        self._path = path.resolve()
        if self._path.suffix == '':
            self._path = self._path.with_name(self._path.name + '.yml')

        # set default path for all file containers
        self._call_container_funcs('_set_default_path', self._path.parent)

    def load(self, path: Path = None):
        """Load values from the configuration file. If the file doesn't exist it will be created.
        Missing required config entries will also be created.

        :param path: if not already set a path instance to the config file
        """
        if path is not None:
            self.set_path(path)
        assert self._path is not None

        cfg = ruamel.yaml.comments.CommentedMap()
        if not self._path.parent.is_dir():
            raise FileNotFoundError(f'Configuration folder {self._path.parent} does not exist!')

        if self._path.is_file():
            with self._path.open('r', encoding='utf-8') as file:
                cfg = yaml.load(file)
            if cfg is None:
                cfg = ruamel.yaml.comments.CommentedMap()

        # add default values
        data_changed = self._update_yaml(cfg, insert_values=False)

        # validate - this also makes it a normal dict
        schema = {}
        self._update_schema(schema, insert_values=False)
        schema = voluptuous.Schema(schema)
        validated_cfg = schema(cfg)

        # update optional keys if we have them and write back to disk
        if data_changed:
            with self._path.open('w', encoding='utf-8') as file:
                yaml.dump(cfg, file)

        self._set_value(validated_cfg)

    def _print_created_cfg(self):
        cfg = ruamel.yaml.comments.CommentedMap()
        self._update_yaml(cfg, insert_values=False)

        tmp = io.StringIO()
        yaml.dump(cfg, tmp)
        output = tmp.getvalue()
        print(output)
