from flask import jsonify, request, flash, get_flashed_messages
from . import pedidos
from database import mysql
from datetime import datetime

@pedidos.route('/', methods=['GET'])
def listar_pedidos():

    cursor = mysql.connection.cursor()

    cursor.execute('SELECT * FROM pedidos')

    resultado = cursor.fetchall()

    datos = []

    for p in resultado:
        datos.append({
            'id_pedido': p[0],
            'nombre': p[1],
            'direccion': p[2],
            'telefono': p[3],
            'fecha_pedido': str(p[4]),
            'total': float(p[5])
        })

    cursor.close()

    return jsonify(datos)


@pedidos.route('/registrar', methods=['POST'])
def registrar_pedido():

    datos = request.get_json(silent=True)

    # 1. Comprobar que se recibieron datos
    if not isinstance(datos, dict):
        return jsonify({'mensaje': 'No se recibieron datos válidos'}), 400

    # 2. Obtener los datos del cliente
    nombre = str(datos.get('nombre') or '').strip()
    direccion = str(datos.get('direccion') or '').strip()
    telefono = str(datos.get('telefono') or '').strip()
    fecha = datos.get('fecha_pedido')
    pizzas = datos.get('pizzas')

    # 3. Validar los datos del cliente
    if not nombre:
        return jsonify({'mensaje': 'El nombre es obligatorio'}), 400

    if not direccion:
        return jsonify({'mensaje': 'La dirección es obligatoria'}), 400

    if not telefono:
        return jsonify({'mensaje': 'El teléfono es obligatorio'}), 400

    # 4. Validar la fecha
    try:
        datetime.strptime(fecha, '%Y-%m-%d')
    except (ValueError, TypeError):
        return jsonify({
            'mensaje': 'La fecha debe tener el formato YYYY-MM-DD'
        }), 400

    # 5. Validar que existan pizzas
    if not isinstance(pizzas, list) or len(pizzas) == 0:
        return jsonify({
            'mensaje': 'El pedido debe tener al menos una pizza'
        }), 400

    precios = {
        'Chica': 40,
        'Mediana': 80,
        'Grande': 120
    }

    ingredientes_validos = {
        'Jamón': 10,
        'Piña': 10,
        'Champiñones': 10
    }

    total = 0
    detalles = []

    # 6. Validar y calcular cada pizza
    for p in pizzas:

        if not isinstance(p, dict):
            return jsonify({
                'mensaje': 'Los datos de la pizza son incorrectos'
            }), 400

        tamano = p.get('tamano')
        cantidad_recibida = p.get('cantidad')
        ingredientes = p.get('ingredientes')

        if tamano not in precios:
            return jsonify({
                'mensaje': 'Tamaño de pizza incorrecto'
            }), 400

        # Validar cantidad
        try:
            cantidad = int(cantidad_recibida)

            if str(cantidad_recibida).strip() != str(cantidad):
                return jsonify({
                    'mensaje': 'La cantidad debe ser un número entero positivo'
                }), 400

            if cantidad <= 0:
                return jsonify({
                    'mensaje': 'La cantidad debe ser mayor a cero'
                }), 400

        except (ValueError, TypeError):
            return jsonify({
                'mensaje': 'La cantidad debe ser un número entero positivo'
            }), 400

        # Validar ingredientes
        if not isinstance(ingredientes, list):
            return jsonify({
                'mensaje': 'Los ingredientes deben enviarse en una lista'
            }), 400

        precio_tamano = precios[tamano]
        precio_ingredientes = 0

        for i in ingredientes:

            if not isinstance(i, dict):
                return jsonify({
                    'mensaje': 'Los datos del ingrediente son incorrectos'
                }), 400

            nombre_ingrediente = i.get('nombre')

            if nombre_ingrediente not in ingredientes_validos:
                return jsonify({
                    'mensaje': 'Ingrediente incorrecto'
                }), 400

            precio_ingredientes += ingredientes_validos[nombre_ingrediente]

        subtotal = (precio_tamano + precio_ingredientes) * cantidad

        total += subtotal

        detalles.append({
            'tamano': tamano,
            'cantidad': cantidad,
            'precio_tamano': precio_tamano,
            'subtotal': subtotal,
            'ingredientes': ingredientes
        })

    # 7. Registrar el pedido en MySQL
    cursor = mysql.connection.cursor()

    try:

        mysql.connection.begin()

        cursor.execute("""
            INSERT INTO pedidos
            (nombre, direccion, telefono, fecha_pedido, total)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, direccion, telefono, fecha, total))

        id_pedido = cursor.lastrowid

        for p in detalles:

            cursor.execute("""
                INSERT INTO detalle_pedido
                (id_pedido, tamano, cantidad, precio_tamano, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                id_pedido,
                p['tamano'],
                p['cantidad'],
                p['precio_tamano'],
                p['subtotal']
            ))

            id_detalle = cursor.lastrowid

            for i in p['ingredientes']:

                cursor.execute("""
                    INSERT INTO ingredientes_detalle
                    (id_detalle, ingrediente, precio)
                    VALUES (%s, %s, %s)
                """, (
                    id_detalle,
                    i['nombre'],
                    ingredientes_validos[i['nombre']]
                ))

        mysql.connection.commit()

        flash(
            'Pedido registrado correctamente. Total: $' + str(total),
            'success'
        )

        return jsonify({
            'mensaje': 'Pedido registrado correctamente',
            'id_pedido': id_pedido,
            'total': total,
            'mensajes': get_flashed_messages()
        }), 201

    except Exception as e:

        mysql.connection.rollback()

        return jsonify({'error': str(e)}), 500

    finally:

        cursor.close()


@pedidos.route('/detalle/<int:id_pedido>', methods=['GET'])
def detalle_pedido(id_pedido):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT nombre, direccion, telefono, fecha_pedido, total
        FROM pedidos
        WHERE id_pedido = %s
    """, (id_pedido,))

    pedido = cursor.fetchone()

    if not pedido:
        cursor.close()
        return jsonify({'mensaje': 'Pedido no encontrado'}), 404

    cursor.execute("""
        SELECT id_detalle, tamano, cantidad, precio_tamano, subtotal
        FROM detalle_pedido
        WHERE id_pedido = %s
    """, (id_pedido,))

    resultado = cursor.fetchall()

    pizzas = []

    for p in resultado:

        cursor.execute("""
            SELECT ingrediente, precio
            FROM ingredientes_detalle
            WHERE id_detalle = %s
        """, (p[0],))

        ingredientes = cursor.fetchall()

        lista_ingredientes = []

        for i in ingredientes:
            lista_ingredientes.append({
                'nombre': i[0],
                'precio': float(i[1])
            })

        pizzas.append({
            'tamano': p[1],
            'cantidad': p[2],
            'precio_tamano': float(p[3]),
            'subtotal': float(p[4]),
            'ingredientes': lista_ingredientes
        })

    cursor.close()

    return jsonify({
        'id_pedido': id_pedido,
        'nombre': pedido[0],
        'direccion': pedido[1],
        'telefono': pedido[2],
        'fecha_pedido': str(pedido[3]),
        'total': float(pedido[4]),
        'pizzas': pizzas
    })


@pedidos.route('/ventas/dia/<dia>', methods=['GET'])
def ventas_por_dia(dia):

    dias = {
        'lunes': 0,
        'martes': 1,
        'miércoles': 2,
        'miercoles': 2,
        'jueves': 3,
        'viernes': 4,
        'sábado': 5,
        'sabado': 5,
        'domingo': 6
    }

    dia = dia.lower().strip()

    if dia not in dias:
        return jsonify({
            'mensaje': 'Día de la semana incorrecto'
        }), 400

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT id_pedido, nombre, direccion, telefono,
               fecha_pedido, total
        FROM pedidos
        WHERE WEEKDAY(fecha_pedido) = %s
    """, (dias[dia],))

    resultado = cursor.fetchall()

    ventas = []
    total_dia = 0

    for p in resultado:

        total_dia += float(p[5])

        ventas.append({
            'id_pedido': p[0],
            'nombre': p[1],
            'direccion': p[2],
            'telefono': p[3],
            'fecha_pedido': str(p[4]),
            'total': float(p[5])
        })

    cursor.close()

    return jsonify({
        'dia': dia,
        'ventas': ventas,
        'cantidad_pedidos': len(ventas),
        'total_dia': total_dia
    })


@pedidos.route('/ventas/mes/<mes>', methods=['GET'])
@pedidos.route('/ventas/mes/<mes>/<int:anio>', methods=['GET'])
def ventas_por_mes(mes, anio=None):

    meses = {
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'setiembre': 9,
        'octubre': 10,
        'noviembre': 11,
        'diciembre': 12
    }

    mes = mes.lower().strip()

    if mes not in meses:
        return jsonify({
            'mensaje': 'Mes incorrecto'
        }), 400

    cursor = mysql.connection.cursor()

    if anio is not None:
        cursor.execute("""
            SELECT id_pedido, nombre, direccion, telefono,
                   fecha_pedido, total
            FROM pedidos
            WHERE MONTH(fecha_pedido) = %s
            AND YEAR(fecha_pedido) = %s
        """, (meses[mes], anio))
    else:
        cursor.execute("""
            SELECT id_pedido, nombre, direccion, telefono,
                   fecha_pedido, total
            FROM pedidos
            WHERE MONTH(fecha_pedido) = %s
        """, (meses[mes],))

    resultado = cursor.fetchall()

    ventas = []
    total_mes = 0

    for p in resultado:

        total_mes += float(p[5])

        ventas.append({
            'id_pedido': p[0],
            'nombre': p[1],
            'direccion': p[2],
            'telefono': p[3],
            'fecha_pedido': str(p[4]),
            'total': float(p[5])
        })

    cursor.close()

    return jsonify({
        'mes': mes,
        'anio': anio,
        'ventas': ventas,
        'cantidad_pedidos': len(ventas),
        'total_mes': total_mes
    })
