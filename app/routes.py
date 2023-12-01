from flask import render_template, request, jsonify
from app import app
from BD import cuentas
from datetime import datetime




@app.route('/')
def index():
    return "este es el index"



@app.route('/cuentas', methods=['GET'])
def obtener_cuentas():
    return jsonify(cuentas)




@app.route('/billetera/contactos', methods=['GET'])
def obtener_contactos():
    num = request.args.get('minumero')
    cuenta = next((c for c in cuentas if c["id"] == num), None)
    if cuenta:
        contactos_info = []
        for contacto_id in cuenta["contactos"]:
            contacto = next((c for c in cuentas if c["id"] == contacto_id), None)
            if contacto:
                contactos_info.append(f"{contacto['id']}: {contacto['nombre']}")
        return jsonify({"contactos": contactos_info})
    else:
        return jsonify({"message": "Cuenta no encontrada"}), 404




@app.route('/billetera/pagar', methods=['GET'])
def realizar_pago():
    minumero = request.args.get('minumero')
    numerodestino = request.args.get('numerodestino')
    valor = float(request.args.get('valor'))

    cuenta_origen = next((c for c in cuentas if c["id"] == minumero), None)
    cuenta_destino = next((c for c in cuentas if c["id"] == numerodestino), None)

    if cuenta_origen and cuenta_destino:
        if cuenta_origen["saldo"] >= valor:
            cuenta_origen["saldo"] -= valor
            cuenta_destino["saldo"] += valor

            pago_realizado = {
                "origen": minumero,
                "destino": numerodestino,
                "valor": valor,
                "fecha": datetime.now().strftime("%d/%m/%Y")
            }

            
            cuenta_origen["historial"].append(pago_realizado)

            
            pago_recibido = {
                "origen": minumero,
                "destino": numerodestino,
                "valor": valor,
                "fecha": datetime.now().strftime("%d/%m/%Y")
            }
            cuenta_destino["historial"].append(pago_recibido)

            return jsonify({"message": "Pago realizado correctamente"})
        else:
            return jsonify({"message": "Saldo insuficiente"}), 400
    else:
        return jsonify({"message": "Cuenta no encontrada"}), 404
    
    
@app.route('/billetera/historial', methods=['GET'])
def obtener_historial():
    num = request.args.get('minumero')
    cuenta = next((c for c in cuentas if c["id"] == num), None)

    print(cuenta["historial"])

    if cuenta:
        saldo_actual = cuenta["saldo"]
        historial_operaciones = f"Saldo de {cuenta['nombre']}: {saldo_actual}\nOperaciones de {cuenta['nombre']}:\n"

        # Recorriendo el historial de la cuenta para mostrar las operaciones
        for operacion in cuenta["historial"]:
            if operacion["origen"] == num:
                historial_operaciones += f"Pago realizado de {operacion['valor']} a {next(c['nombre'] for c in cuentas if c['id'] == operacion['destino'])}\n"
            if operacion["destino"] == num:
                historial_operaciones += f"Pago recibido de {operacion['valor']} de {next(c['nombre'] for c in cuentas if c['id'] == operacion['origen'])}\n"

        return historial_operaciones
    else:
        return jsonify({"message": "Cuenta no encontrada"}), 404






