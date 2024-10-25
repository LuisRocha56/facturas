import os
import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
import pandas as pd

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

    if os.path.exists(ruta_excel):
        df = pd.read_excel(ruta_excel)
    else:
        df = pd.DataFrame(columns=["Fecha", "Factura", "Nombre Proveedor", "RFC", "Sub Total", "IVA", "Total"])

    errores = []
    archivos_a_procesar = lista_archivos.get(0, tk.END)
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
            iva_element = root.find(".//cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado", namespaces={"cfdi": "http://www.sat.gob.mx/cfd/4"})
            iva = float(iva_element.get("Importe") if iva_element is not None else 0)
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

    # Guardar los datos en el archivo Excel
    if not df.empty:
        try:
            df.to_excel(ruta_excel, index=False)
            messagebox.showinfo("Éxito", "Facturas procesadas y datos guardados en Excel.")
        except Exception as e:
            errores.append(f"Error al guardar el archivo Excel: {str(e)}")

    lista_archivos.delete(0, tk.END)

    # Mostrar errores si hubo problemas
    if errores:
        mensaje_errores = "\n".join(errores)
        messagebox.showwarning("Procesado con advertencias", f"Ocurrieron algunos errores:\n{mensaje_errores}")

# Configuración de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Procesador de Facturas XML")
ventana.geometry("600x400")

boton_guardar = tk.Button(ventana, text="Elegir Guardar Excel", command=elegir_guardar_excel)
boton_guardar.pack(pady=10)

boton_elegir = tk.Button(ventana, text="Elegir Facturas", command=elegir_facturas)
boton_elegir.pack(pady=10)

boton_procesar = tk.Button(ventana, text="Procesar Facturas", command=procesar_facturas)
boton_procesar.pack(pady=10)

label_ruta_excel = tk.Label(ventana, text="Ruta del archivo Excel no seleccionada")
label_ruta_excel.pack(pady=10)

lista_archivos = tk.Listbox(ventana, selectmode=tk.MULTIPLE)
lista_archivos.pack(pady=10)

ventana.mainloop()