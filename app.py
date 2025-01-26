from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal

app = Flask(__name__)
app.secret_key = 'amazon'


# Credenciales de la base de datos PostgreSQL
DB_HOST = "localhost"
DB_NAME = ""
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
    conn.set_client_encoding('UTF8')  # Esto asegura que se use UTF-8
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/producto')
def producto():
    return render_template('producto.html')

@app.route('/carrito')
def carrito():
    return render_template('carrito.html')

@app.route('/libreria')
def libreria():
    return render_template('libreria.html')

@app.route('/libros')
def libros():
    return render_template('libros.html')


# Ruta para el login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Verificación de credenciales en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cliente WHERE correo = %s AND contrasena = %s', (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            # Redirige a index.html si las credenciales son correctas
            return redirect(url_for('index'))
        else:
            # Muestra un mensaje de error si las credenciales no son correctas
            return 'Credenciales incorrectas'

    return render_template('login.html')

# Ruta para la página principal (index.html)
@app.route('/index')
def index():
    return render_template('index.html')


# Ruta para el registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        
        try:
            # Conectar a la base de datos
            conn = get_db_connection()
            cursor = conn.cursor()

            # Verificar si el correo ya existe en la base de datos
            cursor.execute('SELECT * FROM cliente WHERE correo = %s', (email,))
            existing_user = cursor.fetchone()  # Devuelve None si no encuentra registros

            if existing_user:
                flash('El correo ya está registrado, por favor ingresa otro.', 'error')
                cursor.close()
                conn.close()
                # Volver a renderizar el formulario de registro con el mensaje de error
                return render_template('login.html', show_register=True)

            cursor.execute('INSERT INTO cliente (nombre, telefono, correo, contrasena) VALUES (%s, %s, %s, %s)',
                           (name, phone, email, password))
            conn.commit()  # Asegúrate de hacer commit
            cursor.close()
            conn.close()

            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')

            return redirect(url_for('login'))

        except Exception as e:
            print(f"Error al registrar el cliente: {e}")
            flash('Hubo un problema al registrar al cliente, por favor intenta de nuevo.', 'error')
            return render_template('login.html', show_register=True)

    return render_template('login.html', show_register=False)

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
    if not all(key in cliente for key in ['nombre', 'correo', 'telefono', 'contrasena']):
        return jsonify({"error": "Datos incompletos"}), 400
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Cliente (nombre, correo, telefono, contrasena) 
            VALUES (%s, %s, %s, %s)
            """,
            (cliente['nombre'], cliente['correo'], cliente['telefono'], cliente['contrasena'])
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
@app.route('/cliente/<int:id_cliente>', methods=['PUT'])
def update_cliente(id_cliente):
    # Verificar si el cliente está autenticado
    if not session.get('cliente_id') or session['cliente_id'] != id_cliente:
        return jsonify({"error": "No estás autorizado para actualizar estos datos"}), 403

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
    query = f"UPDATE cliente SET {', '.join(campos)} WHERE id_cliente = %s"

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
            "INSERT INTO PROVEEDOR (NOMBRE, DESCRIPCION_PROVEEDOR, TELEFONO_PROVEEDOR, CORREO_PROVEEDOR) VALUES (%s, %s, %s, %s)",
            (proveedor['nombre'], proveedor['descripcion_proveedor'], proveedor['telefono_proveedor'], proveedor['correo_proveedor'])
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
            "INSERT INTO CATEGORIA (NOMBRE_CATEGORIA, DESCRIPCION_CATEGORIA) VALUES (%s, %s)",
            (categoria['nombre_categoria'], categoria['descripcion_categoria'])
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


##PRODUCTOS
def validate_producto_data(producto):
    """Valida los campos requeridos para un producto."""
    required_fields = ['nombre', 'descripcion', 'precio', 'stock', 'id_proveedor', 'id_categoria']
    for field in required_fields:
        if field not in producto or producto[field] is None:
            raise ValueError(f"El campo '{field}' es obligatorio.")

@app.route('/productos', methods=['POST'])
def add_producto():
    """Agrega un producto a la base de datos."""
    producto = request.json
    try:
        validate_producto_data(producto)  # Validar datos de entrada
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO producto (nombre, descripcion, precio, stock, id_proveedor, id_categoria)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (producto['nombre'], producto['descripcion'], producto['precio'],
             producto['stock'], producto['id_proveedor'], producto['id_categoria'])
        )
        conn.commit()
        return jsonify({"message": "Producto agregado exitosamente"}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/productos/<int:id_producto>', methods=['PUT'])
def update_producto(id_producto):
    """Actualiza un producto existente (parcial o completo)."""
    datos = request.json
    if not datos:
        return jsonify({"error": "No se enviaron datos para actualizar"}), 400

    campos = []
    valores = []

    # Construir dinámicamente la consulta SQL a partir de los campos enviados
    for campo in ['nombre', 'descripcion', 'precio', 'stock', 'id_proveedor', 'id_categoria']:
        if campo in datos:
            campos.append(f"{campo} = %s")
            valores.append(datos[campo])
    
    if not campos:
        return jsonify({"error": "No se enviaron campos válidos para actualizar"}), 400

    # Agregar el id_producto como último parámetro para el WHERE
    valores.append(id_producto)
    consulta_sql = f"UPDATE producto SET {', '.join(campos)} WHERE id_producto = %s"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(consulta_sql, valores)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Producto no encontrado"}), 404
        return jsonify({"message": "Producto actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/productos/<int:id_producto>', methods=['DELETE'])
def delete_producto(id_producto):
    """Eliminar un producto."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PRODUCTO WHERE ID_PRODUCTO = %s", (id_producto,))
        conn.commit()
        if cursor.rowcount:
            return jsonify({"message": "Producto eliminado exitosamente"}), 200
        else:
            return jsonify({"message": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/productos', methods=['GET'])
def get_productos():
    """Listar todos los productos."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM PRODUCTO")
        productos = cursor.fetchall()

        if not productos:
            return jsonify({"message": "No se encontraron productos"}), 404
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": f"Error al consultar productos: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

# Obtener los productos segun su categoria
@app.route('/productos/categoria/<int:id_categoria>', methods=['GET'])
def get_productos_por_categoria(id_categoria):
    """Listar productos por categoría."""
    if id_categoria <= 0:
        return jsonify({"error": "ID de categoría inválido"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM PRODUCTO WHERE ID_CATEGORIA = %s", (id_categoria,))
        productos = cursor.fetchall()

        if not productos:
            return jsonify({"message": "No se encontraron productos para esta categoría"}), 404
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": f"Error al consultar productos: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/compras', methods=['POST'])
def registrar_compra():
    data = request.json

    try:
        # Extraer datos principales
        id_cliente = data['id_cliente']
        id_direccion = data['id_direccion']
        productos = data['productos']  # Lista de productos con id y cantidad

        total_importe = 0
        detalles = []

        # Conexión a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Validar productos y calcular totales
        for prod in productos:
            cursor.execute("SELECT id_producto, precio, stock FROM producto WHERE id_producto = %s", (prod['id_producto'],))
            producto = cursor.fetchone()

            if not producto:
                return jsonify({'error': f"Producto con ID {prod['id_producto']} no encontrado"}), 404

            if producto['stock'] < prod['cantidad']:
                return jsonify({'error': f"Stock insuficiente para el producto {producto['id_producto']}"}), 400

            subtotal = Decimal(producto['precio']) * Decimal(prod['cantidad'])
            total_importe += subtotal

            detalles.append({
                'id_producto': producto['id_producto'],
                'cantidad': prod['cantidad'],
                'precio_unitario': producto['precio'],
                'subtotal': subtotal
            })

        # Calcular impuestos (10%) y precio total
        impuestos = total_importe * Decimal('0.10')
        precio_total = total_importe + impuestos

        # Insertar la compra en la tabla COMPRA
        cursor.execute(
            """
            INSERT INTO compra (id_cliente, id_direccion, impuestos, importe, precio_total)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_compra
            """,
            (id_cliente, id_direccion, impuestos, total_importe, precio_total)
        )
        id_compra = cursor.fetchone()['id_compra']

        # Insertar los detalles de la compra en la tabla DETALLE_COMPRA
        for detalle in detalles:
            cursor.execute(
                """
                INSERT INTO detalle_compra (id_producto, id_compra, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (detalle['id_producto'], id_compra, detalle['cantidad'], detalle['precio_unitario'], detalle['subtotal'])
            )

            # Reducir stock del producto
            cursor.execute(
                "UPDATE producto SET stock = stock - %s WHERE id_producto = %s",
                (detalle['cantidad'], detalle['id_producto'])
            )

        # Confirmar transacción
        conn.commit()
        return jsonify({'message': 'Compra registrada exitosamente', 'id_compra': id_compra}), 201

    except Exception as e:
        # Revertir cambios en caso de error
        if conn:
            conn.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        # Cerrar la conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()

      
        
@app.route('/compras/<int:cliente_id>', methods=['GET'])
def historial_compras(cliente_id):
    """
    Consultar el historial de compras de un cliente.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Verificar que el cliente exista
        cursor.execute("SELECT * FROM cliente WHERE id_cliente = %s", (cliente_id,))
        if not cursor.fetchone():
            return jsonify({"message": "Cliente no encontrado"}), 404

        cursor.execute(
            """
            SELECT c.id_compra, c.precio_total, dc.id_producto, dc.cantidad, 
                   p.nombre AS producto, p.precio, p.descuento
            FROM compra c
            JOIN detalle_compra dc ON c.id_compra = dc.id_compra
            JOIN producto p ON dc.id_producto = p.id_producto
            WHERE c.id_cliente = %s
            ORDER BY c.id_compra DESC
            """,
            (cliente_id,)
        )
        compras = cursor.fetchall()

        if not compras:
            return jsonify({"message": "No se encontraron compras para este cliente"}), 404

        return jsonify(compras), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Cerrar cursor y conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/compra/<int:compra_id>', methods=['GET'])
def detalle_compra(compra_id):
    """
    Obtener detalles de una compra específica.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Verificar que la compra exista
        cursor.execute("SELECT * FROM compra WHERE id_compra = %s", (compra_id,))
        if not cursor.fetchone():
            return jsonify({"message": "Compra no encontrada"}), 404

        cursor.execute(
            """
            SELECT c.id_compra, c.precio_total, dc.id_producto, dc.cantidad, 
                   p.nombre AS producto, p.precio
            FROM compra c
            JOIN detalle_compra dc ON c.id_compra = dc.id_compra
            JOIN producto p ON dc.id_producto = p.id_producto
            WHERE c.id_compra = %s
            """,
            (compra_id,)
        )
        compra = cursor.fetchall()

        if not compra:
            return jsonify({"message": "Detalles de la compra no encontrados"}), 404

        return jsonify(compra), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Cerrar cursor y conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()



@app.route('/compra/<compra_id>', methods=['DELETE'])
def eliminar_compra(compra_id):
    """
    Eliminar una compra específica.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si la compra existe
        cursor.execute("SELECT * FROM Compra WHERE Id_Compra = %s", (compra_id,))
        if not cursor.fetchone():
            return jsonify({"message": "Compra no encontrada"}), 404

        # Eliminar productos asociados a la compra
        cursor.execute("DELETE FROM Compra_Producto WHERE Id_Compra = %s", (compra_id,))

        # Eliminar la compra
        cursor.execute("DELETE FROM Compra WHERE Id_Compra = %s", (compra_id,))

        conn.commit()
        return jsonify({"message": "Compra eliminada exitosamente"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
  
@app.route('/rastreo/<int:compra_id>', methods=['GET'])
def rastrear_compra(compra_id):
    """
    Consultar el estado de rastreo de una compra.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Ajuste en nombres de columnas según la tabla proporcionada
        cursor.execute(
            """
            SELECT r.id_rastreo, r.estado_rastreo AS estado, r.fecha_envio, r.fecha_entrega
            FROM rastreo r
            JOIN compra c ON r.id_compra = c.id_compra
            WHERE c.id_compra = %s
            """,
            (compra_id,)
        )
        rastreo = cursor.fetchone()

        if not rastreo:
            return jsonify({"message": "No se encontró rastreo para esta compra"}), 404

        return jsonify(rastreo), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/metodo_pago', methods=['GET'])
def obtener_metodos_pago():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM metodo_de_pago"
        cursor.execute(query)
        metodos_pago = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(metodos_pago), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/metodo_pago', methods=['POST'])
def registrar_metodo_pago():
    data = request.json
    id_compra = data.get("id_compra")
    metodo_pago = data.get("metodo_pago")  # "tarjeta", "giftcard" o "ambos"
    tarjeta = data.get("tarjeta", {})  # Diccionario con info de la tarjeta
    giftcard = data.get("giftcard", {})  # Diccionario con info de la gift card

    try:
        # Conexión a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar que la compra exista
        cursor.execute("SELECT precio_total FROM COMPRA WHERE id_compra = %s", (id_compra,))
        compra = cursor.fetchone()
        if not compra:
            return jsonify({"error": "La compra no existe"}), 404

        precio_total = Decimal(compra[0])  # Total de la compra
        restante = precio_total  # Para manejar el saldo restante

        # Registrar método de pago
        if metodo_pago == "tarjeta":
            # Validar datos de la tarjeta
            if not tarjeta.get("num_tarjeta") or not tarjeta.get("fecha_vencimiento") or not tarjeta.get("cvv"):
                return jsonify({"error": "Datos incompletos de la tarjeta"}), 400

            # Insertar en METODO_DE_PAGO
            cursor.execute(
                """
                INSERT INTO METODO_DE_PAGO (id_compra, tipo_pago)
                VALUES (%s, %s) RETURNING id_metodopago
                """,
                (id_compra, "tarjeta")
            )
            id_metodopago = cursor.fetchone()[0]

            # Insertar en TARJETA
            cursor.execute(
                """
                INSERT INTO TARJETA (num_tarjeta, id_metodopago, nombre, fecha_vencimiento, cvv)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (tarjeta["num_tarjeta"], id_metodopago, tarjeta.get("nombre"), tarjeta["fecha_vencimiento"], tarjeta["cvv"])
            )
            restante = Decimal(0)  # Se cubrió todo con la tarjeta

        elif metodo_pago == "giftcard":
            # Validar datos de la gift card
            if not giftcard.get("id_gift") or not giftcard.get("saldo") or not giftcard.get("fecha_emision") or not giftcard.get("fecha_expedicion"):
                return jsonify({"error": "Datos incompletos de la gift card"}), 400

            # Insertar en METODO_DE_PAGO
            cursor.execute(
                """
                INSERT INTO METODO_DE_PAGO (id_compra, tipo_pago)
                VALUES (%s, %s) RETURNING id_metodopago
                """,
                (id_compra, "giftcard")
            )
            id_metodopago = cursor.fetchone()[0]

            # Validar existencia y saldo de la gift card
            cursor.execute("SELECT saldo FROM GIFT_CARD WHERE id_gift = %s", (giftcard["id_gift"],))
            giftcard_data = cursor.fetchone()

            if not giftcard_data:
                # Si la gift card no existe, insertar una nueva asociada al método de pago
                cursor.execute(
                    """
                    INSERT INTO GIFT_CARD (id_gift, id_metodopago, saldo, fecha_emision, fecha_expedicion)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (giftcard["id_gift"], id_metodopago, giftcard["saldo"], giftcard["fecha_emision"], giftcard["fecha_expedicion"])
                )
            else:
                # Si la gift card existe, validar su saldo y actualizar
                saldo_giftcard = Decimal(giftcard_data[0])
                if saldo_giftcard < precio_total:
                    return jsonify({"error": "Saldo insuficiente en la gift card"}), 400

                nuevo_saldo = saldo_giftcard - precio_total
                cursor.execute(
                    "UPDATE GIFT_CARD SET saldo = %s WHERE id_gift = %s",
                    (nuevo_saldo, giftcard["id_gift"])
                )

            restante = Decimal(0) # Se cubrió todo con la gift card

        elif metodo_pago == "ambos":
            # Validar datos de la tarjeta y gift card
            if not tarjeta.get("num_tarjeta") or not tarjeta.get("fecha_vencimiento") or not tarjeta.get("cvv"):
                return jsonify({"error": "Datos incompletos de la tarjeta"}), 400

            if not giftcard.get("id_gift"):
                return jsonify({"error": "Datos incompletos de la gift card"}), 400

            # Validar existencia y saldo de la gift card
            cursor.execute("SELECT saldo FROM GIFT_CARD WHERE id_gift = %s", (giftcard["id_gift"],))
            giftcard_data = cursor.fetchone()
            if not giftcard_data:
                return jsonify({"error": "La gift card no existe"}), 404

            saldo_giftcard = Decimal(giftcard_data[0])
            pago_giftcard = min(saldo_giftcard, precio_total)
            restante -= pago_giftcard

            # Actualizar saldo de la gift card
            cursor.execute(
                "UPDATE GIFT_CARD SET saldo = %s WHERE id_gift = %s",
                (saldo_giftcard - pago_giftcard, giftcard["id_gift"])
            )

            # Insertar en METODO_DE_PAGO para la gift card
            cursor.execute(
                """
                INSERT INTO METODO_DE_PAGO (id_compra, tipo_pago)
                VALUES (%s, %s)
                """,
                (id_compra, "giftcard")
            )

            # Si todavía queda un monto restante, se cubre con la tarjeta
            if restante > 0:
                # Insertar en METODO_DE_PAGO para la tarjeta
                cursor.execute(
                    """
                    INSERT INTO METODO_DE_PAGO (id_compra, tipo_pago)
                    VALUES (%s, %s) RETURNING id_metodopago
                    """,
                    (id_compra, "tarjeta")
                )
                id_metodopago = cursor.fetchone()[0]

                # Insertar en TARJETA
                cursor.execute(
                    """
                    INSERT INTO TARJETA (num_tarjeta, id_metodopago, nombre, fecha_vencimiento, cvv)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (tarjeta["num_tarjeta"], id_metodopago, tarjeta.get("nombre"), tarjeta["fecha_vencimiento"], tarjeta["cvv"])
                )
                restante = Decimal(0)  # Todo el saldo restante se cubrió con la tarjeta

            # Si el monto restante es mayor que 0, hay un error en la lógica
            if restante > 0:
                return jsonify({"error": "El monto restante no pudo ser cubierto"}), 400

        # Confirmar cambios
        conn.commit()
        return jsonify({"message": "Método de pago registrado exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/tarjeta', methods=['GET'])
def obtener_tarjetas():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM tarjeta"
        cursor.execute(query)
        tarjetas = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(tarjetas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para agregar una nueva tarjeta
@app.route('/tarjeta', methods=['POST'])
def agregar_tarjeta():
    try:
        datos = request.json

        num_tarjeta = datos.get('num_tarjeta')
        id_metodopago = datos.get('id_metodopago')
        nombre = datos.get('nombre')
        fecha_vencimiento = datos.get('fecha_vencimiento')
        cvv = datos.get('cvv')

        if not all([num_tarjeta, id_metodopago, nombre, fecha_vencimiento, cvv]):
            return jsonify({'error': 'Faltan datos requeridos: num_tarjeta, id_metodopago, nombre, fecha_vencimiento, cvv'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO tarjeta (num_tarjeta, id_metodopago, nombre, fecha_vencimiento, cvv)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (num_tarjeta, id_metodopago, nombre, fecha_vencimiento, cvv))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'mensaje': 'Tarjeta agregada exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para obtener gift cards
@app.route('/gift_card', methods=['GET'])
def obtener_gift_cards():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM gift_card"
        cursor.execute(query)
        gift_cards = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(gift_cards), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para agregar una nueva gift card
@app.route('/gift_card', methods=['POST'])
def registrar_giftcard():
    data = request.json

    id_gift = data.get("id_gift")
    id_metodopago = data.get("id_metodopago")
    saldo = data.get("saldo")
    fecha_emision = data.get("fecha_emision")
    fecha_expedicion = data.get("fecha_expedicion")

    # Validar datos obligatorios
    if not id_gift or not id_metodopago or saldo is None or not fecha_emision or not fecha_expedicion:
        return jsonify({"error": "Datos incompletos para la gift card"}), 400

    try:
        # Conexión a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar que el método de pago exista
        cursor.execute("SELECT id_metodopago FROM METODO_DE_PAGO WHERE id_metodopago = %s", (id_metodopago,))
        if cursor.fetchone() is None:
            return jsonify({"error": "El método de pago asociado no existe"}), 404

        # Insertar en la tabla GIFT_CARD
        cursor.execute(
            """
            INSERT INTO GIFT_CARD (id_gift, id_metodopago, saldo, fecha_emision, fecha_expedicion)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (id_gift, id_metodopago, saldo, fecha_emision, fecha_expedicion)
        )

        # Confirmar cambios
        conn.commit()
        return jsonify({"message": "Gift card registrada exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/direcciones', methods=['POST'])
def agregar_direccion():
    """
    Agregar una nueva dirección.
    """
    datos = request.json
    id_ciudad = datos.get('id_ciudad')
    direccion_principal = datos.get('direccion_principal')
    direccion_secundaria = datos.get('direccion_secundaria')
    codigo_postal = datos.get('codigo_postal')

    if not id_ciudad or not direccion_principal or not direccion_secundaria or not codigo_postal:
        return jsonify({"error": "Los campos id_ciudad, direccion_principal, direccion_secundaria y codigo_postal son obligatorios"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si la ciudad existe
        cursor.execute("SELECT * FROM Ciudad WHERE id_ciudad = %s", (id_ciudad,))
        if not cursor.fetchone():
            return jsonify({"error": "Ciudad no encontrada"}), 404

        # Insertar nueva dirección
        cursor.execute(
            """
            INSERT INTO Direccion (id_ciudad, direccion_principal, direccion_secundaria, codigo_postal) 
            VALUES (%s, %s, %s, %s) RETURNING id_direccion
            """,
            (id_ciudad, direccion_principal, direccion_secundaria, codigo_postal)
        )
        id_direccion = cursor.fetchone()[0]
        conn.commit()

        return jsonify({"message": "Dirección registrada exitosamente", "id_direccion": id_direccion}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
        

@app.route('/direcciones', methods=['GET'])
def listar_direcciones():
    """
    Listar todas las direcciones.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            """
            SELECT d.id_direccion, d.direccion_principal, d.direccion_secundaria, d.codigo_postal,
                   c.nombre_ciudad AS ciudad
            FROM Direccion d
            JOIN Ciudad c ON d.id_ciudad = c.id_ciudad
            """
        )
        direcciones = cursor.fetchall()

        if not direcciones:
            return jsonify({"message": "No se encontraron direcciones"}), 404

        return jsonify(direcciones), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
        
        
@app.route('/direcciones/<int:id_direccion>', methods=['GET'])
def get_direccion_by_id(id_direccion):
    """
    Obtener una dirección por su ID.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT d.id_direccion, d.direccion_principal, d.direccion_secundaria, d.codigo_postal, c.nombre_ciudad AS ciudad, p.nombre_provincia AS provincia, pa.nombre_pais AS pais
            FROM Direccion d
            JOIN Ciudad c ON d.id_ciudad = c.id_ciudad
            JOIN Provincia p ON c.id_provincia = p.id_provincia
            JOIN Pais pa ON p.id_pais = pa.id_pais
            WHERE d.id_direccion = %s
        """, (id_direccion,))
        
        direccion = cursor.fetchone()

        if direccion:
            return jsonify(direccion), 200
        else:
            return jsonify({"message": "Dirección no encontrada"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/direcciones/<id_direccion>', methods=['PUT'])
def actualizar_direccion(id_direccion):
    """
    Actualizar uno o más campos de una dirección existente.
    """
    datos = request.json
    direccion_principal = datos.get('direccion_principal')
    direccion_secundaria = datos.get('direccion_secundaria')
    codigo_postal = datos.get('codigo_postal')
    id_ciudad = datos.get('id_ciudad')

    # Verificar que al menos un campo haya sido proporcionado
    if not any([direccion_principal, direccion_secundaria, codigo_postal, id_ciudad]):
        return jsonify({"error": "Debe proporcionar al menos un campo para actualizar"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si la dirección existe
        cursor.execute("SELECT * FROM Direccion WHERE id_direccion = %s", (id_direccion,))
        if not cursor.fetchone():
            return jsonify({"error": "Dirección no encontrada"}), 404

        # Construir dinámicamente la consulta de actualización
        campos_actualizar = []
        valores = []

        if direccion_principal:
            campos_actualizar.append("direccion_principal = %s")
            valores.append(direccion_principal)
        if direccion_secundaria:
            campos_actualizar.append("direccion_secundaria = %s")
            valores.append(direccion_secundaria)
        if codigo_postal:
            campos_actualizar.append("codigo_postal = %s")
            valores.append(codigo_postal)
        if id_ciudad:
            # Verificar si la ciudad existe antes de actualizar
            cursor.execute("SELECT * FROM Ciudad WHERE id_ciudad = %s", (id_ciudad,))
            if not cursor.fetchone():
                return jsonify({"error": "Ciudad no encontrada"}), 404
            campos_actualizar.append("id_ciudad = %s")
            valores.append(id_ciudad)

        # Añadir el ID de la dirección al final de los valores
        valores.append(id_direccion)

        # Ejecutar la consulta de actualización
        consulta = f"""
            UPDATE Direccion 
            SET {', '.join(campos_actualizar)}
            WHERE id_direccion = %s
        """
        cursor.execute(consulta, tuple(valores))
        conn.commit()

        return jsonify({"message": "Dirección actualizada exitosamente"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/direcciones/<id_direccion>', methods=['DELETE'])
def eliminar_direccion(id_direccion):
    """
    Eliminar una dirección por su ID.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si la dirección existe
        cursor.execute("SELECT * FROM Direccion WHERE id_direccion = %s", (id_direccion,))
        if not cursor.fetchone():
            return jsonify({"error": "Dirección no encontrada"}), 404

        # Eliminar dirección
        cursor.execute("DELETE FROM Direccion WHERE id_direccion = %s", (id_direccion,))
        conn.commit()

        return jsonify({"message": "Dirección eliminada exitosamente"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# Gestión de País
@app.route('/paises', methods=['POST'])
def agregar_pais():
    """
    Agregar un nuevo país.
    """
    datos = request.json
    nombre_pais = datos.get('nombre_pais')

    if not nombre_pais:
        return jsonify({"error": "El campo 'nombre_pais' es obligatorio"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO PAIS (NOMBRE_PAIS) VALUES (%s) RETURNING ID_PAIS", (nombre_pais,))
        pais_id = cursor.fetchone()[0]
        conn.commit()

        return jsonify({"message": "País registrado exitosamente", "id_pais": pais_id}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/paises', methods=['GET'])
def listar_paises():
    """
    Listar todos los países.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM PAIS")
        paises = cursor.fetchall()

        return jsonify(paises), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/paises/<id_pais>', methods=['PUT'])
def actualizar_pais(id_pais):
    """
    Actualizar un país.
    """
    datos = request.json
    nuevo_nombre = datos.get('nombre_pais')

    if not nuevo_nombre:
        return jsonify({"error": "El campo 'nombre_pais' es obligatorio"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE PAIS SET NOMBRE_PAIS = %s WHERE ID_PAIS = %s", (nuevo_nombre, id_pais))
        conn.commit()

        return jsonify({"message": "País actualizado exitosamente"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/paises/<id_pais>', methods=['DELETE'])
def eliminar_pais(id_pais):
    """
    Eliminar un país.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si el país está asociado a alguna provincia
        cursor.execute("SELECT * FROM PROVINCIA WHERE ID_PAIS = %s", (id_pais,))
        if cursor.fetchone():
            return jsonify({"error": "No se puede eliminar el país porque está asociado a una provincia"}), 400

        cursor.execute("DELETE FROM PAIS WHERE ID_PAIS = %s", (id_pais,))
        conn.commit()

        return jsonify({"message": "País eliminado exitosamente"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# Gestión de Provincia
@app.route('/provincias', methods=['POST'])
def agregar_provincia():
    """
    Agregar una nueva provincia asociada a un país.
    """
    datos = request.json
    nombre_provincia = datos.get('nombre_provincia')
    id_pais = datos.get('id_pais')

    if not nombre_provincia or not id_pais:
        return jsonify({"error": "Los campos 'nombre_provincia' y 'id_pais' son obligatorios"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si el país existe
        cursor.execute("SELECT * FROM Pais WHERE id_pais = %s", (id_pais,))
        if not cursor.fetchone():
            return jsonify({"error": "País no encontrado"}), 404

        # Insertar la provincia
        cursor.execute(
            "INSERT INTO Provincia (nombre_provincia, id_pais) VALUES (%s, %s) RETURNING id_provincia", 
            (nombre_provincia, id_pais)
        )
        id_provincia = cursor.fetchone()[0]
        conn.commit()

        return jsonify({"message": "Provincia registrada exitosamente", "id_provincia": id_provincia}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/provincias/<id_provincia>', methods=['PUT'])
def actualizar_provincia(id_provincia):
    """
    Actualizar una provincia.
    """
    datos = request.json
    nuevo_nombre_provincia = datos.get('nombre_provincia')

    if not nuevo_nombre_provincia:
        return jsonify({"error": "El campo 'nombre_provincia' es obligatorio"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Actualizar el nombre de la provincia
        cursor.execute(
            "UPDATE Provincia SET nombre_provincia = %s WHERE id_provincia = %s", 
            (nuevo_nombre_provincia, id_provincia)
        )
        if cursor.rowcount == 0:
            return jsonify({"error": "Provincia no encontrada"}), 404

        conn.commit()
        return jsonify({"message": "Provincia actualizada exitosamente"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# Gestión de Ciudad
@app.route('/ciudades', methods=['POST'])
def agregar_ciudad():
    """
    Agregar una nueva ciudad asociada a una provincia.
    """
    datos = request.json
    nombre_ciudad = datos.get('nombre_ciudad')
    id_provincia = datos.get('id_provincia')

    if not nombre_ciudad or not id_provincia:
        return jsonify({"error": "Los campos 'nombre_ciudad' y 'id_provincia' son obligatorios"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si la provincia existe
        cursor.execute("SELECT * FROM Provincia WHERE id_provincia = %s", (id_provincia,))
        if not cursor.fetchone():
            return jsonify({"error": "Provincia no encontrada"}), 404

        # Insertar la ciudad
        cursor.execute(
            "INSERT INTO Ciudad (nombre_ciudad, id_provincia) VALUES (%s, %s) RETURNING id_ciudad",
            (nombre_ciudad, id_provincia)
        )
        id_ciudad = cursor.fetchone()[0]
        conn.commit()

        return jsonify({"message": "Ciudad registrada exitosamente", "id_ciudad": id_ciudad}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/ciudades', methods=['GET'])
def listar_ciudades():
    """
    Listar todas las ciudades.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT c.id_ciudad, c.nombre_ciudad AS ciudad, p.nombre_provincia AS provincia, pa.nombre_pais AS pais
            FROM Ciudad c
            JOIN Provincia p ON c.id_provincia = p.id_provincia
            JOIN Pais pa ON p.id_pais = pa.id_pais
        """)
        ciudades = cursor.fetchall()

        return jsonify(ciudades), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/ciudades/<id_ciudad>', methods=['PUT'])
def modificar_ciudad(id_ciudad):
    """
    Modificar los datos de una ciudad por su ID.
    """
    datos = request.json
    nuevo_nombre_ciudad = datos.get('nombre_ciudad')
    nueva_id_provincia = datos.get('id_provincia')

    if not nuevo_nombre_ciudad and not nueva_id_provincia:
        return jsonify({"error": "Debe proporcionar al menos 'nombre_ciudad' o 'id_provincia' para actualizar"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si la ciudad existe
        cursor.execute("SELECT * FROM Ciudad WHERE id_ciudad = %s", (id_ciudad,))
        if not cursor.fetchone():
            return jsonify({"error": "Ciudad no encontrada"}), 404

        # Si se va a actualizar la provincia, verificar que exista
        if nueva_id_provincia:
            cursor.execute("SELECT * FROM Provincia WHERE id_provincia = %s", (nueva_id_provincia,))
            if not cursor.fetchone():
                return jsonify({"error": "Provincia no encontrada"}), 404

        # Construir la consulta dinámica para actualizar
        campos_a_actualizar = []
        valores = []

        if nuevo_nombre_ciudad:
            campos_a_actualizar.append("nombre_ciudad = %s")
            valores.append(nuevo_nombre_ciudad)

        if nueva_id_provincia:
            campos_a_actualizar.append("id_provincia = %s")
            valores.append(nueva_id_provincia)

        valores.append(id_ciudad)  # ID de la ciudad para la cláusula WHERE
        consulta_actualizacion = f"UPDATE Ciudad SET {', '.join(campos_a_actualizar)} WHERE id_ciudad = %s"

        # Ejecutar la actualización
        cursor.execute(consulta_actualizacion, tuple(valores))
        conn.commit()

        return jsonify({"message": "Ciudad actualizada exitosamente"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@app.route('/ciudades/<int:id_ciudad>', methods=['GET'])
def get_ciudad_by_id(id_ciudad):
    """
    Obtener una ciudad por su ID.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT c.id_ciudad, c.nombre_ciudad AS ciudad, p.nombre_provincia AS provincia, pa.nombre_pais AS pais
            FROM Ciudad c
            JOIN Provincia p ON c.id_provincia = p.id_provincia
            JOIN Pais pa ON p.id_pais = pa.id_pais
            WHERE c.id_ciudad = %s
        """, (id_ciudad,))
        
        ciudad = cursor.fetchone()

        if ciudad:
            return jsonify(ciudad), 200
        else:
            return jsonify({"message": "Ciudad no encontrada"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@app.route('/ciudades/<id_ciudad>', methods=['DELETE'])
def eliminar_ciudad(id_ciudad):
    """
    Eliminar una ciudad por su ID.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si la ciudad está asociada a alguna dirección
        cursor.execute("SELECT * FROM Direccion WHERE id_ciudad = %s", (id_ciudad,))
        if cursor.fetchone():
            return jsonify({"error": "No se puede eliminar la ciudad porque está asociada a una dirección"}), 400

        # Eliminar la ciudad
        cursor.execute("DELETE FROM Ciudad WHERE id_ciudad = %s", (id_ciudad,))
        if cursor.rowcount == 0:
            return jsonify({"error": "Ciudad no encontrada"}), 404

        conn.commit()
        return jsonify({"message": "Ciudad eliminada exitosamente"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
