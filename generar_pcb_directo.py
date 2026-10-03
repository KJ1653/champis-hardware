import os

def generar_archivo_pcb_crudo():
    nombre_archivo = "ChampIS_v3_Layout.kicad_pcb"
    
    # Parámetros físicos (Placa 60x40mm)
    # Colocamos el origen local para que el centro exacto sea (30, 20)
    ancho = 60.0
    alto = 40.0
    
    # 1. Cabecera estructural nativa del formato KiCad PCB v2022/2024
    contenido = [
        f"(kicad_pcb (version 20211014) (generator python_raw_script)",
        f"  (general (thickness 1.6))",
        f"  (paper \"A4\")",
        f"  (layers",
        f"    (0 \"F.Cu\" signal)",
        f"    (31 \"B.Cu\" signal)",
        f"    (34 \"B.Paste\" user)",
        f"    (35 \"F.Paste\" user)",
        f"    (36 \"B.SilkS\" user)",
        f"    (37 \"F.SilkS\" user)",
        f"    (38 \"B.Mask\" user)",
        f"    (39 \"F.Mask\" user)",
        f"    (44 \"Edge.Cuts\" user)",
        f"  )",
        f"",
        f"  # ==========================================",
        f"  # DIBUJO DEL CONTORNO FÍSICO DE LA PLACA (60x40mm)",
        f"  # ==========================================",
        f"  (gr_line (start 0 0) (end {ancho} 0) (layer \"Edge.Cuts\") (width 0.15))",
        f"  (gr_line (start {ancho} 0) (end {ancho} {alto}) (layer \"Edge.Cuts\") (width 0.15))",
        f"  (gr_line (start {ancho} {alto}) (end 0 {alto}) (layer \"Edge.Cuts\") (width 0.15))",
        f"  (gr_line (start 0 {alto}) (end 0 0) (layer \"Edge.Cuts\") (width 0.15))",
        f"",
        f"  # ==========================================",
        f"  # ANCLAJES MECÁNICOS Y MARCAS DE POSICIÓN CENTRAL",
        f"  # Heltec V3 y MT3608 comparten el centro geométrico (30, 20)",
        f"  # ==========================================",
    ]
    
    # Posición central de control
    cx, cy = 30.0, 20.0
    
    # Simular pines de la Heltec V3 (2 filas de 18 pines espaciados a 2.54mm)
    # Distancia entre las dos filas (ancho del riel): 22.86mm (0.9 pulgadas estándar)
    distancia_rieles = 22.86
    x_riel_izq = cx - (distancia_rieles / 2.0)
    x_riel_der = cx + (distancia_rieles / 2.0)
    
    contenido.append(f"  # Riel Izquierdo Heltec V3 (F.Cu)")
    for i in range(18):
        y_pin = cy - (17 * 2.54 / 2.0) + (i * 2.54)
        contenido.append(f"  (pad \"H_L{i+1}\" thru_hole circle (at {x_riel_izq:.4f} {y_pin:.4f}) (size 1.7 1.7) (drill 1.0) (layers *.Cu *.Mask))")
        
    contenido.append(f"  # Riel Derecho Heltec V3 (F.Cu)")
    for i in range(18):
        y_pin = cy - (17 * 2.54 / 2.0) + (i * 2.54)
        contenido.append(f"  (pad \"H_R{i+1}\" thru_hole circle (at {x_riel_der:.4f} {y_pin:.4f}) (size 1.7 1.7) (drill 1.0) (layers *.Cu *.Mask))")

    # Posicionar el MT3608 exactamente en el medio de ambos rieles en la capa inferior (B.SilkS/B.Cu)
    # Su espacio interno libre queda perfectamente protegido aquí
    contenido.extend([
        f"  # Ubicación física reservada para el MT3608 (Capa de abajo)",
        f"  (gr_text \"MT3608 UNDER\" (at {cx:.4f} {cy:.4f}) (layer \"B.SilkS\")",
        f"    (effects (font (size 1 1) (thickness 0.15)) (justify mirror))",
        f"  )",
        f"  (gr_rect (start {cx-8:.2f} {cy-10:.2f}) (end {cx+8:.2f} {cy+10:.2f}) (layer \"B.SilkS\") (width 0.12))",
        f")"
    ])
    
    # Escribir el archivo final
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("\n".join(contenido))
        
    print("\n" + "="*50)
    print(f"🎉 ¡SUCCESS! Archivo de hardware puro generado directamente:")
    print(f"➡️ {os.path.abspath(nombre_archivo)}")
    print("="*50)

if __name__ == "__main__":
    generar_archivo_pcb_crudo()
