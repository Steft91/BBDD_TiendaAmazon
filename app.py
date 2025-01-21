from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Credenciales de la base de datos PostgreSQL
DB_HOST = "localhost"
DB_NAME = "PostAmazon"
DB_USER = "postgres"
DB_PASSWORD = ""

# Conexión a la base de datos
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, 
        database=DB_NAME, 
        user=DB_USER, 
        password=DB_PASSWORD,
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
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM Cliente")
        clientes = cursor.fetchall()
        return jsonify(clientes)
    except psycopg2.DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Obtener un cliente por ID
@app.route('/clientes/<int:id_cliente>', methods=['GET'])
def get_cliente_by_id(id_cliente):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM Cliente WHERE id_cliente = %s", (id_cliente,))
        cliente = cursor.fetchone()
        if cliente:
            return jsonify(cliente)
        else:
            return jsonify({"message": "Cliente no encontrado"}), 404
    except psycopg2.DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Agregar un cliente con id_cliente manual
@app.route('/clientes', methods=['POST'])
def add_cliente():
    cliente = request.json
    # Validar datos requeridos
    if not all(key in cliente for key in ['id_cliente', 'nombre', 'correo', 'telefono', 'contrasena']):
        return jsonify({"error": "Datos incompletos"}), 400
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Cliente (id_cliente, nombre, correo, telefono, contrasena) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (cliente['id_cliente'], cliente['nombre'], cliente['correo'], cliente['telefono'], cliente['contrasena'])
        )
        conn.commit()
        return jsonify({"message": "Cliente agregado correctamente"}), 201
    except psycopg2.DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Actualizar un cliente
@app.route('/clientes/<int:id_cliente>', methods=['PUT'])
def update_cliente(id_cliente):
    cliente = request.json

    # Validar que el cuerpo de la solicitud no esté vacío
    if not cliente:
        return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

    # Definir los campos válidos de la tabla y sus alias
    alias_campos = {
        "correo": "correo",  # Cambia 'correo' si el esquema tiene un nombre diferente
        "nombre": "nombre",
        "telefono": "telefono"
    }

    # Filtrar los campos válidos del JSON recibido
    campos = []
    valores = []
    for key, value in cliente.items():
        if key in alias_campos:  # Si la clave del JSON es válida
            campos.append(f"{alias_campos[key]} = %s")
            valores.append(value)

    # Si no hay campos válidos, devolver error
    if not campos:
        return jsonify({"error": "Ningún campo válido proporcionado para actualizar"}), 400

    # Agregar el ID del cliente al final de la lista de valores
    valores.append(id_cliente)

    # Construir la consulta SQL dinámica
    query = f"UPDATE Cliente SET {', '.join(campos)} WHERE id_cliente = %s"

    # Ejecutar la consulta
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, valores)
        conn.commit()

        # Verificar si se actualizó alguna fila
        if cursor.rowcount:
            return jsonify({"message": "Cliente actualizado"}), 200
        else:
            return jsonify({"message": "Cliente no encontrado"}), 404
    except psycopg2.DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Eliminar un cliente
@app.route('/clientes/<int:id_cliente>', methods=['DELETE'])
def delete_cliente(id_cliente):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Cliente WHERE id_cliente = %s", (id_cliente,))
        conn.commit()
        if cursor.rowcount:
            return jsonify({"message": "Cliente eliminado"}), 200
        else:
            return jsonify({"message": "Cliente no encontrado"}), 404
    except psycopg2.DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

## Proveedores
@app.route('/proveedores', methods=['GET'])
def get_proveedores():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM Proveedor")
        proveedor = cursor.fetchall()
        return jsonify(proveedor)
    except psycopg2.DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
            
@app.route('/proveedores', methods=['POST'])
def add_proveedor():
    """Registrar un nuevo proveedor."""
    proveedor = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO PROVEEDOR (ID_PROVEEDOR, NOMBRE, DESCRIPCION_PROVEEDOR, TELEFONO_PROVEEDOR, CORREO_PROVEEDOR) VALUES (%s, %s, %s, %s, %s)",
            (proveedor['id_proveedor'], proveedor['nombre'], proveedor['descripcion_proveedor'], proveedor['telefono_proveedor'], proveedor['correo_proveedor'])
        )
        conn.commit()
        return jsonify({"message": "Proveedor registrado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/proveedores/<int:id_proveedor>', methods=['PUT'])
def update_proveedor(id_proveedor):
    """Actualizar un proveedor existente (parcial o completo)."""
    datos = request.json
    if not datos:
        return jsonify({"error": "No se enviaron datos para actualizar"}), 400
    
    campos = []
    valores = []

    # Construir dinámicamente la consulta SQL a partir de los campos enviados
    for campo in ['nombre', 'descripcion_proveedor', 'telefono_proveedor', 'correo_proveedor']:
        if campo in datos:
            campos.append(f"{campo.upper()} = %s")
            valores.append(datos[campo])
    
    if not campos:
        return jsonify({"error": "No se enviaron campos válidos para actualizar"}), 400

    # Agregar el id_proveedor como último parámetro para el WHERE
    valores.append(id_proveedor)
    consulta_sql = f"UPDATE PROVEEDOR SET {', '.join(campos)} WHERE ID_PROVEEDOR = %s"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(consulta_sql, valores)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Proveedor no encontrado"}), 404
        return jsonify({"message": "Proveedor actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/proveedores/<int:id_proveedor>', methods=['DELETE'])
def delete_proveedor(id_proveedor):
    """Eliminar un proveedor existente."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM PROVEEDOR WHERE ID_PROVEEDOR = %s",
            (id_proveedor,)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Proveedor no encontrado"}), 404
        return jsonify({"message": "Proveedor eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


##CATEGORIAS
@app.route('/categorias', methods=['GET'])
def get_categorias():
    """Obtener todas las categorías."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CATEGORIA")
        categorias = cursor.fetchall()
        
        if not categorias:
            return jsonify({"message": "No hay categorías disponibles"}), 404
        
        # Convertir los resultados en una lista de diccionarios
        categorias_lista = [
            {
                "id_categoria": categoria[0],
                "nombre_categoria": categoria[1],
                "descripcion_categoria": categoria[2]
            }
            for categoria in categorias
        ]
        
        return jsonify(categorias_lista), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/categorias', methods=['POST'])
def add_categoria():
    """Registrar una nueva categoría."""
    categoria = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Modificar la consulta para retornar el ID generado automáticamente
        cursor.execute(
            "INSERT INTO CATEGORIA (ID_CATEGORIA, NOMBRE_CATEGORIA, DESCRIPCION_CATEGORIA) VALUES (%s, %s, %s)",
            (categoria['id_categoria'], categoria['nombre_categoria'], categoria['descripcion_categoria'])
        )
        
        conn.commit()
        return jsonify({"message": "Categoria registrada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/categorias/<int:id_categoria>', methods=['PUT'])
def update_categoria(id_categoria):
    """Actualizar una categoría existente (parcial o completa)."""
    datos = request.json
    if not datos:
        return jsonify({"error": "No se enviaron datos para actualizar"}), 400
    
    campos = []
    valores = []

    # Construir dinámicamente la consulta SQL a partir de los campos enviados
    for campo in ['nombre_categoria', 'descripcion_categoria']:
        if campo in datos:
            campos.append(f"{campo.upper()} = %s")
            valores.append(datos[campo])
    
    if not campos:
        return jsonify({"error": "No se enviaron campos válidos para actualizar"}), 400

    # Agregar el id_categoria como último parámetro para el WHERE
    valores.append(id_categoria)
    consulta_sql = f"UPDATE CATEGORIA SET {', '.join(campos)} WHERE ID_CATEGORIA = %s"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(consulta_sql, valores)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Categoría no encontrada"}), 404
        return jsonify({"message": "Categoría actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/categorias/<int:id_categoria>', methods=['DELETE'])
def delete_categoria(id_categoria):
    """Eliminar una categoría."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM CATEGORIA WHERE ID_CATEGORIA = %s", (id_categoria,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Categoría no encontrada"}), 404
        return jsonify({"message": "Categoría eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



if __name__ == '__main__':
    app.run(debug=True)
