import flask
import flask_restful
from routers import Comments

app = flask.Flask(__name__)
api = flask_restful.Api(app)
base_url = "/api/v1"

api.add_resource(
    Comments, f"{base_url.lower()}/comment"
)

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8989)

