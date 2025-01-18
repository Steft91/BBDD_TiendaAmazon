from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Credenciales de la base de datos PostgreSQL
DB_HOST = "localhost"
DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""

# Conexión a la base de datos
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, 
        database=DB_NAME, 
        user=DB_USER, 
        password=DB_PASSWORD
    )

@app.route('/')
def home():
    return render_template('index.html')

# Definición de rutas

## CLIENTES
# Obtener todos los clientes
@app.route('/clientes', methods=['GET'])
def get_clientes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM Cliente")
        clientes = cursor.fetchall()
        return jsonify(clientes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Obtener un cliente por ID
@app.route('/clientes/<Id_cliente>', methods=['GET'])
def get_cliente_by_id(Id_cliente):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM Cliente WHERE Id_cliente = %s", (Id_cliente,))
        cliente = cursor.fetchone()
        if cliente:
            return jsonify(cliente)
        else:
            return jsonify({"message": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


## Proveedores


## Productos



if __name__ == '__main__':
    app.run(debug=True)
