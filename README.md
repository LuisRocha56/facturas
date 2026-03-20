Procesador de Facturas XML

Descripción

Este proyecto es una aplicación de escritorio desarrollada en Python que
permite procesar facturas en formato XML y extraer automáticamente
información relevante.

A través de una interfaz gráfica, el usuario puede seleccionar múltiples
archivos XML, procesarlos y almacenar los datos en un archivo de Excel
de forma estructurada y acumulativa.

Funcionalidades

-   Selección de múltiples archivos XML
-   Extracción automática de datos de facturación
-   Generación y actualización de archivo Excel
-   Interfaz gráfica intuitiva (Tkinter)
-   Barra de progreso durante el procesamiento
-   Registro de errores en archivo log
-   Prevención de archivos duplicados

Datos extraídos

El programa obtiene la siguiente información de cada factura:

-   Fecha
-   Número de factura
-   Nombre del proveedor
-   RFC
-   Subtotal
-   IVA
-   Total

Además, calcula automáticamente: - Suma total de todas las facturas
procesadas

Tecnologías utilizadas

-   Python
-   Tkinter (interfaz gráfica)
-   Pandas (manejo de datos)
-   ElementTree (procesamiento de XML)
-   OpenPyXL (exportación a Excel)
-   Logging (registro de errores)

Instalación

1.  Clona este repositorio:

git clone https://github.com/tu-usuario/tu-repo.git cd tu-repo

2.  Instala las dependencias necesarias:

pip install pandas openpyxl

Uso

1.  Ejecuta el programa:

python nombre_del_archivo.py

2.  Dentro de la aplicación:

-   Haz clic en “Elegir Guardar Excel” y selecciona dónde se guardará el
    archivo.
-   Haz clic en “Elegir Facturas” y selecciona uno o varios archivos
    XML.
-   Presiona “Procesar Facturas” para iniciar el análisis.

3.  Al finalizar:

-   Se generará o actualizará el archivo Excel con la información.
-   Si ocurre algún error, se registrará en el archivo
    procesamiento_facturas.log.

Notas

-   El programa está diseñado para trabajar con diferentes estructuras
    de XML, incluyendo variaciones comunes en etiquetas.
-   Si el archivo Excel ya existe, los nuevos datos se agregan sin
    eliminar los anteriores.
-   Los archivos ya procesados no se duplican en la misma ejecución.

Objetivo

Este proyecto tiene como objetivo automatizar la captura y organización
de datos de facturas, reduciendo el trabajo manual y facilitando su
análisis.
