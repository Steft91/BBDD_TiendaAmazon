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

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/producto')
def producto():
    return render_template('producto.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/carrito')
def carrito():
    return render_template('carrito.html')


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

# Agregar un cliente
@app.route('/clientes', methods=['POST'])
def add_cliente():
    cliente = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Cliente (nombre, email, telefono) VALUES (%s, %s, %s)",
            (cliente['nombre'], cliente['email'], cliente['telefono'])
        )
        conn.commit()
        return jsonify({"message": "Cliente agregado"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Actualizar un cliente
@app.route('/clientes/<cliente_id>', methods=['PUT'])
def update_cliente(cliente_id):
    cliente = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Cliente SET nombre = %s, email = %s, telefono = %s WHERE cliente_id = %s",
            (cliente['nombre'], cliente['email'], cliente['telefono'], cliente_id)
        )
        conn.commit()
        if cursor.rowcount:
            return jsonify({"message": "Cliente actualizado"}), 200
        else:
            return jsonify({"message": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Eliminar un cliente
@app.route('/clientes/<cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Cliente WHERE cliente_id = %s", (cliente_id,))
        conn.commit()
        if cursor.rowcount:
            return jsonify({"message": "Cliente eliminado"}), 200
        else:
            return jsonify({"message": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
        


## Proveedores
@app.route('/proveedores', methods=['POST'])
def add_proveedor():
    """Registrar un nuevo proveedor."""
    proveedor = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Proveedor (nombre, email, telefono) VALUES (%s, %s, %s)",
            (proveedor['nombre'], proveedor['email'], proveedor['telefono'])
        )
        conn.commit()
        return jsonify({"message": "Proveedor registrado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/productos', methods=['POST'])
def add_producto():
    """Agregar un producto a la base de datos."""
    producto = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Producto (nombre, descripcion, precio, stock, proveedor_id, categoria_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (producto['nombre'], producto['descripcion'], producto['precio'], 
             producto['stock'], producto['proveedor_id'], producto['categoria_id'])
        )
        conn.commit()
        return jsonify({"message": "Producto agregado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/productos/<producto_id>', methods=['PUT'])
def update_producto(producto_id):
    """Actualizar información de un producto."""
    producto = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Producto SET nombre = %s, descripcion = %s, precio = %s, 
            stock = %s, proveedor_id = %s, categoria_id = %s
            WHERE producto_id = %s
            """,
            (producto['nombre'], producto['descripcion'], producto['precio'], 
             producto['stock'], producto['proveedor_id'], producto['categoria_id'], producto_id)
        )
        conn.commit()
        if cursor.rowcount:
            return jsonify({"message": "Producto actualizado exitosamente"}), 200
        else:
            return jsonify({"message": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/productos/<producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    """Eliminar un producto."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Producto WHERE producto_id = %s", (producto_id,))
        conn.commit()
        if cursor.rowcount:
            return jsonify({"message": "Producto eliminado exitosamente"}), 200
        else:
            return jsonify({"message": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



if __name__ == '__main__':
    app.run(debug=True)
