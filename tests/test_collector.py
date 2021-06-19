import pytest

import coollect


@pytest.mark.parametrize(
    'strategy', list(coollect.Strategy.__members__.values())
)
@pytest.mark.parametrize('validator', [None, lambda foo: foo])
def test_init(strategy, validator):
    collector = coollect.Collector(
        strategy=strategy,
        validator=validator,
    )
    assert collector.strategy == strategy
    assert collector.validator == validator
    assert collector.tags == []


@pytest.mark.parametrize(
    'strategy', list(coollect.Strategy.__members__.values())
)
def test_get_unknown_tag(strategy):
    collector = coollect.Collector(strategy=strategy)
    assert collector.get('foo') is None
    assert collector.get('foo', 'bar') == 'bar'


class TestSingleStrategy:
    def test_collect(self):
        collector = coollect.Collector(strategy=coollect.Strategy.SINGLE)

        @collector.collect
        def foo():
            pass

        assert collector.get('foo') == foo

    def test_multiple_collect_same_tag(self):
        collector = coollect.Collector(strategy=coollect.Strategy.SINGLE)

        @collector.collect(tag='same')
        def foo():
            pass

        exception = coollect.exceptions.TagAlreadyAssignedException
        with pytest.raises(exception) as exception_info:

            @collector.collect(tag='same')
            def bar():
                pass

        assert exception_info.value.tag == 'same'
        assert exception_info.value.func == foo

    def test_multiple_collect_different_tag(self):
        collector = coollect.Collector(strategy=coollect.Strategy.SINGLE)

        @collector.collect
        def foo():
            pass

        @collector.collect
        def bar():
            pass

        assert collector.get('foo') == foo
        assert collector.get('bar') == bar


class TestSingleOverrideStrategy:
    def test_collect(self):
        collector = coollect.Collector(
            strategy=coollect.Strategy.SINGLE_OVERRIDE
        )

        @collector.collect
        def foo():
            pass

        assert collector.get('foo') == foo

    def test_multiple_collect_same_tag(self):
        collector = coollect.Collector(
            strategy=coollect.Strategy.SINGLE_OVERRIDE
        )

        @collector.collect(tag='same')
        def foo():
            pass

        @collector.collect(tag='same')
        def bar():
            pass

        assert collector.get('same') == bar

    def test_multiple_collect_different_tag(self):
        collector = coollect.Collector(
            strategy=coollect.Strategy.SINGLE_OVERRIDE
        )

        @collector.collect
        def foo():
            pass

        @collector.collect
        def bar():
            pass

        assert collector.get('foo') == foo
        assert collector.get('bar') == bar


class TestMultipleStrategy:
    def test_collect(self):
        collector = coollect.Collector(strategy=coollect.Strategy.MULTIPLE)

        @collector.collect
        def foo():
            pass

        assert collector.get('foo') == {foo}

    def test_multiple_collect_same_tag(self):
        collector = coollect.Collector(strategy=coollect.Strategy.MULTIPLE)

        @collector.collect(tag='same')
        def foo():
            pass

        @collector.collect(tag='same')
        def bar():
            pass

        assert collector.get('same') == {foo, bar}

    def test_multiple_collect_different_tag(self):
        collector = coollect.Collector(strategy=coollect.Strategy.MULTIPLE)

        @collector.collect
        def foo():
            pass

        @collector.collect
        def bar():
            pass

        assert collector.get('foo') == {foo}
        assert collector.get('bar') == {bar}


class TestMultipleOrderedStrategy:
    def test_collect(self):
        collector = coollect.Collector(
            strategy=coollect.Strategy.MULTIPLE_ORDERED
        )

        @collector.collect
        def foo():
            pass

        assert collector.get('foo') == {foo}

    def test_multiple_collect_same_tag(self):
        collector = coollect.Collector(
            strategy=coollect.Strategy.MULTIPLE_ORDERED
        )

        funcs = []
        for _ in range(10):

            @collector.collect
            def foo():
                pass

            funcs.append(foo)

        assert list(collector.get('foo')) == funcs

    def test_multiple_collect_different_tag(self):
        collector = coollect.Collector(
            strategy=coollect.Strategy.MULTIPLE_ORDERED
        )

        @collector.collect
        def foo():
            pass

        @collector.collect
        def bar():
            pass

        assert collector.get('foo') == {foo}
        assert collector.get('bar') == {bar}


class TestValidator:
    def test_validator_match(self):
        collector = coollect.Collector(
            strategy=coollect.Strategy.SINGLE,
            validator=lambda func: func,
        )

        @collector.collect
        def foo():
            pass

        assert collector.get('foo') == foo

    def test_validator_unmatch(self):
        collector = coollect.Collector(
            strategy=coollect.Strategy.SINGLE,
            validator=lambda func: None,
        )

        def foo():
            pass

        exception = coollect.exceptions.InvalidateCallableException
        with pytest.raises(exception) as exception_info:
            # We don't use decorator here,
            # in order to use the function `foo` in the assert below.
            collector.collect(foo)

        assert collector.get('foo') is None
        assert exception_info.value.validator == collector.validator
        assert exception_info.value.callable == foo

    def test_validator_new_func(self):
        def other_foo():
            pass

        collector = coollect.Collector(
            strategy=coollect.Strategy.SINGLE,
            validator=lambda func: other_foo,
        )

        @collector.collect
        def foo():
            pass

        assert collector.get('foo') == other_foo

    def test_validator_not_callable(self):
        collector = coollect.Collector(
            strategy=coollect.Strategy.SINGLE,
            validator=lambda func: True,
        )

        exception = coollect.exceptions.ExpectedCallableException
        with pytest.raises(exception) as exception_info:

            @collector.collect
            def foo():
                pass

        assert collector.get('foo') is None
        assert exception_info.value.obj is True
