# Cifrado/Descifrado Vigenère

## Descripción

Este módulo implementa el algoritmo de cifrado y descifrado Vigenère, con ejemplos prácticos de uso en ficheros. Permite cifrar y descifrar textos tanto desde la consola como desde ficheros de texto, gestionando adecuadamente errores y codificación.

---

## Funcionalidades

- Cifrado y descifrado de textos con el algoritmo de Vigenère.

- Lectura y escritura de ficheros de forma controlada con gestión de errores.

- Registro (logging) de eventos y errores, con posibilidad de guardar logs en fichero.

- Interfaz de línea de comandos con un menú para seleccionar opciones.

---

### Recomendaciones

- Usa clave alfabética no vacía para el cifrado.

- Asegúrate que los ficheros de texto están codificados en UTF-8.

- Mantén el archivo de logs logs.log para revisar eventos y errores.

### Ejecutar programa

Desde la consola, en la carpeta del proyecto:

python src/vigenere.py

El programa mostrará un menú con opciones para:

    1. Cifrar mensaje por consola.

    2. Descifrar mensaje por consola.

    3. Cifrar fichero de texto.

    4. Descifrar fichero de texto.

## Estructura de funciones principales

- cifrar_vigenere: cifra texto completo.

- descifrar_vigenere: descifra texto completo.

- leer_fichero y escribir_fichero: Funciones auxiliares para la gestión de ficheros con logging.

- ajustar_clave: ajusta la clave a la longitud necesaria.

## Autores

**Telmo Castillo**

**Erlantz García**

## Fecha:

10 de Noviembre de 2025