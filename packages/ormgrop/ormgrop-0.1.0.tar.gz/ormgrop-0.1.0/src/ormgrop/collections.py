class NestedValueNotFoundError(Exception):
    pass


def get_in(collection, path, not_found=None):
    return _get_in(collection, path, lambda: not_found) if path else not_found


def require_in(collection, path):
    def raise_not_found_error():
        raise NestedValueNotFoundError(f"'{path}' not found in '{collection}'")
    return _get_in(collection, path, raise_not_found_error) if path else raise_not_found_error()


def _get_in(current, path, not_found):
    if not path:
        return current
    else:
        next_step, *rest = path
        try:
            return _get_in(current[next_step], rest, not_found)
        except (KeyError, IndexError, TypeError):
            return not_found()
