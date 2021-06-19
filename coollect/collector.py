import collections
import orderedset
import enum
import typing

from . import exceptions


class Strategy(enum.Enum):
    SINGLE = enum.auto()
    SINGLE_OVERRIDE = enum.auto()
    MULTIPLE = enum.auto()
    MULTIPLE_ORDERED = enum.auto()


class Collector:
    def __init__(
        self,
        strategy: Strategy = Strategy.MULTIPLE,
        validator: typing.Optional[typing.Callable[
            [typing.Callable], typing.Optional[typing.Callable]]] = None,
    ):
        if strategy == Strategy.MULTIPLE_ORDERED:
            container_cls = orderedset.OrderedSet
        else:
            container_cls = set
        self._collection = collections.defaultdict(container_cls)
        self._strategy = strategy
        self._validator = validator

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @property
    def validator(
        self
    ) -> typing.Optional[typing.Callable[[typing.Callable],
                                         typing.Optional[typing.Callable]]]:
        return self._validator

    @property
    def tags(self) -> typing.List[str]:
        return list(self._collection.keys())

    def collect(
        self,
        func: typing.Optional[typing.Callable] = None,
        *,
        tag: typing.Optional[str] = None
    ):
        def _collect(func: typing.Callable):
            nonlocal tag
            tag = tag if tag is not None else func.__name__

            if self.validator is not None:
                validated_func = self.validator(func)
                if validated_func is not None:
                    if not hasattr(validated_func, '__call__'):
                        raise exceptions.ExpectedCallableException(
                            obj=validated_func
                        )
                    func = validated_func
                else:
                    raise exceptions.InvalidateCallableException(
                        callable=func, validator=self.validator
                    )

            already_exists = tag in self._collection
            if already_exists and self._strategy == Strategy.SINGLE:
                raise exceptions.TagAlreadyAssignedException(
                    tag=tag,
                    func=self.get(tag),
                )
            elif already_exists and self._strategy == Strategy.SINGLE_OVERRIDE:
                self._collection[tag].clear()
            self._collection[tag].add(func)
            return func

        if func is None:
            return _collect
        return _collect(func)

    def get(self, tag: str, default: typing.Any = None) -> typing.Any:
        collection = self._collection.get(tag)
        if collection is None:
            return default

        if self.strategy in (
                Strategy.SINGLE,
                Strategy.SINGLE_OVERRIDE,
        ):
            # In case strategy is SINGLE*,
            # it means there is only one registered function.
            return list(collection)[0]

        return collection
