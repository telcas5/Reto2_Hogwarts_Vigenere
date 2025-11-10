"""
Cifrado y Descifrado con el algoritmo de Vigenère. 

Este módulo implementa el algoritmo de cifrado y descifrado Vigenère 
con ejemplos de uso en ficheros.

Incluye:
- Funciones auxiliares para la gestión de ficheros.
- Control de errores y codificación.
- Ejemplo de uso en la función main(), que permite operaciones por consola y ficheros.

Excepciones:
- ValueError: Claves vacías o no válidas.
- OSError: Errores en lectura/escritura de ficheros.

Autores: Telmo Castillo y Erlantz García
Fecha: 10 de Noviembre de 2025
"""

# TODO: Hacer que lea por grupos de BYTES
# TODO: El segundo punto de puntos extra

import sys
import logging
from pathlib import Path

# Para configurar el sistema de logging
logging.basicConfig(
    filename='logs.log',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


# Constantes
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent / "data"
RESULTS_DIR = DATA_DIR / "1_Resultados"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def leer_fichero(path: str):
    """
    Lee el contenido de un fichero de texto.

    Parámetros:
        path (str): Ruta del fichero.

    Retorna:
        str: Conenido leído del fichero sin saltos finales, o una cadena cacía si da error.
    
    Excepciones:
        OSError: Si ocurre un error al leer el fichero.
    """
    try:
        logging.info("Leyendo fichero %s", path)
        contenido = path.read_text(encoding="utf-8").strip()
        logging.debug("Contenido leído.")
        return contenido
    except FileNotFoundError as e:
        logging.error("Archivo no encontrado %s: %s", path, e)
    except PermissionError as e:
        logging.error("Permiso denegado en %s: %s", path, e)
    except OSError as e:
        logging.error("Error en el sistema de ficheros para %s: %s", path, e)


def escribir_fichero(path: str, contenido: str) -> None:
    """
    Escribe contenido en un fichero de texto con codificación UTF-8.

    Parámetros:
        path (str): Ruta del fichero.
        contenido (str): Texto a escribir.
    
    Excepciones:
        OSError: Si ocurre un error al escribir el fichero.
    """
    try:
        logging.info("Escribiendo en fichero %s", path)
        path.write_text(contenido, encoding='utf-8')
        logging.debug("Contenido escrito.")
    except FileNotFoundError as e:
        logging.error("Archivo no encontrado %s: %s", path, e)
    except PermissionError as e:
        logging.error("Permiso denegado en %s: %s", path, e)
    except OSError as e:
        logging.error("Error en el sistema de ficheros para %s: %s", path, e)


def ajustar_clave(texto: str, clave: str) -> str:
    """
    Ajusta la clave para que coincida en longitud coincida con el 
    número de caracteres alfabéticos del texto.

    Parámetros:
        texto (str): Texto base para medir longitud.
        clave (str): Clave original.

    Retorna:
        str: Clave repetida o recortada para igualar la longitud del texto (solo letras).

    Excepciones:
        ValueError: Si la clave está vacía después de limpieza.
    """
    clave_filtrada = ''.join(c for c in clave if c.isalpha())
    logging.debug("Clave filtrada")
    if not clave_filtrada:
        raise ValueError("La clave no puede estar vacía.")
    longitud = 0
    for c in texto:
        if c.isalpha():
            longitud += 1
    clave_ajustada = (clave_filtrada * (longitud // len(clave_filtrada) + 1))[:longitud]
    logging.debug("Clave ajustada correctamente.")
    return clave_ajustada


def cifrar_vigenere(texto: str, clave: str) -> str:
    """
    Cifra un texto usando el algoritmo de Vigenère.

    Parámetros:
        texto (str): Texto original a cifrar.
        clave (str): Clave para el cifrado.

    Retorna:
        str: Texto cifrado, preservando mayúsculas, minúsculas y caracteres no alfabéticos.

    Excepciones:
        ValueError: Si la clave está vacía o es inválida.
    """
    clave_ajustada = ajustar_clave(texto, clave)
    resultado = []
    idx_clave = 0

    for c in texto:
        if c.isalpha():
            k = clave_ajustada[idx_clave].lower()
            k_offset = ord(k) - ord('a')
            base = ord('A') if c.isupper() else ord('a')
            nueva_letra = chr((ord(c) - base + k_offset) % 26 + base)
            resultado.append(nueva_letra)
            idx_clave += 1
        else:
            resultado.append(c)

    logging.info("Texto cifrado correctamente.")
    return ''.join(resultado)


def descifrar_vigenere(texto_cifrado: str, clave: str) -> str:
    """
    Descifra un texto cifrado con el algoritmo de Vigenère.

    Parámetros:
        texto_cifrado (str): Texto cifrado a descifrar.
        clave (str): Clave usada para el cifrado.

    Retorna:
        str: Texto original descifrado, preservando mayúsculas, minúsculas 
        y caracteres no alfabéticos.
    
        Excepciones:
            ValueError: Si la clave está vacía o es inválida.
    """
    clave_ajustada = ajustar_clave(texto_cifrado, clave)
    resultado = []
    idx_clave = 0

    for c in texto_cifrado:
        if c.isalpha():
            k = clave_ajustada[idx_clave].lower()
            k_offset = ord(k) - ord('a')
            base = ord('A') if c.isupper() else ord('a')
            nueva_letra = chr((ord(c) - base - k_offset + 26) % 26 + base)
            resultado.append(nueva_letra)
            idx_clave += 1
        else:
            resultado.append(c)

    logging.info("Texto descifrado correctamente.")
    return ''.join(resultado)


def main():
    """
    Punto de entrada del programa. 
    
    Ofrece menú para cifrar y descifrar mensajes por consola o ficheros,
    controlado errores específicos y mostrando resultados.
    
    Excepciones:
        ValueError: Si la clave está vacía o es inválida.
        OSError: Errores en la lectura o escritura del ficheros.
        KeyboardInterrupt: Interrupción manual por el usuario.
    """
    print("=== Cifrado y Descifrado Vigenère ===")
    print("Opciones:")
    print("1 - Cifrar mensaje por consola")
    print("2 - Descifrar mensaje por consola")
    print("3 - Cifrar mensaje desde fichero")
    print("4 - Descifrar mensaje desde fichero")

    opcion = input("Selecciona opción (1-4): ").strip()
    logging.info("Opción seleccionada: %s", opcion)

    try:
        match opcion:
            case '1':
                mensaje = input("Introduce el mensaje a cifrar: ")
                clave = input("Introduce la clave: ")
                texto_cifrado = cifrar_vigenere(mensaje, clave)
                print(f"Mensaje cifrado: {texto_cifrado}")
            case '2':
                mensaje = input("Introduce el mensaje cifrado: ")
                clave = input("Introduce la clave: ")
                texto_descifrado = descifrar_vigenere(mensaje, clave)
                print(f"Mensaje descifrado: {texto_descifrado}")
            case '3':
                nombre_fichero = input("Introduce el nombre del fichero a cifrar: ")
                path_original = DATA_DIR / nombre_fichero
                if not path_original.is_file():
                    print(f"Error: no se encontró el fichero '{nombre_fichero}'")
                    return
                clave = input("Introduce la clave: ")
                mensaje = leer_fichero(path_original)
                texto_cifrado = cifrar_vigenere(mensaje, clave)
                nombre_sin_ext = path_original.stem
                path_salida = RESULTS_DIR / f"{nombre_sin_ext}_cifrado.txt"
                escribir_fichero(path_salida, texto_cifrado)
                print(f"Mensaje cifrado guardado en {path_salida}")
            case '4':
                nombre_fichero = input("Introduce el nombre del fichero a descifrar: ")
                path_cifrado = DATA_DIR / nombre_fichero
                if not path_cifrado.is_file():
                    print(f"Error: no se encontró el fichero '{nombre_fichero}'")
                    return
                clave = input("Introduce la clave: ")
                mensaje_cifrado = leer_fichero(path_cifrado)
                texto_descifrado = descifrar_vigenere(mensaje_cifrado, clave)
                nombre_sin_ext = path_cifrado.stem
                path_salida = RESULTS_DIR / f"{nombre_sin_ext}_descifrado.txt"
                escribir_fichero(path_salida, texto_descifrado)
                print(f"Mensaje descifrado guardado en {path_salida}")
            case _:
                print("Opción no válida. Elige un número entre 1 y 4.")

    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario.")
        logging.warning("Ejecución interrumpida por el usuario. ")
        sys.exit(0)

    except (ValueError, OSError) as e:
        logging.error("Error: %s", e)
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
