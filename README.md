Descripción
Este proyecto permite procesar facturas en formato PDF y extraer automáticamente información relevante de cada documento.
Los datos obtenidos se almacenan en un archivo de Excel, facilitando la organización y el análisis de múltiples facturas en un solo lugar.
________________________________________
Funcionamiento
El flujo del programa es el siguiente:
1.	Se ingresan uno o varios archivos PDF de facturas.
2.	El programa analiza el contenido de cada archivo.
3.	Se extraen campos clave de cada factura (según la lógica implementada).
4.	La información se guarda en un archivo de Excel.
El archivo de Excel es acumulativo, lo que significa que:
•	Cada vez que se procesan nuevas facturas, los datos se agregan al mismo archivo.
•	No se sobrescribe la información previamente almacenada.
________________________________________
Características
•	Procesamiento automático de facturas en PDF
•	Extracción de datos relevantes
•	Generación de archivo Excel
•	Almacenamiento acumulativo de información
•	Fácil de usar
________________________________________
Tecnologías
(Aquí puedes especificar las tecnologías utilizadas, por ejemplo:)
•	Python
•	Librerías para lectura de PDF (como PyPDF, pdfplumber, etc.)
•	OpenPyXL o Pandas para manejo de Excel
________________________________________
Uso
1.	Coloca los archivos PDF en la carpeta correspondiente.
2.	Ejecuta el programa.
3.	Revisa el archivo Excel generado con la información procesada.
________________________________________
Notas
•	El formato de las facturas puede influir en la precisión de los datos extraídos.
•	Se recomienda utilizar facturas con una estructura consistente.
