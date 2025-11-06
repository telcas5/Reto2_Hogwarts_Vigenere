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
import os
import sys

# --- Constantes ---
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

FILE_ORIGINAL = os.path.join(DATA_DIR, "mensaje.txt")
FILE_CIFRADO = os.path.join(DATA_DIR, "mensaje_cifrado.txt")
FILE_DESCIFRADO = os.path.join(DATA_DIR, "mensaje_descifrado.txt")

def limpiar_texto(texto: str) -> str:
    """
    Convierte el texto a mayúsculas y elimina caracteres no alfabéticos.

    Args:
        texto (str): Texto a limpiar.

    Returns:
        str: Texto limpio solo con letras mayúsculas.
    """
    return ''.join(c for c in texto.upper() if c in string.ascii_uppercase)

def leer_fichero(path: str) -> str:
    """
    Lee el contenido de un fichero de texto.

    Intenta primero en UTF-8, si falla prueba con latin-1.

    Args:
        path (str): Ruta del fichero.

    Returns:
        str: Contenido del fichero (sin saltos finales), o cadena vacía si error.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except UnicodeDecodeError:
        try:
            with open(path, 'r', encoding='latin-1') as f:
                return f.read().strip()
        except (UnicodeDecodeError, OSError) as e:
            print(f"Error leyendo {path}: {e}")
            return ""
    except OSError as e:
        print(f"Error leyendo {path}: {e}")
        return ""

def escribir_fichero(path: str, contenido: str) -> None:
    """
    Escribe contenido en un fichero de texto con codificación UTF-8.

    Args:
        path (str): Ruta del fichero.
        contenido (str): Texto a escribir.
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(contenido)
    except OSError as e:
        print(f"Error escribiendo {path}: {e}")

def ajustar_clave(texto: str, clave: str) -> str:
    """
    Ajusta la clave para que coincida en longitud con el texto.

    Args:
        texto (str): Texto cuya longitud usar.
        clave (str): Clave original.

    Returns:
        str: Clave repetida o cortada para igualar longitud.

    Raises:
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

    Args:
        texto (str): Texto original.
        clave (str): Clave para cifrado.

    Returns:
        str: Texto cifrado.

    Raises:
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
    return ''.join(resultado)

def descifrar_vigenere(texto_cifrado: str, clave: str) -> str:
    """
    Descifra un texto cifrado con Vigenère.

    Args:
        texto_cifrado (str): Texto cifrado.
        clave (str): Clave usada para cifrado.

    Returns:
        str: Texto original descifrado.

    Raises:
        ValueError: Si la clave está vacía.
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
    return ''.join(resultado)

def main():
    """
    Punto de entrada del programa. Ofrece menú para cifrar/descifrar por consola o ficheros.
    Controla errores específicos y muestra resultados.
    
    Raises:
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
            mensaje = leer_fichero(FILE_ORIGINAL)
            if not mensaje:
                print(f"No se pudo leer el fichero {FILE_ORIGINAL}")
                return
            clave = input("Introduce la clave: ")
            texto_cifrado = cifrar_vigenere(mensaje, clave)
            escribir_fichero(FILE_CIFRADO, texto_cifrado)
            print(f"Mensaje cifrado guardado en {FILE_CIFRADO}")

        elif opcion == '4':
            mensaje_cifrado = leer_fichero(FILE_CIFRADO)
            if not mensaje_cifrado:
                print(f"No se pudo leer el fichero {FILE_CIFRADO}")
                return
            clave = input("Introduce la clave: ")
            texto_descifrado = descifrar_vigenere(mensaje_cifrado, clave)
            escribir_fichero(FILE_DESCIFRADO, texto_descifrado)
            print(f"Mensaje descifrado guardado en {FILE_DESCIFRADO}")

        else:
            print("Opción no válida. Elige un número entre 1 y 4.")

    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario.")
        sys.exit(0)

    except (FileNotFoundError, ValueError, OSError) as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    main()
