from pathlib import Path
import typing

import voluptuous

from . import EasyCoConfig


def convert_to_path(str_obj) -> Path:
    if not isinstance(str_obj, str):
        raise voluptuous.Invalid(f'Input for Path must be str not {type(str_obj)}')
    return Path(str_obj)


class MissingType:
    def __repr__(self):
        return 'MISSING'


MISSING = MissingType()


class SkipVariableType:
    def __repr__(self):
        return 'Skipped'


SKIP = SkipVariableType()


class ConfigEntry:

    def __init__(self, default=MISSING, default_factory: typing.Callable[[], typing.Any] = MISSING, validator = MISSING,
                 required: bool = True, description: str = '', key_name: typing.Optional[str] = None):
        """ConfigEntry

        :param default: Default value for this entry
        :param default_factory: Factory function which creates the default value, use for list, dict, etc.
        :param validator: validator which validates the loaded values
        :param required: is this entry required
        :param description: description of this entry which will also be added to the config file as a comment
        :param key_name: key name in the config file
        """
        assert isinstance(description, str), type(description)
        assert isinstance(required, bool), type(required)

        # can't use both
        if default is not MISSING and default_factory is not MISSING:
            raise ValueError('cannot specify both default and default_factory')

        if default is not MISSING and not isinstance(default, (bool, str, int, float, Path)):
            raise ValueError('use parameter default_factory for mutable types')

        self.default = default
        self.default_factory: typing.Callable[[], typing.Any] = default_factory
        self.validator = validator

        self.required: bool = required
        self.description: str = description

        self.name: typing.Optional[str] = key_name
        self.type = None

        # # so we can enter '5' and still get a proper int value
        # if self.value_type is float or self.value_type is int:
        #     self.validator = voluptuous.Coerce(self.value_type)

    def __repr__(self):
        ret = f'<{self.__class__.__name__} '
        for k, v in sorted(self.__dict__.items()):
            ret += f'{k}: {v}, '
        return ret[:-2] + ' >'

    def get_key_name(self, cfg: EasyCoConfig):
        if cfg.lower_case_keys:
            return self.name.lower()
        return self.name

    def set_type_hint(self, var_name, var_type):
        # name can already be set through constructor
        if self.name is None:
            self.name = var_name

        # type is mandatory
        self.type = var_type

        # Validator is already set -> don't overwrite it
        if self.validator is not MISSING:
            return None

        # we load strings instead of Path objects
        if self.type is Path:
            self.validator = convert_to_path
            return None

        # propably a type-hint, support lists and dict
        if hasattr(self.type, '__origin__') and hasattr(self.type, '__args__'):
            origin = getattr(self.type, '__origin__')
            args = getattr(self.type, '__args__')

            if origin is list or origin is typing.List:
                self.validator = [args[0]]
                return None
            if origin is set or origin is typing.Set:
                self.validator = {args[0]}
                return None
            if origin is dict or origin is typing.Dict:
                self.validator = {args[0]: args[1]}
                return None

        # use type as validator
        self.validator = self.type
        return None

    def set_validator(self, data: dict, cfg: EasyCoConfig) -> dict:
        assert isinstance(cfg, EasyCoConfig), type(cfg)

        default = voluptuous.UNDEFINED
        if self.default is not MISSING:
            default = self.default
        if self.default_factory is not MISSING:
            default = self.default_factory()

        key = (voluptuous.Required if self.required else voluptuous.Optional)(
            schema=self.get_key_name(cfg), description=self.description, default=default)
        data[key] = self.validator
        return data

    def set_default(self, data: dict, cfg: EasyCoConfig) -> bool:
        assert isinstance(cfg, EasyCoConfig), type(cfg)

        # skip if we don't have a default value
        if self.default is MISSING and self.default_factory is MISSING:
            return False

        # respect option to only create required keys
        if not self.required and not cfg.create_optional_keys:
            return False

        # value is already there -> do nothing
        name = self.get_key_name(cfg)
        if name in data:
            return False

        # set default value for entry
        if self.default is not MISSING:
            data[name] = str(self.default) if isinstance(self.default, Path) else self.default
        if self.default_factory is not MISSING:
            data[name] = self.default_factory()

        # add description as yaml comment, only set comment if there is none
        if self.description:
            if name not in data.ca.items:
                data.yaml_add_eol_comment(self.description, name)
                # -> only add comments if we add a value, too
                # changed = True

        return True
