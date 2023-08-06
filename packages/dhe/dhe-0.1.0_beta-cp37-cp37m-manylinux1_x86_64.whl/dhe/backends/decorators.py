import inspect


def swallow_unneeded_arguments(f):
    sig = inspect.signature(f)
    arg_keys = frozenset(p.name for p in sig.parameters.values() if p.kind in {
        inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY})

    def _f(*args, **kwargs):
        return f(*args, **{k: v for k, v in kwargs.items() if k in arg_keys})
    return _f
