from flask_restplus import Namespace, Resource

ping_namespace = Namespace("Ping")


class Ping(Resource):
    def get(self):
        return {"status": "success", "message": "pong"}


ping_namespace.add_resource(Ping, "")
