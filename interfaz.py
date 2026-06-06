"""
interfaz.py
───────────
Capa de presentación del simulador.

Responsabilidades:
  • Simular el indicador de "escribiendo..." que se ve en WhatsApp.
  • Imprimir las burbujas de chat del bot (izquierda) y del usuario (derecha).
  • Mostrar la barra de título, la línea separadora y la lista de usuarios.

No contiene lógica de negocio ni accede a la máquina de estados.
"""

import os
import sys
import time
from datetime import datetime

from config import (
    RESET, NEGRITA,
    VERDE, CIAN, AMARILLO, GRIS, BLANCO,
    FONDO_BOT, FONDO_USUARIO, FONDO_CABECERA,
)
from base_de_datos import listar_todos_los_usuarios


# ─── Constantes de presentación ───────────────────────────────────────────────

ANCHO_PANTALLA          = 65   # columnas de referencia para alinear burbujas
ANCHO_MAXIMO_BURBUJA    = 58   # máximo de caracteres por línea en burbuja bot
TIEMPO_ESCRITURA_MS     = 600  # milisegundos que dura la animación de "escribiendo"
LONGITUD_LINEA_SEPARADORA = 65


# ─────────────────────────────────────────────────────────────────────────────
# Utilidades internas
# ─────────────────────────────────────────────────────────────────────────────

def _limpiar_pantalla() -> None:
    os.system("clear" if os.name != "nt" else "cls")


def _timestamp_actual() -> str:
    return datetime.now().strftime("%H:%M")


# ─────────────────────────────────────────────────────────────────────────────
# Elementos visuales públicos
# ─────────────────────────────────────────────────────────────────────────────

def simular_escritura() -> None:
    """Muestra el indicador animado 'escribiendo...' y lo borra al terminar."""
    sys.stdout.write(f"  {GRIS}⬤ ⬤ ⬤  escribiendo...{RESET}")
    sys.stdout.flush()
    time.sleep(TIEMPO_ESCRITURA_MS / 1000)
    sys.stdout.write("\r" + " " * 35 + "\r")
    sys.stdout.flush()


def mostrar_burbuja_bot(texto: str) -> None:
    """
    Imprime el mensaje del bot como burbuja izquierda (estilo WhatsApp).
    Espera la animación de escritura antes de mostrar el contenido.
    """
    simular_escritura()

    lineas = texto.split("\n")
    ancho_contenido = min(
        max(len(linea) for linea in lineas) + 4,
        ANCHO_MAXIMO_BURBUJA,
    )

    print(f"\n  {GRIS}Bot Vacaciones{RESET}")
    for linea in lineas:
        print(f"  {FONDO_BOT}{BLANCO}  {linea:<{ancho_contenido - 4}}  {RESET}")
    print(f"  {GRIS}{_timestamp_actual()}{RESET}\n")


def mostrar_burbuja_usuario(texto: str) -> None:
    """
    Imprime el mensaje del usuario como burbuja derecha (estilo WhatsApp).
    """
    etiqueta = "Vos"
    print(f"\n{' ' * (ANCHO_PANTALLA - len(etiqueta) - 2)}{GRIS}{etiqueta}{RESET}")
    for linea in texto.split("\n"):
        relleno_derecho = max(ANCHO_PANTALLA - len(linea) - 6, 0)
        print(f"    {FONDO_USUARIO}{BLANCO}  {linea}  {' ' * relleno_derecho}{RESET}")
    print(f"{' ' * (ANCHO_PANTALLA - len(_timestamp_actual()) - 1)}"
          f"{GRIS}{_timestamp_actual()}{RESET}\n")


def mostrar_linea_separadora() -> None:
    print(f"{GRIS}{'─' * LONGITUD_LINEA_SEPARADORA}{RESET}")


def mostrar_encabezado() -> None:
    """Borra la pantalla y muestra la barra de título verde del chat."""
    _limpiar_pantalla()
    print(f"\n{FONDO_CABECERA}{BLANCO}{NEGRITA}"
          f"  📱  Bot Gestión de Vacaciones   {'':>30}{RESET}")
    print(f"{GRIS}  Simulador WhatsApp — Persistencia en JSON{RESET}\n")
    mostrar_linea_separadora()


def mostrar_lista_usuarios() -> None:
    """
    Lista todos los usuarios registrados con nombre, teléfono y rol.
    Facilita seleccionar con qué número iniciar sesión durante las pruebas.
    """
    todos_los_usuarios = listar_todos_los_usuarios()
    print(f"\n{CIAN}{NEGRITA}👥 USUARIOS DEL SISTEMA:{RESET}")
    print(f"{GRIS}{'─' * 60}{RESET}")
    print(f"{GRIS}  {'Nombre':<26} {'Teléfono':<22} Rol{RESET}")
    print(f"{GRIS}{'─' * 60}{RESET}")
    for usuario in todos_los_usuarios:
        icono_rol = "👔" if usuario["rol"] == "GERENTE" else "👤"
        print(
            f"  {icono_rol} {usuario['nombre_completo']:<25} "
            f"{AMARILLO}{usuario['telefono']:<21}{RESET}"
            f"{GRIS}{usuario['rol']}{RESET}"
        )
    print(f"{GRIS}{'─' * 60}{RESET}\n")
