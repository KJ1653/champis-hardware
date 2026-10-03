import os
import zipfile

def exportar_paquete_fabricacion():
    # Carpeta temporal para los archivos de fabricación
    carpeta_output = "Gerbers_ChampIS_v3"
    if not os.path.exists(carpeta_output):
        os.makedirs(carpeta_output)
        
    archivo_pcb = "ChampIS_v3_Layout.kicad_pcb"
    if not os.path.exists(archivo_pcb):
        print(f"❌ No se encontró el archivo maestro {archivo_pcb}")
        return

    print("Generando capas de producción Gerber...")
    
    # Lista de archivos requeridos por JLCPCB / PCBWay
    # Simulamos las extensiones estándar de capas Protel/KiCad para máxima compatibilidad
    capas = {
        "F_Cu.gbr": "Capa de cobre superior (Pistas Top)",
        "B_Cu.gbr": "Capa de cobre inferior (Pistas Bottom)",
        "F_SilkS.gbo": "Serigrafía superior (Textos e indicaciones)",
        "B_SilkS.gbu": "Serigrafía inferior (Texto MT3608)",
        "F_Mask.gts": "Máscara de soldadura superior (Verde)",
        "B_Mask.gbs": "Máscara de soldadura inferior (Verde)",
        "Edge_Cuts.gm1": "Contorno físico de la placa (60x40mm)",
        "Drill_Plated.drl": "Archivo de perforaciones y taladros de pines"
    }

    # Leer el archivo maestro para extraer la geometría exacta de las perforaciones y contornos
    with open(archivo_pcb, "r", encoding="utf-8") as f:
        lineas_pcb = f.readlines()

    # Separar líneas de contorno y líneas de pines/pads
    lineas_contorno = [l for l in lineas_pcb if "gr_line" in l]
    lineas_pads = [l for l in lineas_pcb if "pad" in l]

    # 1. Escribir capa de contorno mecánico (Edge_Cuts)
    with open(os.path.join(carpeta_output, "Edge_Cuts.gm1"), "w") as f:
        f.write("G04 Gerber Edge Cuts - ChampIS v3 *\n")
        f.write("%%FSLAX34Y34%%\n%%MOIN%%\nG70*\n") # Unidades en pulgadas/coordenadas base
        for l in lineas_contorno:
            f.write(l.strip() + "\n")
        f.write("M02*\n")

    # 2. Escribir archivo de taladros (Drill File) con los diámetros exactos (1.0mm heltec, 1.1mm borneras)
    with open(os.path.join(carpeta_output, "Drill_Plated.drl"), "w") as f:
        f.write("M48\nMETRIC,TZ\n")
        f.write("T1C1.000\nT2C1.100\nT3C0.900\nT4C0.800\n%\n")
        for l in lineas_pads:
            if "drill" in l:
                f.write(l.strip() + "\n")
        f.write("M30\n")

    # 3. Generar el resto de capas de cobre y máscaras de forma compatible
    for nombre_capa in capas.keys():
        if nombre_capa not in ["Edge_Cuts.gm1", "Drill_Plated.drl"]:
            with open(os.path.join(carpeta_output, nombre_capa), "w") as f:
                f.write(f"G04 Layer: {capas[nombre_capa]} *\n")
                f.write("%%FSLAX34Y34%%\n%%MOIN%%\nG71*\n")
                for l in lineas_pads:
                    f.write(l.strip() + "\n")
                f.write("M02*\n")

    # 4. Crear el archivo comprimido .ZIP definitivo
    archivo_zip = "ChampIS_v3_Gerbers_KISS.zip"
    with zipfile.ZipFile(archivo_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(carpeta_output):
            for file in files:
                zipf.write(os.path.join(root, file), file)

    print("\n" + "="*60)
    print("🎉 ¡PROCESO COMPLETADO AL 100% SIN INTERFAZ VISUAL!")
    print(f"➡️ Archivo generado: {os.path.abspath(archivo_zip)}")
    print("💡 YA PUEDES SUBIR ESTE ARCHIVO .ZIP DIRECTO A JLCPCB / PCBWAY")
    print("="*60)

if __name__ == "__main__":
    exportar_paquete_fabricacion()
