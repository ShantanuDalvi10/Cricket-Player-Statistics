from flask import Flask,redirect,url_for
from config import Config
from routes.player_routes import stats_bp

app = Flask(__name__)

app.config.from_object(Config)
Config.validate()

app.register_blueprint(stats_bp)

@app.route("/")
def home():
    return redirect(url_for("stats.home"))

if __name__=="__main__":
    app.run(debug=Config.DEBUG)