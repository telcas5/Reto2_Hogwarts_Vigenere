"""
Pruebas automáticas para el algoritmo de cifrado Vigenère.

Este fichero incluye diferentes tests usando pytest:
- Casos básicos de cifrado y descifrado.
- Manejo de minúsculas y espacios.
- Claves más cortas que el texto.
- Textos vacíos.
- Frases largas.
- Cifrado y descifrado de ficheros.

Además, se añade control para que los tests se salten en caso
de que no exista el fichero src/vigenere.py.
"""

import pytest
import sys
import os
import importlib.util

# --- Localización automática de vigenere.py ---
# Buscamos el archivo vigenere.py dentro de src/ relativo a la carpeta de este test
base_path = os.path.dirname(__file__)
src_path = os.path.join(base_path, "..", "src", "vigenere.py")

# Verificamos si existe el fichero
vigenere_disponible = os.path.exists(src_path)

# Si existe, lo cargamos dinámicamente con importlib
if vigenere_disponible:
    spec = importlib.util.spec_from_file_location("vigenere", src_path)
    vigenere = importlib.util.module_from_spec(spec)
    sys.modules["vigenere"] = vigenere
    spec.loader.exec_module(vigenere)

    # Importamos las funciones que vamos a probar
    cifrar_vigenere = vigenere.cifrar_vigenere
    descifrar_vigenere = vigenere.descifrar_vigenere


@pytest.mark.skipif(not vigenere_disponible, reason="No se encuentra vigenere.py en src/")
def test_cifrado_y_descifrado_basico():
    """
    Prueba básica: verifica que cifrar y luego descifrar devuelve el texto original.
    """
    texto = "ATAQUE"
    clave = "CLAVE"
    cifrado = cifrar_vigenere(texto, clave)
    assert cifrado == "CEALYG"
    descifrado = descifrar_vigenere(cifrado, clave)
    assert descifrado == texto


@pytest.mark.skipif(not vigenere_disponible, reason="No se encuentra vigenere.py en src/")
def test_minusculas_y_espacios():
    """
    Prueba que se eliminan espacios y que las minúsculas se convierten a mayúsculas.
    """
    texto = "ataque sorpresa"
    clave = "clave"
    cifrado = cifrar_vigenere(texto, clave)
    descifrado = descifrar_vigenere(cifrado, clave)
    assert descifrado == "ATAQUESORPRESA"


@pytest.mark.skipif(not vigenere_disponible, reason="No se encuentra vigenere.py en src/")
def test_clave_mas_corta():
    """
    Prueba que si la clave es más corta que el texto, se repite hasta cubrir la longitud.
    En este caso, como la clave es 'A', el cifrado debe devolver exactamente el mismo texto.
    """
    texto = "PYTHON"
    clave = "A"
    cifrado = cifrar_vigenere(texto, clave)
    assert cifrado == "PYTHON"
    descifrado = descifrar_vigenere(cifrado, clave)
    assert descifrado == texto


@pytest.mark.skipif(not vigenere_disponible, reason="No se encuentra vigenere.py en src/")
def test_texto_vacio():
    """
    Prueba que el comportamiento con un texto vacío no produce errores y devuelve vacío.
    """
    texto = ""
    clave = "CLAVE"
    cifrado = cifrar_vigenere(texto, clave)
    assert cifrado == ""
    descifrado = descifrar_vigenere(cifrado, clave)
    assert descifrado == ""


@pytest.mark.skipif(not vigenere_disponible, reason="No se encuentra vigenere.py en src/")
def test_frase_larga():
    """
    Prueba con una frase más larga que incluye espacios.
    Se espera que al descifrar se recupere el texto limpio sin espacios.
    """
    texto = "PROGRAMACION EN PYTHON"
    clave = "SEGURIDAD"
    cifrado = cifrar_vigenere(texto, clave)
    descifrado = descifrar_vigenere(cifrado, clave)
    assert descifrado == "PROGRAMACIONENPYTHON"


@pytest.mark.skipif(not vigenere_disponible, reason="No se encuentra vigenere.py en src/")
def test_cifrado_y_descifrado_ficheros(tmp_path):
    """
    Prueba el cifrado y descifrado trabajando con ficheros.

    1. Se crea un fichero temporal 'mensaje.txt'.
    2. Se cifra su contenido y se guarda en 'mensaje_cifrado.txt'.
    3. Se descifra el resultado y se guarda en 'mensaje_descifrado.txt'.
    4. Se verifica que el texto final coincide con el original, en mayúsculas y sin espacios.
    """
    clave = "CLAVE"

    # Crear un fichero temporal con un mensaje
    mensaje_path = tmp_path / "mensaje.txt"
    mensaje_path.write_text("Este es un mensaje de prueba.")

    # Leer contenido y cifrar
    original = mensaje_path.read_text()
    cifrado = cifrar_vigenere(original, clave)

    mensaje_cifrado_path = tmp_path / "mensaje_cifrado.txt"
    mensaje_cifrado_path.write_text(cifrado)

    # Leer el cifrado y descifrar
    contenido_cifrado = mensaje_cifrado_path.read_text()
    descifrado = descifrar_vigenere(contenido_cifrado, clave)

    mensaje_descifrado_path = tmp_path / "mensaje_descifrado.txt"
    mensaje_descifrado_path.write_text(descifrado)

    # Validación
    assert descifrado == "ESTEESUNMENSAJEDEPRUEBA"
    assert mensaje_descifrado_path.read_text() == "ESTEESUNMENSAJEDEPRUEBA"

@pytest.mark.skipif(not vigenere_disponible, reason="No se encuentra vigenere.py en src/")
def test_clave_vacia():
    """
    Prueba que el uso de una clave vacía lanza un error controlado.
    Lo esperado es que la función lance un ValueError.
    """
    texto = "PRUEBA"
    clave = ""

    with pytest.raises(ValueError):
        cifrar_vigenere(texto, clave)

    with pytest.raises(ValueError):
        descifrar_vigenere("ABCDEF", clave)