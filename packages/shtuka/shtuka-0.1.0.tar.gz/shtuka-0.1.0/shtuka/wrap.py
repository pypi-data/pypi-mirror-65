"""Functions and classes for wrappers instantiating."""

import keyword

from shtuka import core
from shtuka import utils

from typing import Any, NamedTuple  # isort:skip


class Setup(NamedTuple):
    """Wrappers creation settings."""

    frozen: bool = False
    strict: bool = False
    validate: bool = False

    def empty(self) -> core.GMissing:
        """Creates empty wrapper.

        Returns:
            Empty shtuka wrapper.

        """

        return core.GMissing(self)

    def cook(self, data: Any) -> Any:
        """Wrap input data with current setup.

        Args:
            data: Data to cook.

        Returns:
            Wrapped data.

        """

        if isinstance(data, list):
            return self.__cook_list(data)
        elif isinstance(data, dict):
            return self.__cook_dict(data)
        else:  # Cook entity.
            return data if self.strict else core.GLeaf(self, data)

    def __cook_list(self, data):
        if self.frozen:
            return core.GFrozenList(self, data)
        else:
            return core.GList(self, data)

    def __cook_dict(self, data):
        if self.frozen:
            cooked_dict = core.GFrozenDict(self, data)
        else:
            cooked_dict = core.GDict(self, data)

        if self.validate:
            forbidden_attributes = utils.find_forbidden_attributes(
                data=data,
                forbidden_keys=set(dir(cooked_dict)) | set(keyword.kwlist),
            )
            if len(forbidden_attributes):
                raise ValueError(
                    "Data dict contains forbidden attributes: "
                    f"'{forbidden_attributes}'."
                )

        return cooked_dict


def cook(
    data: Any,
    *,
    frozen: bool = False,
    strict: bool = False,
    validate: bool = False,
) -> Any:
    """Wraps raw python object to one of shtuka wrapper.

    Args:
        data: Raw python object. Could be list or dict to be considered
            as internal shtuka tree inner node. Any other type would be
            considered a leaf (either mutable or immutable).
        frozen: True if make object immutable. Immutability copies all
            inner list/dict nodes and checks leafs hashability. Any
            further converting to raw data will return copy as well to
            prevent changing.
        strict: True if create strict shtuka wrapper. Strict one would
            not wrap leafs and produce an error for missing keys
            (either for lists or dicts). Non-strict one, otherwise,
            would wrap every leaf and output an empty node for missing
            keys.
        validate: True if validate for attribute usage. Raises an error
            if meets a dict key that cannot be accessed as attribute.
            Validation goes in lazy manner, checking only those nodes
            for which wrappers were created.

    Returns:
        High-level shtuka wrapper.

    Raises:
        TypeError: When input data doesn't comply with kwargs params.

    """

    if isinstance(data, core.GABC):  # Recooking the data.
        data = data.raw_

    if frozen:
        data = utils.tree_copy(data)
        for parents, leaf in utils.gen_leafs(data):
            if not utils.is_hashable(leaf):
                raise TypeError(
                    f"Element {leaf} at position {parents} isn't hashable."
                )

    setup = Setup(frozen, strict, validate)
    return setup.cook(data)


def raw(entity: Any) -> Any:
    """Performs the reverse-`cook` operation and undone the wrapping.

    Args:
        entity: Entity to unwrap.

    Returns:
        Raw object without shtuka wrappers.

    """

    if isinstance(entity, core.GABC):
        return entity.raw_
    else:
        return entity


class glist(core.GList):  # noqa
    """List constructor with non-strict wrapping."""

    __slots__ = ()

    def __init__(self, *args, **kwargs):
        """Creates a list of elements.

        Args:
            *args: Args to propagate to :obj:`list` constructor.
            **kwargs: Kwargs to propagate to :obj:`list` constructor.

        """

        # noinspection PyArgumentList
        setup = Setup()
        data = list(*args, **kwargs)
        super().__init__(setup, data)


class gfrozenlist(core.GFrozenList):  # noqa
    """Frozen list constructor with non-strict wrapping."""

    __slots__ = ()

    def __init__(self, *args, **kwargs):
        """Creates a frozen list of elements.

        Args:
            *args: Args to propagate to :obj:`list` constructor.
            **kwargs: Kwargs to propagate to :obj:`list` constructor.

        """

        # noinspection PyArgumentList
        setup = Setup(frozen=True)
        data = list(*args, **kwargs)
        super().__init__(setup, data)


class gdict(core.GDict):  # noqa
    """Dict constructor with non-strict wrapping."""

    __slots__ = ()

    def __init__(self, *args, **kwargs):
        """Creates a dict of elements.

        Args:
            *args: Args to propagate to :obj:`dict` constructor.
            **kwargs: Kwargs to propagate to :obj:`dict` constructor.

        """

        # noinspection PyArgumentList
        setup = Setup()
        data = dict(*args, **kwargs)
        super().__init__(setup, data)


class gfrozendict(core.GFrozenDict):  # noqa
    """Frozen dict constructor with non-strict wrapping."""

    __slots__ = ()

    def __init__(self, *args, **kwargs):
        """Creates a frozen dict of elements.

        Args:
            *args: Args to propagate to :obj:`dict` constructor.
            **kwargs: Kwargs to propagate to :obj:`dict` constructor.

        """

        # noinspection PyArgumentList
        setup = Setup(frozen=True)
        data = dict(*args, **kwargs)
        super().__init__(setup, data)
