import typing
from pathlib import Path

import ruamel.yaml
import voluptuous

yaml_rt = ruamel.yaml.YAML(typ='rt')
yaml_safe = ruamel.yaml.YAML(typ='safe')

for __loader in (yaml_rt, yaml_safe):
    __loader.default_flow_style = False
    __loader.default_style = False
    __loader.width = 1000000
    __loader.allow_unicode = True
    __loader.sort_base_mapping_type_on_output = False


def safe_load(path: Path, validator: typing.Optional[voluptuous.Schema] = None) -> typing.Union[dict, list, None]:
    with path.open('r', encoding='utf-8') as file:
        ret = yaml_safe.load(file)
    if validator is not None:
        ret = validator(ret)
    return ret
