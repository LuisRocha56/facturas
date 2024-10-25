import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
import pandas as pd
import logging

# Configuración de registro
logging.basicConfig(filename='procesamiento_facturas.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Variable global para almacenar archivos procesados y ruta del archivo Excel
archivos_procesados = set()
ruta_excel = ""

# Función para elegir la ubicación del archivo Excel
def elegir_guardar_excel():
    global ruta_excel
    ruta_excel = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if ruta_excel:
        label_ruta_excel.config(text=ruta_excel)

# Función para elegir archivos XML
def elegir_facturas():
    archivos = filedialog.askopenfilenames(title="Seleccionar archivos XML", filetypes=[("XML files", "*.xml")])
    if archivos:
        for archivo in archivos:
            if archivo not in archivos_procesados:  # Evitar duplicados
                lista_archivos.insert(tk.END, archivo)

# Función para procesar los archivos XML seleccionados y extraer datos
def procesar_facturas():
    global archivos_procesados
    if not ruta_excel:
        messagebox.showwarning("Advertencia", "Por favor, elija primero la ubicación para guardar el archivo Excel.")
        return

    if lista_archivos.size() == 0:
        messagebox.showwarning("Advertencia", "Por favor, elija archivos XML primero.")
        return

    # Cargar datos existentes si el archivo ya existe o crear nuevo DataFrame
    if os.path.exists(ruta_excel):
        df = pd.read_excel(ruta_excel)
    else:
        df = pd.DataFrame(columns=["Fecha", "Factura", "Nombre Proveedor", "RFC", "Sub Total", "IVA", "Total"])

    errores = []
    archivos_a_procesar = lista_archivos.get(0, tk.END)
    
    # Crear barra de progreso
    progress_bar['maximum'] = len(archivos_a_procesar)
    progress_bar['value'] = 0
    
    for archivo in archivos_a_procesar:
        try:
            tree = ET.parse(archivo)
            root = tree.getroot()

            # Función auxiliar para buscar diferentes variaciones de etiquetas/atributos
            def obtener_valor(root, opciones):
                for opcion in opciones:
                    elemento = root.find(opcion[0], namespaces=opcion[1] if len(opcion) > 1 else {})
                    if elemento is not None and elemento.get(opcion[2] if len(opcion) > 2 else ""):
                        return elemento.get(opcion[2] if len(opcion) > 2 else "")
                return "Desconocido"

            # Extraer los datos según la estructura del XML
            fecha = root.get("Fecha") or root.get("fecha") or root.get("fechaEmision")
            factura = root.get("Folio") or root.get("folio") or root.get("numero")

            # Buscar "Nombre Proveedor" y "RFC" en varias estructuras
            nombre_proveedor = obtener_valor(root, [
                (".//cfdi:Emisor", {"cfdi": "http://www.sat.gob.mx/cfd/4"}, "Nombre"),
                (".//Emisor", {}, "Nombre"),
                (".//proveedor", {}, "Nombre"),
                (".//nombreProveedor", {}, ""),
                (".//NombreProveedor", {}, ""),
                (".//razonSocial", {}, ""),
                (".//RazonSocial", {}, ""),
                (".//Nombre", {}, ""),
                (".//nombre", {}, "")
            ])
            rfc = obtener_valor(root, [
                (".//cfdi:Emisor", {"cfdi": "http://www.sat.gob.mx/cfd/4"}, "Rfc"),
                (".//Emisor", {}, "Rfc"),
                (".//proveedor", {}, "RFC"),
                (".//nombreProveedor", {}, "RFC"),
                (".//Rfc", {}, ""),
                (".//rfc", {}, "")
            ])

            subtotal = float(root.get("SubTotal") or root.get("subTotal") or 0)
            
            # Extracción del IVA
            iva = 0.0
            try:
                iva_element = root.find(".//cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado", namespaces={"cfdi": "http://www.sat.gob.mx/cfd/4"})
                if iva_element is not None:
                    iva = float(iva_element.get("Importe", 0))
            except Exception as e:
                logging.error(f"Error al extraer el IVA de {archivo}: {str(e)}")
                iva = 0.0  # Valor por defecto si hay un error
            
            total = float(root.get("Total") or root.get("total") or 0)

            nuevo_df = pd.DataFrame({
                "Fecha": [fecha],
                "Factura": [factura],
                "Nombre Proveedor": [nombre_proveedor],
                "RFC": [rfc],
                "Sub Total": [subtotal],
                "IVA": [iva],
                "Total": [total]
            })

            df = pd.concat([df, nuevo_df], ignore_index=True).drop_duplicates()
            archivos_procesados.add(archivo)

        except Exception as e:
            errores.append(f"Error procesando {archivo}: {str(e)}")
            logging.error(f"Error procesando {archivo}: {str(e)}")

        # Actualizar la barra de progreso
        progress_bar['value'] += 1

    # Añadir la columna "Suma de Totales"
    df["Suma de Totales"] = df["Total"].sum()

    # Ordenar el DataFrame por la columna "Fecha" de la más actual a la más antigua
    df = df.sort_values(by="Fecha", ascending=False)

    # Guardar los datos en el archivo Excel
    if not df.empty:
        try:
            df.to_excel(ruta_excel, index=False)
            messagebox.showinfo("Éxito", "Facturas procesadas y datos guardados en Excel.")
        except Exception as e:
            errores.append(f"Error al guardar el archivo Excel: {str(e)}")
            logging.error(f"Error al guardar el archivo Excel: {str(e)}")

    lista_archivos.delete(0, tk.END)

    # Mostrar errores si hubo problemas
    if errores:
        mensaje_errores = "\n".join(errores)
        messagebox.showwarning("Procesado con advertencias", f"Ocurrieron algunos errores:\n{mensaje_errores}")

# Función para mostrar la ayuda
def mostrar_ayuda():
    ayuda_texto = (
        "Manual de Usuario\n\n"
        "Este programa permite procesar archivos XML de facturas.\n\n"
        "1. Elegir Guardar Excel:\n"
        "   Seleccione la ubicación y nombre del archivo Excel donde se guardarán los datos.\n\n"
        "2. Elegir Facturas:\n"
        "   Seleccione uno o más archivos XML que desee procesar.\n\n"
        "3. Procesar Facturas:\n"
        "   Este botón procesará los archivos XML seleccionados y los datos se guardarán en el archivo Excel elegido.\n\n"
        "Notas:\n"
        "- Asegúrese de que los archivos XML estén en el formato correcto.\n"
        "- El programa generará un registro de errores en caso de problemas durante el procesamiento."
    )
    messagebox.showinfo("Ayuda", ayuda_texto)

# Configuración de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Procesador de Facturas XML")
ventana.geometry("600x500")

boton_guardar = tk.Button(ventana, text="Elegir Guardar Excel", command=elegir_guardar_excel)
boton_guardar.pack(pady=10)

boton_elegir = tk.Button(ventana, text="Elegir Facturas", command=elegir_facturas)
boton_elegir.pack(pady=10)

boton_procesar = tk.Button(ventana, text="Procesar Facturas", command=procesar_facturas)
boton_procesar.pack(pady=10)

boton_ayuda = tk.Button(ventana, text="Ayuda", command=mostrar_ayuda)
boton_ayuda.pack(pady=10)

label_ruta_excel = tk.Label(ventana, text="Ruta del archivo Excel no seleccionada")
label_ruta_excel.pack(pady=10)

lista_archivos = tk.Listbox(ventana, selectmode=tk.MULTIPLE)
lista_archivos.pack(pady=10, fill=tk.BOTH, expand=True)

# Barra de progreso
progress_bar = ttk.Progressbar(ventana, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

ventana.mainloop()

#hola