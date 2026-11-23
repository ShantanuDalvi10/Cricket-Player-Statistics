from flask import Blueprint,render_template,request,flash,current_app,redirect,url_for,session
from services.player_service import get_player_data
from services.api import PlayerNotFoundError,APIRequestError

stats_bp  = Blueprint("stats", __name__)

@stats_bp.route("/player-statistics")
def home():
    player_data = session.pop("player_data", None)
    return render_template("player_stats.html",player_data=player_data)



@stats_bp.route("/search", methods=['POST'])
def search_player():
    """This route is used search the player using player name through the form"""

    player_name = request.form.get("player_name","")
    try:
        player_data = get_player_data(player_name=player_name)
        session["player_data"] = player_data
        flash("Player Found Successfully.","success")
        return render_template("player_stats.html", player_data=player_data)
    except PlayerNotFoundError:
        flash("Player not found.", "error")
        return redirect(url_for("stats.home"))
    except APIRequestError:
        flash("Unable to retrieve player information. Please try again.", "error")
        return redirect(url_for("stats.home"))
    except ValueError as error:
        flash(str(error),"error")
        return redirect(url_for("stats.home"))
    except Exception:
        current_app.logger.exception("There is problem in searching player")
        flash("Player couldn't found.","error")
        return redirect(url_for("stats.home"))


