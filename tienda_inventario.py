# ============================================================
#   SISTEMA DE TIENDA E INVENTARIO
#   Proyecto Python - Conceptos fundamentales
# ============================================================
#   Temas cubiertos:
#   - Variables y tipos de datos
#   - Operadores aritméticos y lógicos
#   - Estructuras de control (if/elif/else, for, while, break, continue)
#   - Funciones con parámetros, retorno y lambda
#   - Listas, tuplas y diccionarios
#   - Manejo de errores
#   - Buenas prácticas: modularización y comentarios
# ============================================================


# ─────────────────────────────────────────────────────────────
# SECCIÓN 1: Constantes y datos globales (Variables y tipos)
# ─────────────────────────────────────────────────────────────

NOMBRE_TIENDA: str = "Mi Tienda"
STOCK_MINIMO: int = 5           # Alerta si hay menos de esta cantidad
IVA: float = 0.16               # 16% de impuesto
ACTIVO: bool = True             # Estado del sistema

# Categorías disponibles (tupla → datos inmutables)
CATEGORIAS: tuple = ("Alimentos", "Bebidas", "Limpieza", "Electrónica", "Otro")

# Inventario: lista de diccionarios
inventario: list = []


# ─────────────────────────────────────────────────────────────
# SECCIÓN 2: Funciones de utilidad
# ─────────────────────────────────────────────────────────────

def separador(caracter: str = "─", largo: int = 48) -> None:
    """Imprime una línea decorativa."""
    print(caracter * largo)


def pausar() -> None:
    """Espera a que el usuario presione Enter."""
    input("\n  Presiona Enter para continuar...")


# Función lambda: calcula precio con IVA
precio_con_iva = lambda precio: round(precio * (1 + IVA), 2)

# Función lambda: verifica si el stock es bajo
stock_bajo = lambda cantidad: cantidad < STOCK_MINIMO


# ─────────────────────────────────────────────────────────────
# SECCIÓN 3: Validación de entradas (Manejo de errores)
# ─────────────────────────────────────────────────────────────

def pedir_texto(mensaje: str) -> str:
    """Pide un texto y valida que no esté vacío."""
    while True:
        try:
            valor: str = input(mensaje).strip()
            if len(valor) < 2:
                print("  ⚠  Escribe al menos 2 caracteres.")
                continue
            return valor
        except (EOFError, KeyboardInterrupt):
            return ""


def pedir_entero(mensaje: str, minimo: int = 0, maximo: int = 9999) -> int:
    """Pide un número entero con validación de rango."""
    while True:
        try:
            valor: int = int(input(mensaje))
            if not (minimo <= valor <= maximo):
                print(f"  ⚠  Ingresa un número entre {minimo} y {maximo}.")
                continue
            return valor
        except ValueError:
            print("  ⚠  Eso no es un número válido.")


def pedir_flotante(mensaje: str, minimo: float = 0.01) -> float:
    """Pide un número decimal con validación."""
    while True:
        try:
            valor: float = float(input(mensaje).replace(",", "."))
            if valor < minimo:
                print(f"  ⚠  El valor mínimo es {minimo}.")
                continue
            return valor
        except ValueError:
            print("  ⚠  Ingresa un número válido (ejemplo: 12.50).")


# ─────────────────────────────────────────────────────────────
# SECCIÓN 4: Lógica del inventario (Estructuras de datos)
# ─────────────────────────────────────────────────────────────

def buscar_producto(nombre: str) -> dict | None:
    """Busca un producto por nombre (sin distinguir mayúsculas)."""
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            return producto
    return None


def mostrar_producto(p: dict) -> None:
    """Muestra los datos de un producto con formato."""
    separador()
    print(f"  Nombre    : {p['nombre']}")
    print(f"  Categoría : {p['categoria']}")
    print(f"  Precio    : ${p['precio']:.2f}  (con IVA: ${precio_con_iva(p['precio'])})")
    print(f"  Stock     : {p['stock']} unidades", end="")
    # Operador lógico: agrega alerta si el stock es bajo
    if stock_bajo(p["stock"]):
        print("  ⚠  STOCK BAJO")
    else:
        print()
    separador()


# ─────────────────────────────────────────────────────────────
# SECCIÓN 5: Opciones del menú
# ─────────────────────────────────────────────────────────────

def agregar_producto() -> None:
    """Registra un nuevo producto en el inventario."""
    print("\n  ── AGREGAR PRODUCTO ──")

    nombre: str = pedir_texto("  Nombre del producto : ")
    if not nombre:
        return

    # Verificar duplicados
    if buscar_producto(nombre):
        print(f"  ⚠  Ya existe un producto llamado '{nombre}'.")
        pausar()
        return

    # Mostrar categorías disponibles (uso de for + tupla)
    print("\n  Categorías:")
    for i, cat in enumerate(CATEGORIAS, start=1):
        print(f"    {i}. {cat}")

    num_cat: int = pedir_entero("  Elige el número de categoría: ", 1, len(CATEGORIAS))
    categoria: str = CATEGORIAS[num_cat - 1]

    precio: float = pedir_flotante("  Precio unitario ($): ")
    stock: int = pedir_entero("  Cantidad en stock  : ", 0, 9999)

    # Crear diccionario del producto
    producto: dict = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock,
    }

    inventario.append(producto)
    print(f"\n  ✓ Producto '{nombre}' agregado correctamente.")
    pausar()


def ver_producto() -> None:
    """Busca y muestra un producto específico."""
    print("\n  ── VER PRODUCTO ──")

    if not inventario:
        print("  No hay productos registrados.")
        pausar()
        return

    nombre: str = pedir_texto("  Nombre del producto: ")
    p: dict | None = buscar_producto(nombre)

    if p is None:
        print(f"  ✗ No se encontró '{nombre}'.")
    else:
        mostrar_producto(p)

    pausar()


def listar_productos() -> None:
    """Muestra todos los productos del inventario en tabla."""
    print("\n  ── INVENTARIO COMPLETO ──")

    if not inventario:
        print("  No hay productos registrados aún.")
        pausar()
        return

    separador()
    print(f"  {'Nombre':<20} {'Categoría':<12} {'Precio':>8}  {'Stock':>6}  {'Estado'}")
    separador()

    total_productos: int = 0
    alertas: int = 0

    for p in inventario:
        # continue: omite productos con precio 0 (datos corruptos)
        if p["precio"] <= 0:
            continue

        estado: str = "⚠ Bajo" if stock_bajo(p["stock"]) else "OK"
        print(f"  {p['nombre']:<20} {p['categoria']:<12} ${p['precio']:>7.2f}  {p['stock']:>6}  {estado}")

        total_productos += 1
        if stock_bajo(p["stock"]):
            alertas += 1

    separador()
    print(f"  Total: {total_productos} productos  |  Alertas de stock bajo: {alertas}")
    pausar()


def registrar_venta() -> None:
    """
    Registra la venta de un producto:
    reduce el stock y calcula el total a cobrar.
    """
    print("\n  ── REGISTRAR VENTA ──")

    if not inventario:
        print("  No hay productos en inventario.")
        pausar()
        return

    nombre: str = pedir_texto("  Producto a vender : ")
    p: dict | None = buscar_producto(nombre)

    if p is None:
        print(f"  ✗ No se encontró '{nombre}'.")
        pausar()
        return

    print(f"  Stock disponible: {p['stock']} unidades")

    # Validar que haya suficiente stock
    if p["stock"] == 0:
        print("  ✗ Sin stock disponible.")
        pausar()
        return

    cantidad: int = pedir_entero("  Cantidad a vender  : ", 1, p["stock"])

    # Operadores aritméticos: calcular totales
    subtotal: float = p["precio"] * cantidad
    impuesto: float = subtotal * IVA
    total: float = subtotal + impuesto

    # Reducir stock
    p["stock"] -= cantidad

    print(f"\n  ── TICKET DE VENTA ──")
    print(f"  Producto  : {p['nombre']}")
    print(f"  Cantidad  : {cantidad}")
    print(f"  Subtotal  : ${subtotal:.2f}")
    print(f"  IVA (16%) : ${impuesto:.2f}")
    print(f"  TOTAL     : ${total:.2f}")

    # Alerta automática si el stock quedó bajo
    if stock_bajo(p["stock"]):
        print(f"\n  ⚠  Aviso: stock de '{p['nombre']}' en nivel bajo ({p['stock']} uds).")

    pausar()


def reabastecer_producto() -> None:
    """Suma unidades al stock de un producto existente."""
    print("\n  ── REABASTECER PRODUCTO ──")

    if not inventario:
        print("  No hay productos registrados.")
        pausar()
        return

    nombre: str = pedir_texto("  Nombre del producto: ")
    p: dict | None = buscar_producto(nombre)

    if p is None:
        print(f"  ✗ No se encontró '{nombre}'.")
        pausar()
        return

    print(f"  Stock actual: {p['stock']} unidades")
    cantidad: int = pedir_entero("  Unidades a agregar: ", 1, 9999)

    p["stock"] += cantidad
    print(f"  ✓ Nuevo stock de '{p['nombre']}': {p['stock']} unidades.")
    pausar()


def resumen_inventario() -> None:
    """
    Muestra estadísticas generales del inventario.
    Usa operadores aritméticos y lógicos.
    """
    print("\n  ── RESUMEN DEL INVENTARIO ──")

    if not inventario:
        print("  No hay datos suficientes.")
        pausar()
        return

    total_productos: int = len(inventario)
    valor_total: float = sum(p["precio"] * p["stock"] for p in inventario)
    producto_caro = max(inventario, key=lambda p: p["precio"])
    producto_barato = min(inventario, key=lambda p: p["precio"])
    con_stock_bajo: list = [p["nombre"] for p in inventario if stock_bajo(p["stock"])]

    separador()
    print(f"  Productos registrados : {total_productos}")
    print(f"  Valor total inventario: ${valor_total:.2f}")
    print(f"  Producto más caro     : {producto_caro['nombre']} (${producto_caro['precio']:.2f})")
    print(f"  Producto más barato   : {producto_barato['nombre']} (${producto_barato['precio']:.2f})")
    separador()

    # Mostrar productos con stock bajo (uso de if + lista)
    if con_stock_bajo:
        print(f"  ⚠  Productos con stock bajo ({len(con_stock_bajo)}):")
        for nombre in con_stock_bajo:
            print(f"     - {nombre}")
    else:
        print("  ✓ Todos los productos tienen stock suficiente.")

    separador()
    pausar()


# ─────────────────────────────────────────────────────────────
# SECCIÓN 6: Menú principal (while + break)
# ─────────────────────────────────────────────────────────────

def mostrar_menu() -> None:
    """Imprime el menú principal."""
    print("\n" * 2)
    separador("═")
    print(f"  {NOMBRE_TIENDA} – Gestión de Inventario")
    separador("═")
    print("  1. Agregar producto")
    print("  2. Ver producto")
    print("  3. Listar inventario")
    print("  4. Registrar venta")
    print("  5. Reabastecer producto")
    print("  6. Resumen del inventario")
    print("  0. Salir")
    separador()


def main() -> None:
    """Función principal: controla el flujo con while y break."""
    print(f"\n  Bienvenido a {NOMBRE_TIENDA}")

    while ACTIVO:
        mostrar_menu()

        opcion: str = input("  Elige una opción: ").strip()

        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            ver_producto()
        elif opcion == "3":
            listar_productos()
        elif opcion == "4":
            registrar_venta()
        elif opcion == "5":
            reabastecer_producto()
        elif opcion == "6":
            resumen_inventario()
        elif opcion == "0":
            print("\n  ¡Hasta luego! Cerrando el sistema...\n")
            break   # Sale del bucle while
        else:
            print("  ⚠  Opción no válida. Intenta de nuevo.")


# ─────────────────────────────────────────────────────────────
# Punto de entrada
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
