"""
main.py
───────
Punto de entrada del simulador de WhatsApp por terminal.

Responsabilidades:
  • Inicializar la base de datos (archivos JSON).
  • Pedir el número de teléfono con el que se quiere iniciar sesión.
  • Ejecutar el loop de conversación: leer entrada → procesar → mostrar respuesta.

No contiene lógica de negocio ni acceso a datos: solo orquesta los módulos.
"""

import sys

from config import RESET, VERDE, CIAN, AMARILLO, GRIS, ROJO
from base_de_datos import inicializar_base_de_datos
from interfaz import (
    mostrar_encabezado,
    mostrar_lista_usuarios,
    mostrar_burbuja_bot,
    mostrar_burbuja_usuario,
    mostrar_linea_separadora,
)
from estados import procesar_mensaje

COMANDOS_SALIDA = {"salir", "exit", "quit", "/salir"}


def solicitar_telefono() -> str:
    """Pide al usuario que ingrese su número de WhatsApp para autenticarse."""
    print(f"{CIAN}Ingresá tu número de WhatsApp para iniciar sesión:{RESET}")
    print(f"{GRIS}(copiá uno de la lista de arriba){RESET}")
    return input(f"\n  {AMARILLO}📱 Teléfono > {RESET}").strip()


def construir_id_sesion(telefono: str) -> str:
    """Genera el identificador único de sesión a partir del teléfono."""
    return f"WA_{telefono.replace('+', '').replace(' ', '')}"


def main() -> None:
    inicializar_base_de_datos()
    mostrar_encabezado()
    mostrar_lista_usuarios()

    telefono  = solicitar_telefono()
    if not telefono:
        print(f"{ROJO}Número vacío. Saliendo.{RESET}")
        sys.exit(1)

    id_sesion = construir_id_sesion(telefono)
    mostrar_encabezado()
    print(f"{GRIS}  Conectado como: {AMARILLO}{telefono}{RESET}\n")
    mostrar_linea_separadora()

    # Primer mensaje del usuario (saludo inicial)
    mostrar_burbuja_usuario("Hola 👋")
    respuesta_bienvenida = procesar_mensaje(id_sesion, "Hola", telefono)
    mostrar_burbuja_bot(respuesta_bienvenida)

    # Loop principal de conversación
    while True:
        try:
            mostrar_linea_separadora()
            entrada_usuario = input(f"  {VERDE}✏  Vos > {RESET}").strip()

            if not entrada_usuario:
                continue
            if entrada_usuario.lower() in COMANDOS_SALIDA:
                print(f"\n  {GRIS}👋 Sesión cerrada. ¡Hasta luego!{RESET}\n")
                break

            mostrar_burbuja_usuario(entrada_usuario)
            respuesta = procesar_mensaje(id_sesion, entrada_usuario, telefono)
            mostrar_burbuja_bot(respuesta)

        except KeyboardInterrupt:
            print(f"\n\n  {GRIS}👋 Sesión interrumpida.{RESET}\n")
            break


if __name__ == "__main__":
    main()
