"""Pure job status summary.

Provides ``summarize(items)`` which counts job states in a plain list of
strings. Valid states are exactly ``"passed"``, ``"failed"`` and
``"pending"`` (case-sensitive). The function has no side effects, performs
no I/O, uses no external dependencies and never mutates its input.
"""

__all__ = ["summarize", "VALID_STATES"]

VALID_STATES = ("passed", "failed", "pending")


def _is_valid_state(item):
    """Return True only for exact built-in ``str`` values naming a valid state.

    The exact type check runs before any comparison, so unhashable objects
    (lists, dicts, sets), ``bool``, ``None``, numbers and ``str`` subclasses
    are rejected without hashing or invoking custom ``__eq__`` methods.
    """
    if type(item) is not str:
        return False
    for state in VALID_STATES:
        if item == state:
            return True
    return False


def summarize(items):
    """Summarize job statuses.

    Args:
        items: A plain ``list`` whose elements are each exactly one of
            ``"passed"``, ``"failed"`` or ``"pending"``.

    Returns:
        A new plain ``dict`` with exactly the integer keys ``total``,
        ``passed``, ``failed`` and ``pending``. An empty list yields all
        zeros.

    Raises:
        ValueError: If ``items`` is not a plain list, or if any element is
            not a valid state string (including unhashable objects, ``bool``
            and ``None``). Validation completes before any result is built,
            and the input is never modified.
    """
    if type(items) is not list:
        raise ValueError(
            "items must be a plain list, got %s" % type(items).__name__
        )

    # Work on a shallow snapshot so iteration is stable and the caller's
    # list is never touched.
    snapshot = list(items)

    passed = 0
    failed = 0
    pending = 0
    for index, item in enumerate(snapshot):
        if not _is_valid_state(item):
            raise ValueError(
                "invalid status at index %d: expected one of %s, got %s"
                % (index, ", ".join(VALID_STATES), type(item).__name__)
            )
        if item == "passed":
            passed += 1
        elif item == "failed":
            failed += 1
        else:
            pending += 1

    return {
        "total": len(snapshot),
        "passed": passed,
        "failed": failed,
        "pending": pending,
    }
