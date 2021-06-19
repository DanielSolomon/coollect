import typing


class CoollectException(Exception):
    pass


class TagAlreadyAssignedException(CoollectException):
    def __init__(self, tag: str, func: typing.Callable) -> None:
        super().__init__(f'Function: {func} is assigned to this tag: {tag}')
        self._tag = tag
        self._func = func

    @property
    def tag(self) -> str:
        return self._tag

    @property
    def func(self) -> typing.Callable:
        return self._func


class ExpectedCallableException(CoollectException):
    def __init__(self, obj) -> None:
        super(
        ).__init__(f'Expected {obj} to be Callable, received: {type(obj)}')
        self._obj = obj

    @property
    def obj(self) -> str:
        return self._obj


class InvalidateCallableException(CoollectException):
    def __init__(self, callable, validator) -> None:
        super().__init__(f'Invalid {callable} according to {validator}')
        self._callable = callable
        self._validator = validator

    @property
    def callable(self) -> typing.Callable:
        return self._callable

    @property
    def validator(self) -> typing.Callable:
        return self._validator
