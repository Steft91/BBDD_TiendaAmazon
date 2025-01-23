from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

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
    """Validar los campos requeridos para un producto."""
    required_fields = ['nombre', 'descripcion', 'precio', 'stock', 'proveedor_id', 'categoria_id']
    for field in required_fields:
        if field not in producto or producto[field] is None:
            raise ValueError(f"El campo '{field}' es obligatorio.")
        
        
@app.route('/productos', methods=['POST'])
def add_producto():
    """Agregar un producto a la base de datos."""
    producto = request.json
    try:
        validate_producto_data(producto)  # Validar datos de entrada
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO PRODUCTO (NOMBRE, DESCRIPCION, PRECIO, STOCK, ID_PROVEEDOR, ID_CATEGORIA)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (producto['nombre'], producto['descripcion'], producto['precio'],
             producto['stock'], producto['proveedor_id'], producto['categoria_id'])
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
    """Actualizar un producto existente (parcial o completo)."""
    datos = request.json
    if not datos:
        return jsonify({"error": "No se enviaron datos para actualizar"}), 400

    campos = []
    valores = []

    # Construir dinámicamente la consulta SQL a partir de los campos enviados
    for campo in ['nombre', 'descripcion', 'precio', 'stock', 'proveedor_id', 'categoria_id']:
        if campo in datos:
            campos.append(f"{campo.upper()} = %s")
            valores.append(datos[campo])
    
    if not campos:
        return jsonify({"error": "No se enviaron campos válidos para actualizar"}), 400

    # Agregar el id_producto como último parámetro para el WHERE
    valores.append(id_producto)
    consulta_sql = f"UPDATE PRODUCTO SET {', '.join(campos)} WHERE ID_PRODUCTO = %s"

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
    """
    Registrar una nueva compra con opción de combinar GiftCard y Tarjeta.
    """
    datos = request.json
    cliente_id = datos.get('cliente_id')
    productos = datos.get('productos')  # Lista de {Id_Producto, cantidad}
    metodo_pago = datos.get('metodo_pago')  # GiftCard, Tarjeta o Combinado
    detalles_pago = datos.get('detalles_pago')  # GiftCard y/o Tarjeta

    # Validación inicial
    if not cliente_id or not productos or not metodo_pago:
        return jsonify({"error": "Campos obligatorios: cliente_id, productos, metodo_pago"}), 400
    if metodo_pago not in ["GiftCard", "Tarjeta", "Combinado"]:
        return jsonify({"error": "Método de pago inválido"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar cliente
        cursor.execute("SELECT * FROM Cliente WHERE Id_Cliente = %s", (cliente_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Cliente no encontrado"}), 404

        # Calcular precio total de los productos
        total = 0
        for producto in productos:
            producto_id = producto.get('Id_Producto')
            cantidad = producto.get('cantidad')
            if not producto_id or not cantidad:
                return jsonify({"error": "Cada producto debe tener Id_Producto y cantidad"}), 400

            cursor.execute("SELECT Precio, Descuento, Stock FROM Producto WHERE Id_Producto = %s", (producto_id,))
            producto_data = cursor.fetchone()
            if not producto_data:
                return jsonify({"error": f"Producto con ID {producto_id} no encontrado"}), 404
            precio, descuento, stock = producto_data

            if stock < cantidad:
                return jsonify({"error": f"Stock insuficiente para el producto {producto_id}"}), 400

            precio_final = precio * (1 - descuento / 100)
            total += precio_final * cantidad

        # Manejar métodos de pago
        saldo_giftcard = 0
        if metodo_pago in ["GiftCard", "Combinado"]:
            gift_card_id = detalles_pago.get('gift_card_id')
            cursor.execute("SELECT Saldo FROM GiftCard WHERE Id_Gift = %s", (gift_card_id,))
            gift_card_data = cursor.fetchone()
            if not gift_card_data:
                return jsonify({"error": "GiftCard no encontrada"}), 404
            saldo_giftcard = gift_card_data[0]

        restante = total
        if metodo_pago == "GiftCard":
            if saldo_giftcard < total:
                return jsonify({"error": "Saldo insuficiente en la GiftCard"}), 400
            restante = 0
            cursor.execute("UPDATE GiftCard SET Saldo = Saldo - %s WHERE Id_Gift = %s", (total, gift_card_id))

        elif metodo_pago == "Combinado":
            if saldo_giftcard >= total:
                restante = 0
                cursor.execute("UPDATE GiftCard SET Saldo = Saldo - %s WHERE Id_Gift = %s", (total, gift_card_id))
            else:
                restante = total - saldo_giftcard
                cursor.execute("UPDATE GiftCard SET Saldo = 0 WHERE Id_Gift = %s", (gift_card_id,))

        if metodo_pago in ["Tarjeta", "Combinado"] and restante > 0:
            tarjeta_data = detalles_pago.get('tarjeta')
            if not tarjeta_data:
                return jsonify({"error": "Se requieren detalles de la tarjeta"}), 400
            cursor.execute(
                """
                SELECT * FROM Tarjeta WHERE Num_Tarjeta = %s AND Nombre = %s 
                AND Fecha_Vencimiento = %s AND CVV = %s
                """,
                (
                    tarjeta_data.get('num_tarjeta'),
                    tarjeta_data.get('nombre'),
                    tarjeta_data.get('fecha_vencimiento'),
                    tarjeta_data.get('cvv'),
                ),
            )
            if not cursor.fetchone():
                return jsonify({"error": "Detalles de tarjeta inválidos"}), 400

        # Registrar la compra
        impuesto = total * 0.12
        precio_total = total + impuesto
        cursor.execute(
            """
            INSERT INTO Compra (Id_Cliente, Importe, Impuesto, Precio_Total, Metodo_Pago, Fecha) 
            VALUES (%s, %s, %s, %s, %s, NOW()) RETURNING Id_Compra
            """,
            (cliente_id, total, impuesto, precio_total, metodo_pago),
        )
        compra_id = cursor.fetchone()[0]

        # Registrar productos y reducir stock
        for producto in productos:
            producto_id = producto.get('Id_Producto')
            cantidad = producto.get('cantidad')
            cursor.execute("UPDATE Producto SET Stock = Stock - %s WHERE Id_Producto = %s", (cantidad, producto_id))
            cursor.execute(
                "INSERT INTO Compra_Producto (Id_Compra, Id_Producto, Cantidad) VALUES (%s, %s, %s)",
                (compra_id, producto_id, cantidad),
            )

        conn.commit()
        return jsonify({"message": "Compra registrada exitosamente", "compra_id": compra_id}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
        
        
@app.route('/compras/<cliente_id>', methods=['GET'])
def historial_compras(cliente_id):
    """
    Consultar el historial de compras de un cliente.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            """
            SELECT c.Id_Compra, c.Fecha, c.Precio_Total, cp.Id_Producto, cp.Cantidad, 
                   p.Nombre AS Producto, p.Precio, p.Descuento
            FROM Compra c
            JOIN Compra_Producto cp ON c.Id_Compra = cp.Id_Compra
            JOIN Producto p ON cp.Id_Producto = p.Id_Producto
            WHERE c.Id_Cliente = %s
            ORDER BY c.Fecha DESC
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
        cursor.close()
        conn.close()



@app.route('/compra/<compra_id>', methods=['GET'])
def detalle_compra(compra_id):
    """
    Obtener detalles de una compra específica.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            """
            SELECT c.Id_Compra, c.Fecha, c.Metodo_Pago, cp.Id_Producto, cp.Cantidad, 
                   p.Nombre AS Producto, p.Precio
            FROM Compra c
            JOIN Compra_Producto cp ON c.Id_Compra = cp.Id_Compra
            JOIN Producto p ON cp.Id_Producto = p.Id_Producto
            WHERE c.Id_Compra = %s
            """,
            (compra_id,)
        )
        compra = cursor.fetchall()

        if not compra:
            return jsonify({"message": "Compra no encontrada"}), 404

        return jsonify(compra), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
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

# # Ruta para obtener los productos del carrito
# @app.route('/carrito', methods=['GET'])
# def get_carrito():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(cursor_factory=RealDictCursor)
#         cursor.execute("SELECT * FROM COMPRA")
#         carrito = cursor.fetchall()
#         return jsonify(carrito)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         cursor.close()
#         conn.close()

# # Ruta para agregar un producto al carrito
# @app.route('/carrito', methods=['POST'])
# def add_carrito():
#     data = request.json
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("""
#             INSERT INTO COMPRA (id_direccion, id_cliente, impuestos, importe, precio_total)
#             VALUES (%s, %s, %s, %s, %s) RETURNING id_compra
#         """, (data['id_direccion'], data['id_cliente'], data['impuestos'], data['importe'], data['precio_total']))
#         conn.commit()
#         return jsonify({"message": "Producto agregado al carrito"}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         cursor.close()
#         conn.close()

# # Ruta para actualizar un producto en el carrito
# @app.route('/carrito/<int:id_producto>', methods=['PUT'])
# def update_carrito(id_producto):
#     data = request.json
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("""
#             UPDATE COMPRA SET cantidad = %s WHERE id_producto = %s
#         """, (data['cantidad'], id_producto))
#         conn.commit()
#         return jsonify({"message": "Cantidad actualizada"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         cursor.close()
#         conn.close()

# # Ruta para eliminar un producto del carrito
# @app.route('/carrito/<int:id_producto>', methods=['DELETE'])
# def delete_carrito(id_producto):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("DELETE FROM COMPRA WHERE id_producto = %s", (id_producto,))
#         conn.commit()
#         return jsonify({"message": "Producto eliminado del carrito"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         cursor.close()
#         conn.close()
   



if __name__ == '__main__':
    app.run(debug=True)
