import pytest

from procedure import Procedure, ProcedureFailure

def test_it_exists():
    Procedure

def test_it_raises_an_error_if_initialized_with_arguments():
    with pytest.raises(ValueError) as excinfo:
        Procedure(foo="bar", baz="bang")
    assert str(excinfo.value) == "Do not call a class by initializing it. Use ClassName.call() instead."

    class Example(Procedure):
        def run(self):
            self.ctx.calc = 1 + 1

    with pytest.raises(ValueError) as excinfo:
        Example(foo="bar", baz="bang")
    assert str(excinfo.value) == "Do not call a class by initializing it. Use ClassName.call() instead."

def test_call_method_signature():
    Procedure.call(foo="bar", baz="bang")

def test_call_returns_a_data_structure_with_result():
    r = Procedure.call()
    assert r.success is not None

    r = Procedure.call(foo="bar", baz="bang")
    assert r.foo == "bar"
    assert r.baz == "bang"
    assert r.success == True


def test_inheritance_signature():
    class ExampleProcedure(Procedure):
        def run(self):
            print("context", self.ctx)

    r = ExampleProcedure.call(foo="bar", baz="bang")
    assert r.success == True
    assert r.foo == "bar"
    assert r.baz == "bang"



def test_procedure_with_before_run_method():
    class ExampleProcedure(Procedure):
        def before_run(self):
            self.ctx.foo = "bar"

    r = ExampleProcedure.call()
    assert r.foo == "bar"

    r = ExampleProcedure.call(foo="baz")
    assert r.foo == "bar"


def test_procedure_with_after_method():
    class ExampleProcedure(Procedure):
        def before_run(self):
            self.ctx.foo = "before"

        def after_run(self):
            self.ctx.foo = "after"

    r = ExampleProcedure.call()
    assert r.foo == "after"

def test_procedure_that_will_fail():
    class ExampleProcedure(Procedure):
        def run(self):
            self.ctx.before = True
            self.ctx.after = False
            self.ctx.fail(error="boom")
            self.ctx.after = True

    r = ExampleProcedure.call(foo="bar", baz="bang")
    assert r.success == False
    assert r.error == "boom"
    assert r.before
    assert not r.after

def test_procedure_that_fails_hard():
    class ExampleProcedure(Procedure):
        def run(self):
            self.ctx.before = "foo"
            self.ctx.after = None
            self.ctx.fail(error="BOOM!!", hard=True)
            self.ctx.after = "bar"

    with pytest.raises(ProcedureFailure):
        ExampleProcedure.call()
