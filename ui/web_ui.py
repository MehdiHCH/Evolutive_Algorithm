from flask import Flask, render_template

app = Flask(__name__)

def launch_web_ui(route):
    @app.route("/")
    def index():
        route_data = {
            "distance": route.distance,
            "path": " -> ".join(str(city.ID) for city in route.cities)
        }
        return render_template("index.html", route=route_data)

    app.run(debug=True)
