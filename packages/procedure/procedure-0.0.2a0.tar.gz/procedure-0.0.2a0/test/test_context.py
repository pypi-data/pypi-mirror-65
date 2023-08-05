import pytest

from procedure import Context, ProcedureFailure

def test_it_is_created_with_unlimited_kwargs():
    ctx = Context(foo="bar", baz="bang")
    assert ctx.foo == "bar"
    assert ctx.baz == "bang"

    ctx = Context(a="b", c="d", e="f")
    assert ctx.a == "b"
    assert ctx.c == "d"
    assert ctx.e == "f"

def test_default_success_value():
    ctx = Context()
    assert ctx.success

def test_failing_hard():
    ctx = Context()
    error_msg = "this was the error"
    with pytest.raises(ProcedureFailure, match=error_msg):
        ctx.fail(error=error_msg, hard=True, bar="baz")

    assert not ctx.success
    assert ctx.error == error_msg
    assert hasattr(ctx, "fail_hard")
    assert not hasattr(ctx, "hard")
    assert ctx.bar == "baz"


def test_failing():
    ctx = Context()
    error_msg = "this was the error"
    with pytest.raises(ProcedureFailure, match=error_msg):
        ctx.fail(error=error_msg, bar="baz")

    assert not ctx.success
    assert ctx.error == error_msg
    assert ctx.bar == "baz"
    assert not hasattr(ctx, "fail_hard")
