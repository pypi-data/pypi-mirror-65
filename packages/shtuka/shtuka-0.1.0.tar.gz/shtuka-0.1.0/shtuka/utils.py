"""General-purpose util functions."""

from typing import (  # isort:skip
    Any,
    List,
    Optional,
    Iterator,
    Tuple,
    Dict,
    Set,
)


def tree_copy(data: Any) -> Any:
    """Treats input data as tree and copies it.

    Args:
        data: Tree to copy.

    Returns:
        Copy of input data.

    """

    if isinstance(data, list):
        return [tree_copy(element) for element in data]
    elif isinstance(data, dict):
        return {key: tree_copy(element) for key, element in data.items()}
    else:
        return data


def gen_leafs(
    data: Any, stack: Optional[List[Any]] = None
) -> Iterator[Tuple[List[Any], Any]]:
    """Yields tree object leafs.

    Args:
        data: Data object to iterate.
        stack: List of parents stack nodes.

    Yields:
        Tuple of two: parents stack and leaf in in-order traversal.

    """

    if stack is None:
        stack = []

    if isinstance(data, list):
        for i, element in enumerate(data):
            stack.append(i)
            yield from gen_leafs(element, stack)
            stack.pop()
    elif isinstance(data, dict):
        for key, element in data.items():
            stack.append(key)
            yield from gen_leafs(element, stack)
            stack.pop()
    else:
        yield stack.copy(), data


def is_hashable(data: Any) -> bool:
    """Checks if data object is hashable.

    Args:
        data: Data object to check hashability.

    Returns:
        True if data object is hashable.

    """

    try:
        hash(data)
        return True
    except TypeError:
        return False


def find_forbidden_attributes(
    data: Any,
    forbidden_keys: Set[str],
    recursive: bool = False,
    prefix: Optional[str] = None,
) -> List[str]:
    """Finds list of invalid attribute names.

    Args:
        data: Data structure to find attributes.
        forbidden_keys: List of forbidden keys to detect invalid ones.
        recursive: True if check keys of substructures.
        prefix: Optional prefix str to prepend.

    Returns:
        List of invalid attributes.

    """

    if prefix is None:
        prefix = ""

    invalid_keys = []
    if isinstance(data, list) and recursive:
        for key, element in enumerate(data):
            invalid_keys.extend(
                find_forbidden_attributes(
                    data=element,
                    forbidden_keys=forbidden_keys,
                    recursive=recursive,
                    prefix=f'{prefix}[{key}]',
                )
            )

    if isinstance(data, dict):
        for key, element in data.items():
            if key in forbidden_keys:
                invalid_keys.append(f'{prefix}.{key}')
                continue

            if not recursive:
                continue

            if isinstance(key, str) and key.isidentifier():
                s_key = f'.{key}'
            else:
                s_key = f'[{key}]'

            invalid_keys.extend(
                find_forbidden_attributes(
                    data=element,
                    forbidden_keys=forbidden_keys,
                    recursive=recursive,
                    prefix=f"{prefix}{s_key}",
                )
            )

    return invalid_keys


def merge_dicts(base_dict: Dict, update_dict: Dict) -> Dict:
    """Performs two dicts merging.

    Args:
        base_dict: Base dict to merge.
        update_dict: Values update dict.

    Returns:
        New dict as merged output of two inputs.

    Examples:
        >>> left_dict = {'a': 1, 'b': {'c': 2}, 'f': 10}
        >>> right_dict = {'a': 3, 'd': 4, 'b': {'c': 5}}
        >>> sorted(merge_dicts(left_dict, right_dict).items())
        [('a', 3), ('b', {'c': 5}), ('d', 4), ('f', 10)]

    """

    ans = base_dict.copy()
    for k, v in update_dict.items():
        if k in base_dict:
            base_v = base_dict[k]
            if isinstance(base_v, dict) and isinstance(v, dict):
                ans[k] = merge_dicts(base_v, v)
            else:
                ans[k] = v
        else:
            ans[k] = v

    return ans
