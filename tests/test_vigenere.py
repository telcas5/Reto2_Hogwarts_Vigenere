"""
Pruebas automáticas para el algoritmo de cifrado Vigenère.

Este fichero incluye diferentes tests usando pytest:
- Casos básicos de cifrado y descifrado.
- Manejo de mayúsculas, minúsculas y caracteres no alfabéticos.
- Claves más cortas que el texto.
- Textos vacíos.
- Frases largas.
- Cifrado y descifrado de ficheros.
- Control de errores y excepciones.

Además, se añade control para que los tests se salten
si no existe el fichero src/vigenere.py.
"""

import pytest
import sys
import os
import importlib.util

# --- Localización de vigenere.py ---
base_path = os.path.dirname(__file__)
src_path = os.path.join(base_path, "..", "src", "vigenere.py")
vigenere_disponible = os.path.exists(src_path)

if vigenere_disponible:
    spec = importlib.util.spec_from_file_location("vigenere", src_path)
    vigenere = importlib.util.module_from_spec(spec)
    sys.modules["vigenere"] = vigenere
    spec.loader.exec_module(vigenere)

    cifrar_vigenere = vigenere.cifrar_vigenere
    descifrar_vigenere = vigenere.descifrar_vigenere
    ajustar_clave = vigenere.ajustar_clave
    escribir_fichero = vigenere.escribir_fichero
    leer_fichero = vigenere.leer_fichero

@pytest.mark.skipif(not vigenere_disponible, reason="No se encuentra vigenere.py en src/")
def test_cifrado_y_descifrado_basico():
    texto = "ATAQUE"
    clave = "CLAVE"
    cifrado = cifrar_vigenere(texto, clave)
    assert isinstance(cifrado, str)
    descifrado = descifrar_vigenere(cifrado, clave)
    assert descifrado == texto

@pytest.mark.skipif(not vigenere_disponible, reason="No se encuentra vigenere.py en src/")
def test_mayusculas_minusculas_y_simbolos():
    texto = "Ataque al Amanecer!"
    clave = "Clave"
    cifrado = cifrar_vigenere(texto, clave)
    descifrado = descifrar_vigenere(cifrado, clave)
    assert descifrado == texto

@pytest.mark.skipif(not vigenere_disponible, reason="No se encuentra vigenere.py en src/")
def test_clave_mas_corta():
    texto = "PYTHON"
    clave = "A"  # Desplazamiento 0
    cifrado = cifrar_vigenere(texto, clave)
    assert cifrado == "PYTHON"
    descifrado = descifrar_vigenere(cifrado, clave)
    assert descifrado == texto

@pytest.mark.skipif(not vigenere_disponible, reason="No se encuentra vigenere.py en src/")
def test_texto_vacio():
    texto = ""
    clave = "CLAVE"
    cifrado = cifrar_vigenere(texto, clave)
    assert cifrado == ""
    descifrado = descifrar_vigenere(cifrado, clave)
    assert descifrado == ""

@pytest.mark.skipif(not vigenere_disponible, reason="No se encuentra vigenere.py en src/")
def test_frase_larga_con_espacios_y_puntuacion():
    texto = "PROGRAMACIÓN EN PYTHON ES DIVERTIDA."
    clave = "SEGURIDAD"
    cifrado = cifrar_vigenere(texto, clave)
    descifrado = descifrar_vigenere(cifrado, clave)
    assert "PYTHON" in descifrado
    assert descifrado.endswith("DIVERTIDA.")

@pytest.mark.skipif(not vigenere_disponible, reason="No se encuentra vigenere.py en src/")
def test_ajustar_clave_correcta():
    texto = "ABCDEF"
    clave = "XYZ"
    resultado = ajustar_clave(texto, clave)
    assert len(resultado) == 6
    assert resultado.startswith("XYZ")

@pytest.mark.skipif(not vigenere_disponible, reason="No se encuentra vigenere.py en src/")
def test_clave_vacia():
    texto = "PRUEBA"
    clave = ""
    with pytest.raises(ValueError):
        cifrar_vigenere(texto, clave)
    with pytest.raises(ValueError):
        descifrar_vigenere("ABCDEF", clave)

@pytest.mark.skipif(not vigenere_disponible, reason="No se encuentra vigenere.py en src/")
def test_cifrado_y_descifrado_ficheros(tmp_path):
    clave = "CLAVE"
    original_text = "Mensaje de prueba."
    mensaje_path = tmp_path / "mensaje.txt"
    mensaje_path.write_text(original_text)

    contenido = leer_fichero(mensaje_path)
    cifrado = cifrar_vigenere(contenido, clave)
    cifrado_path = tmp_path / "mensaje_cifrado.txt"
    escribir_fichero(cifrado_path, cifrado)

    cifrado_leido = leer_fichero(cifrado_path)
    descifrado = descifrar_vigenere(cifrado_leido, clave)
    descifrado_path = tmp_path / "mensaje_descifrado.txt"
    escribir_fichero(descifrado_path, descifrado)

    final = leer_fichero(descifrado_path)
    assert final == original_text
