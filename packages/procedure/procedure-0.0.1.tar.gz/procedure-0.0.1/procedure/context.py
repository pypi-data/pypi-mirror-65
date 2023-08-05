from .procedure_failure import ProcedureFailure

class Context(object):
    def __init__(self, **kwargs):
        self.verbose = False # default setting

        self._kwargs = kwargs
        self._parse_kwargs(**kwargs)
        self.success = None
        self.failure = None

    # Return formatted string, when Context is printed to console
    def __repr__(self):
        s =  " "
        for k, v in sorted(self.__dict__.items()):
            if k in ["_kwargs"]:
                continue
            if len(str(v)) > 25:
                continue

            if isinstance(v, str):
                v = "'" + v + "'"
            s += f"{k}={v} "

        s.strip()
        return f"{self.name()}({s})" # => PipelineContext(success=True, ...)

    def parent(self):
        return self._parent

    def name(self):
        return self.parent().__class__.__name__ + "Context"

    def fail(self, *, error=None, hard=False, **kwargs):
        self._parse_kwargs(**kwargs)
        if error is not None:
            self.error = error
        else:
            print(self)

        self.success = False
        self.failure = True
        if hard:
            self.fail_hard = True
        raise ProcedureFailure(str(error))

    def succeeded(self):
        self.success = True

    def _parse_kwargs(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def to_dict(self):
        return self._kwargs
