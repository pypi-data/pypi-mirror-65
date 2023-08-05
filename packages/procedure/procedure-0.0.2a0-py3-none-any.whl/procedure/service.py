from flask import Flask, jsonify, request
import inspect

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(status="error", msg=str(e)), 404

from procedure import Procedure
class Service(Procedure):
    def before_run(self):
        self.validate_procedure()
        self.validate_self()

    def run(self):
        self.start_http_server()

    def parse_request_args(self, request):
        """
        This method can be overwritten by children to inject
        custom arguments to a procedure.

        Must return a dictionary type object.
        """
        return request.args

    def start_http_server(self):
        def handler():
            try:
                result = self.ctx.procedure.call(**self.parse_request_args(request))
                if result.success:
                    status_code = 200
                else:
                    status_code = 422 # unprocessable entity
            except Exception as err:
                status_code = 500
            finally:
                return jsonify(status=result.status), status_code

        app.route('/')(handler)
        app.run()


    def validate_procedure(self):
        assert self.ctx.procedure is not None

    def validate_self(self):
        pass
        #  source_code = inspect.getsource(self.__class__)
        #  print(source_code)
        #  assert "self.ctx.resp" in source_code, "Service does not add `resp` dict to ctx."


