"""
Práctica _ Cifrado y Descifrado con el algoritmo de Vigenère.     
Alumno/a: Telmo Castillo
Unidad Didáctica: UD1 - Python

Implementación del cifrado Vigenère con ejemplos de uso en ficheros.

Incluye:
- Funciones para cifrar y descifrar textos.
- Funciones auxiliares para leer y escribir ficheros.
- Control de errores y codificación.
- Ejemplo de uso en la función main().
"""

import string
import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

# --- Constantes ---
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent / "data"
RESULTS_DIR = DATA_DIR / "1_Resultados"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def limpiar_texto(texto: str) -> str:
    """
    Convierte el texto a mayúsculas y elimina caracteres no alfabéticos.

    Parámetros:
        texto (str): Texto a limpiar.

    Retorna:
        str: Texto limpio solo con letras mayúsculas.
    """
    return ''.join(c for c in texto.upper() if c in string.ascii_uppercase)

def leer_fichero(path: str) -> str:
    """
    Lee el contenido de un fichero de texto.

    Intenta primero en UTF-8, si falla prueba con latin-1.

    Parámetros:
        path (str): Ruta del fichero.

    Retorna:
        str: Contenido del fichero (sin saltos finales), o cadena vacía si error.
    
    Excepción:
        OSError: Si ocurre un error al leer el fichero.
    """
    try:
        logging.info("Leyendo fichero %s", path)
        return path.read_text(encoding="utf-8").strip()
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
    
    Excepción:
        OSError: Si ocurre un error al escribir el fichero.
    """
    try:
        logging.info("Escribiendo en fichero %s", path)
        path.write_text(contenido, encoding='utf-8')
    except FileNotFoundError as e:
        logging.error("Archivo no encontrado %s: %s", path, e)
    except PermissionError as e:
        logging.error("Permiso denegado en %s: %s", path, e)
    except OSError as e:
        logging.error("Error en el sistema de ficheros para %s: %s", path, e)

def ajustar_clave(texto: str, clave: str) -> str:
    """
    Ajusta la clave para que coincida en longitud con el texto.

    Parámetros:
        texto (str): Texto cuya longitud usar.
        clave (str): Clave original.

    Retorna:
        str: Clave repetida o cortada para igualar longitud.

    Excepción:
        ValueError: Si la clave está vacía después de limpieza.
    """
    clave_limpia = limpiar_texto(clave)
    if not clave_limpia:
        raise ValueError("La clave no puede estar vacía.")
    longitud = len(limpiar_texto(texto))
    return (clave_limpia * (longitud // len(clave_limpia) + 1))[:longitud]

def cifrar_vigenere(texto: str, clave: str) -> str:
    """
    Cifra el texto con el algoritmo de Vigenère.

    Parámetros:
        texto (str): Texto original.
        clave (str): Clave para cifrado.

    Retorna:
        str: Texto cifrado.

    Excepción:
        ValueError: Si la clave está vacía.
    """
    texto_limpio = limpiar_texto(texto)
    clave_ajustada = ajustar_clave(texto_limpio, clave)
    resultado = []
    for t_char, k_char in zip(texto_limpio, clave_ajustada):
        # Convertir letras a posiciones 0-25
        t_pos = ord(t_char) - ord('A')
        k_pos = ord(k_char) - ord('A')
        # Sumar y modular para evitar salir del rango
        c_pos = (t_pos + k_pos) % 26
        resultado.append(chr(c_pos + ord('A')))
    logging.info("Texto cifrado correctamente.")
    return ''.join(resultado)

def descifrar_vigenere(texto_cifrado: str, clave: str) -> str:
    """
    Descifra un texto cifrado con Vigenère.

    Parámetros:
        texto_cifrado (str): Texto cifrado.
        clave (str): Clave usada para cifrado.

    Retorna:
        str: Texto original descifrado.
    """
    texto_limpio = limpiar_texto(texto_cifrado)
    clave_ajustada = ajustar_clave(texto_limpio, clave)
    resultado = []
    for c_char, k_char in zip(texto_limpio, clave_ajustada):
        c_pos = ord(c_char) - ord('A')
        k_pos = ord(k_char) - ord('A')
        # Restar, y ajustar si negativa sumando 26
        t_pos = (c_pos - k_pos + 26) % 26
        resultado.append(chr(t_pos + ord('A')))
    logging.info("Texto descifrado correctamente.")
    return ''.join(resultado)

def main():
    """
    Punto de entrada del programa. Ofrece menú para cifrar/descifrar por consola o ficheros.
    Controla errores específicos y muestra resultados.
    
    Excepción:
        ValueError: Si la clave está vacía.
    """
    print("=== Cifrado y Descifrado Vigenère ===")
    print("Opciones:")
    print("1 - Cifrar mensaje por consola")
    print("2 - Descifrar mensaje por consola")
    print("3 - Cifrar mensaje desde fichero")
    print("4 - Descifrar mensaje desde fichero")

    opcion = input("Selecciona opción (1-4): ").strip()

    try:
        if opcion == '1':
            mensaje = input("Introduce el mensaje a cifrar: ")
            clave = input("Introduce la clave: ")
            texto_cifrado = cifrar_vigenere(mensaje, clave)
            print(f"Mensaje cifrado: {texto_cifrado}")

        elif opcion == '2':
            mensaje = input("Introduce el mensaje cifrado: ")
            clave = input("Introduce la clave: ")
            texto_descifrado = descifrar_vigenere(mensaje, clave)
            print(f"Mensaje descifrado: {texto_descifrado}")

        elif opcion == '3':
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

        elif opcion == '4':
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

        else:
            print("Opción no válida. Elige un número entre 1 y 4.")

    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario.")
        sys.exit(0)

    except (ValueError, OSError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
