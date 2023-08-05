from .context import Context, ProcedureFailure

class Procedure(object):
    @classmethod
    def call(cls, **kwargs):
        ctx = Context(**kwargs)
        return cls(ctx)._execute()

    def __init__(self, context=Context(), **kwargs):
        if len(kwargs) != 0:
            raise ValueError("Do not call a class by initializing it. Use ClassName.call() instead.")
        self.ctx = context

    def _execute(self):
        try:
            self.ctx._parent = self
            self.before_run()
            self.run()
            self.after_run()
            self.ctx.succeeded()
        except ProcedureFailure as err:
            if self.ctx.get("error") is None: # parent pipeline or workflow
                self.ctx.error = self.__class__.__name__ + "ProcedureFailure"
                self.ctx.failure = True
                self.ctx.success = False
                print(">>>", self.ctx)
            print("!!! error:", self.ctx.error)
            if hasattr(self.ctx, "fail_hard"):
                raise err
            else:
                print("+ not a hard failure. continuing...")
        finally:
            self.update_context_status()
        return self.ctx

    def before_run(self):
        pass

    def after_run(self):
        pass

    def run(self):
        return self.ctx

    def update_context_status(self):
        if self.ctx.success:
            self.ctx.status = "success"
        else:
            self.ctx.status = "failure"

