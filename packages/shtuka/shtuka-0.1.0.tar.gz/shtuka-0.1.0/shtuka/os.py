"""Functions related memory operations like reading and writing."""

import json
import pathlib
from typing import Union

import yaml

from shtuka import core
from shtuka import wrap

SUPPORTED_SUFFIXES = ('.json', '.yml', '.yaml')


def load(
    path: Union[str, pathlib.Path], encoding: str = 'utf-8', **kwargs,
) -> Union[core.GDict, core.GFrozenDict]:
    """Reads and parses config from the filesystem.

    Args:
        path: Path to config.
        encoding: Encoding for reading.
        **kwargs: Other arguments to pass to cook method.

    Returns:
        Config dict.

    Raises:
        FileNotFoundError: When no such file exists.
        ValueError: When file format is unsupported.

    Examples:
        >>> import shtuka
        >>> shtuka.load('configs/config.yml', strict=False)
        GDict(data={[...]}, [...])

    """

    path = pathlib.Path(path)

    if not path.exists():
        raise FileNotFoundError(f"No such file exists: '{path}'.")

    if path.suffix not in SUPPORTED_SUFFIXES:
        raise ValueError(
            "Unsupported file format, "
            f"should be one of '{SUPPORTED_SUFFIXES}'."
        )

    with path.open(encoding=encoding) as stream:
        if path.suffix == '.json':
            data = json.load(stream)
        else:  # path.suffix in ('.yml', '.yaml')
            data = yaml.load(
                stream=stream, Loader=getattr(yaml, 'CLoader', yaml.Loader)
            )

    config = wrap.cook(data, **kwargs)

    return config


def save(
    config: Union[core.GDict, core.GFrozenDict],
    path: Union[str, pathlib.Path],
    encoding: str = 'utf-8',
    ensure_ascii: bool = False,
    indent: int = 2,
) -> None:
    """Saves given config to local path.

    Args:
        config: Config to save.
        path: Path to save to.
        encoding: Encoding for reading.
        ensure_ascii: Checks only-ascii coding.
        indent: Number of spaces to use for indent.

    Returns:
        None

    Raises:
        ValueError: When tries to save non-dict structure.
        ValueError: When file format is unsupported.

    Examples:
        >>> import shtuka
        >>> import tempfile
        >>> config = shtuka.cook({'key': 'value'})
        >>> with tempfile.TemporaryDirectory() as d:
        ...     shtuka.save(config, f'{d}/config.yml')

    """

    if not isinstance(config, (core.GDict, core.GFrozenDict)):
        raise ValueError(
            f"Could only save dict instances, not '{type(config)}'."
        )

    path = pathlib.Path(path)

    if path.suffix not in SUPPORTED_SUFFIXES:
        raise ValueError(
            "Unsupported file format, "
            f"should be one of '{SUPPORTED_SUFFIXES}'."
        )

    with path.open(encoding=encoding, mode='w') as stream:
        if path.suffix == '.json':
            json.dump(
                config.raw_, stream, indent=indent, ensure_ascii=ensure_ascii
            )
        else:  # path.suffix in ('.yml', '.yaml')
            yaml.dump(
                data=config.raw_,
                stream=stream,
                Dumper=getattr(yaml, 'CDumper', yaml.Dumper),
            )
