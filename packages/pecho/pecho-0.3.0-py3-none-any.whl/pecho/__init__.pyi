from typing import Any, TextIO, Callable, List

__all__: List[str]
__version__: str

def echo(
    *objects: Any,
    newline: bool = False,
    end: str = '',
    pass_end: bool = False,
    str_convert_func: Callable = str,
    print_func: Callable = print,
    **print_kwargs: Any,
): ...
