"""Core shtuka classes."""

import abc
from collections import abc as collections_abc
import functools
import weakref

from shtuka import meta

from typing import Any, Union  # isort:skip


# https://github.com/python/mypy/issues/8539
@functools.total_ordering  # type: ignore
class GABC(metaclass=abc.ABCMeta):
    """General abstact shtuka wrapper."""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Collects fields (statically) from slots.
        cls.__fields__ = meta.Fields(cls)

    __slots__ = ('_setup', '__weakref__')

    def __init__(self, setup):
        """Init base shtuka class with setup setting.

        Args:
            setup: Setup settings.

        """

        super().__init__()

        self._setup = setup

    def __repr__(self):
        clazz = type(self)
        properties_str = ', '.join(
            '{}={}'.format(field[1:], repr(getattr(self, field, None)))
            for field in clazz.__fields__
        )
        return '{}({})'.format(clazz.__name__, properties_str)

    @abc.abstractmethod
    def __str__(self):
        pass

    @abc.abstractmethod
    def __eq__(self, other):
        pass

    @abc.abstractmethod
    def __lt__(self, other):
        pass

    @abc.abstractmethod
    def __bool__(self):
        pass

    @abc.abstractmethod
    def __getitem__(self, item):
        pass

    def __getattr__(self, item):
        if item in type(self).__fields__:
            return object.__getattribute__(self, item)
        else:
            return self.__getitem__(item)

    # -------------------- Change state functions ------------------- #

    @abc.abstractmethod
    def apply_(self, f: Union[str, meta.Function]) -> 'GABC':
        """Applies (non-inplace) function and outputs wrapped result.

        Args:
            f: Function to apply.

        Returns:
            Wrapped result.

        """

    def coerce_(self, f: Union[str, meta.Function]) -> 'GABC':
        """Makes a coercion with type function and empty on failing.

        Coercion is considered fail when caught exception is either
        :exc:`TypeError` or :exc:`ValueError`.

        Args:
            f: Function to do coercion with.

        Returns:
            Wrapped coercion result or empty entity.

        """

        try:
            return self.apply_(f)
        except (TypeError, ValueError):
            return self._setup.empty()

    def check_(
        self, f: Union[str, meta.Filter] = meta.IS_NOT_NONE_F
    ) -> "GABC":
        """Checks wrapped element with True/False filter.

        Args:
            f: Filter function to check with.

        Returns:
            Same element on True, empty entity on False.

        """

        return self if self.f_(f) else self._setup.empty()

    # -------------------- Finalization functions ------------------- #

    @property
    @abc.abstractmethod
    def raw_(self) -> Any:
        """Extracts raw python object from shtuka wrapper.

        Returns:
            A python object inside wrapper.

        Raises:
            ValueError: If tried to convert empty entity.

        """

    def f_(self, f: Union[str, meta.Function]) -> Any:
        """Alias for applying :meth:`apply_` following by :meth:`raw_`.

        Args:
            f: Function to pass to apply.

        Returns:
            Raw unwrapped function result.

        """

        return self.apply_(f).raw_

    @property
    def miss_(self) -> bool:
        """Checks if shtuka wrapper contains an element.

        Returns:
            True if requested element is missing.

        """

        try:
            # noinspection PyUnusedLocal
            _ = self.raw_
            return False
        except ValueError:
            return True

    @property
    def blank_(self) -> bool:
        """Checks if shtuka wrapper contains an element or None.

        Returns:
            True if requested element is missing or is None.

        """

        return self.miss_ or self.f_(meta.IS_NONE_F)

    def or_(self, default) -> Any:
        """Chooses output between raw element or default one if missing.

        Args:
            default: Output when element is missing.

        Returns:
            Raw element or default if missing.

        """

        return default if self.miss_ else self.raw_

    def alt_(self, default) -> Any:
        """Chooses output between raw element or default one if blank.

        Args:
            default: Output when element is blank.

        Returns:
            Raw element or default if blank.

        """

        return default if self.blank_ else self.raw_


class GMissing(meta.FieldsSetDelMixin, GABC):
    """Class for denoting empty wrapper or missing key.

    Although class derived from set/del mixin, which forces it to
    implement getters and setter, it is still immutable by design.
    Because of that, it is also hashable.

    Any two instances of this class should be treated as equal.

    """

    __slots__ = ('_parent_ref', '_missed_key', '_last_missed', meta.HASH_FIELD)

    def __init__(self, setup, parent=None, missed_key=None):
        """Inits missing wrapper with setup setting.

        Args:
            setup: Setup setting.
            parent: Parent wrapper.
            missed_key: Key name that invokes missing key wrapper
                creation.

        """

        super().__init__(setup)

        self._parent_ref = None if parent is None else weakref.ref(parent)
        self._missed_key = missed_key

        # Forward link for GC to not delete new missing object.
        self._last_missed = None

    @property
    def _parent(self):
        return None if self._parent_ref is None else self._parent_ref()

    def __str__(self):
        raise ValueError("Cant cast missing value to string.")

    def __eq__(self, other):
        if isinstance(other, GMissing):
            return True

        return False

    def __lt__(self, other):
        raise TypeError(
            f"'<' not supported between instances of "
            f"'{type(self)}' and '{type(other)}'."
        )

    def __bool__(self):
        return False

    def __getitem__(self, key):
        self._last_missed = GMissing(self._setup, self, key)
        return self._last_missed

    def apply_(self, f: Union[str, meta.Function]) -> 'GABC':
        """See base class."""
        return self._setup.empty()

    @property
    def raw_(self) -> Any:
        """See base class."""
        raise ValueError("Cant get a raw object from missing wrapper.")

    @meta.memoize(field=meta.HASH_FIELD)
    def __hash__(self):
        return hash(None)

    def __setitem__(self, key, value):
        if self._parent is None:
            raise ValueError("Cant set a value to an empty wrapper.")

        final_value, current_node = {key: value}, self
        while isinstance(current_node._parent, GMissing):
            final_value = {current_node._missed_key: final_value}
            current_node = current_node._parent

        current_node._parent[current_node._missed_key] = final_value

    def __delitem__(self, key):
        raise ValueError("Cant del a value to an empty wrapper.")


class GEntity(GABC):
    """Base abstract class for non-empty wrappers."""

    __slots__ = ('_data',)

    def __init__(self, setup, data):
        """Inits entity with setup setting and data object.

        Args:
            setup: Setting setup.
            data: Data object.

        """

        super().__init__(setup)

        self._data = data

    def __str__(self):
        return str(self._data)

    def __eq__(self, other):
        if isinstance(other, GEntity):
            return self._data == other._data

        return self._data == other

    def __lt__(self, other):
        if isinstance(other, GEntity):
            return self._data < other._data

        return self._data < other

    def __bool__(self):
        return True

    def __getitem__(self, key):
        return self._setup.empty()

    def apply_(self, f: Union[str, meta.Function]) -> GABC:
        """See base class."""
        f = meta.func_deref(f)
        return self._setup.cook(f(self._data))

    @property
    def raw_(self) -> Any:
        """See base class."""
        return self._data


class GLeaf(GEntity):
    """Single non-composite object wrapper."""

    __slots__ = (meta.HASH_FIELD,)

    @meta.memoize(field=meta.HASH_FIELD)
    def __hash__(self):
        return hash(self._data)


class GInner(GEntity):
    """Wrapper for inner composite node."""

    __slots__ = ('_children',)

    def __init__(self, setup, data):
        """See base class."""

        super().__init__(setup, data)

        self._children = {}

    @abc.abstractmethod
    def _has_key(self, key):
        pass

    def __getitem__(self, key):
        if key in self._children:
            return self._children[key]

        if not self._has_key(key):
            if self._setup.strict:
                raise AttributeError(f"No such key: '{key}'.")

            value = GMissing(self._setup, self, key)
        else:
            value = self._setup.cook(self._data[key])

        self._children[key] = value

        return value


class GFrozenList(GInner, meta.SequenceMixin):
    """Immutable List."""

    __slots__ = (meta.HASH_FIELD,)

    def _has_key(self, key):
        return 0 <= key < len(self)

    @meta.memoize(field=meta.HASH_FIELD)
    def __hash__(self):
        return hash(tuple(self))


class GFrozenDict(GInner, meta.MappingMixin):
    """Immutable Dict."""

    __slots__ = (meta.HASH_FIELD,)

    def _has_key(self, key):
        return key in self

    @meta.memoize(field=meta.HASH_FIELD)
    def __hash__(self):
        return hash(tuple(self.items()))


class GList(
    GInner,
    meta.SequenceMixin,
    meta.FieldsSetDelMixin,
    collections_abc.MutableSequence,
):
    """Mutable List."""

    __slots__ = ()

    def _has_key(self, key):
        return 0 <= key < len(self)

    def __setitem__(self, key, value):
        self._data[key] = value

        if key in self._children:
            del self._children[key]

    def __delitem__(self, key):
        del self._data[key]

        self._children.clear()

    def insert(self, index, value) -> None:
        """Inserts new value at specified index.

        Args:
            index: Index to insert at.
            value: Object to insert.

        Returns:
            None

        """

        self._data.insert(index, value)
        self._children.clear()


class GDict(
    GInner,
    meta.MappingMixin,
    meta.FieldsSetDelMixin,
    collections_abc.MutableMapping,
):
    """Mutable Dict."""

    __slots__ = ()

    def _has_key(self, key):
        return key in self

    def __setitem__(self, key, value):
        self._data[key] = value

        if key in self._children:
            del self._children[key]

    def __delitem__(self, key):
        del self._data[key]

        if key in self._children:
            del self._children[key]
