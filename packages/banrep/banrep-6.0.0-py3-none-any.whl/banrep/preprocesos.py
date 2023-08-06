# coding: utf-8
"""Módulo para funciones de preprocesamiento de texto."""
import re


def filtrar_cortas(texto, chars=0):
    """Filtra líneas en texto de longitud chars o inferior.

    Parameters
    ----------
    texto : str
        Texto que se quiere filtrar.
    chars : int
        Mínimo número de caracteres en una línea de texto.

    Returns
    -------
    str
       Texto filtrado.
    """
    filtrado = ""
    for linea in texto.splitlines():
        if len(linea) > chars:
            filtrado += linea + "\n"

    return filtrado


def unir_fragmentos(texto):
    """Une fragmentos de palabras partidas por final de línea.

    Parameters
    ----------
    texto : str

    Returns
    -------
    str
        Texto con palabras de fin de línea unidas si estaban partidas.
    """
    # Asume ord('-') == 45
    return re.sub(r'-\n+', '', texto)


def separar_guiones(texto):
    """Separa guiones de primera y última palabra de fragmentos de texto.

    Parameters
    ----------
    texto : str

    Returns
    -------
    str
        Texto con guiones de fragmentos separados de las palabras.
    """
    # Asume ord 8211 ó 8212
    nuevo = re.sub(r'[—–]{1,}', '–', texto)
    nuevo = re.sub(r'(\W)–([A-Za-zÀ-Üà-ü]+)', r'\1– \2', nuevo)

    return re.sub(r'([A-Za-zÀ-Üà-ü]+)–(\W)', r'\1 –\2', nuevo)


def separar_numeros(texto):
    """Separa números de palabras que los tienen.

    Parameters
    ----------
    texto : str

    Returns
    -------
    str
        Texto con números separados de palabras.
    """
    nuevo = re.sub(r'(\d+)([A-Za-zÀ-Üà-ü]{2,}?|\()', r'\1 \2', texto)

    return re.sub(r'([A-Za-zÀ-Üà-ü]{2,}?|\))(\d+)', r'\1 \2', nuevo)


def limpiar_extraccion(texto, chars=0, basura=None):
    """Limpieza de texto extraido.

    Parameters
    ----------
    texto : str
    chars : int
        Mínimo número de caracteres en una línea de texto.
    basura : Iterable
        Caracteres a eliminar.

    Returns
    -------
    str
       Texto procesado.
    """
    limpio = unir_fragmentos(texto)
    limpio = separar_guiones(limpio)
    limpio = separar_numeros(limpio)

    if chars:
        limpio = filtrar_cortas(limpio, chars=chars)

    if basura:
        limpio = re.sub(f"[{''.join(basura)}]", '', limpio)

    return ' '.join(limpio.split())
