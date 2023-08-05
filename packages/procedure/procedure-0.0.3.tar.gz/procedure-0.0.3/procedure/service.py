from flask import Flask, jsonify, request
import inspect
import datetime

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(status="error", msg=str(e)), 404

from procedure import Procedure
class Service(Procedure):
    def before_run(self):
        self.validate_procedure()
        self.validate_self()

        self.ctx.host = self.ctx.get("host", "127.0.0.1")
        self.ctx.port = self.ctx.get("port", 8675)
        self.ctx.debug = self.ctx.get("debug", False)

        self.last_state = None
        self.last_ran = None

    def run(self):
        self.start_http_server()

    def parse_request_args(self, request):
        """
        This method can be overwritten by children to inject
        custom arguments to a procedure.

        Must return a dictionary type object.
        """
        return {} # empty to avoid dangerous injections

    def start_http_server(self):
        def post_handler():
            try:
                result = self.ctx.procedure.call(**self.parse_request_args(request))
                self.last_state = result.status
                self.last_ran = datetime.datetime.now().isoformat(timespec="seconds")

                if result.success:
                    status_code = 200
                else:
                    status_code = 422 # unprocessable entity
            except Exception as err:
                status_code = 500
            finally:
                return jsonify(status=result.status), status_code

        def get_handler():
            return jsonify(service=self.name,
                    procedure=self.ctx.procedure.__name__,
                    last_state=self.last_state,
                    last_ran=self.last_ran,
                    )

        app.route('/', methods=["POST"])(post_handler)
        app.route('/', methods=["GET"])(get_handler)
        app.run(host=self.ctx.host, port=self.ctx.port, debug=self.ctx.debug)


    def validate_procedure(self):
        assert self.ctx.procedure is not None

    def validate_self(self):
        pass
        #  source_code = inspect.getsource(self.__class__)
        #  print(source_code)
        #  assert "self.ctx.resp" in source_code, "Service does not add `resp` dict to ctx."


