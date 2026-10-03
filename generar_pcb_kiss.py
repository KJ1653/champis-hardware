import os

def generar_pcb_final_kiss():
    nombre_archivo = "ChampIS_v3_Layout.kicad_pcb"
    
    # Dimensiones estrictas de la placa (60x40mm)
    ancho = 60.0
    alto = 40.0
    
    # Origen geométrico central
    cx, cy = 30.0, 20.0
    
    contenido = [
        "(kicad_pcb (version 20211014) (generator python_kiss_script)",
        "  (general (thickness 1.6))",
        "  (paper \"A4\")",
        "  (layers",
        "    (0 \"F.Cu\" signal)",
        "    (31 \"B.Cu\" signal)",
        "    (34 \"B.Paste\" user)",
        "    (35 \"F.Paste\" user)",
        "    (36 \"B.SilkS\" user)",
        "    (37 \"F.SilkS\" user)",
        "    (38 \"B.Mask\" user)",
        "    (39 \"F.Mask\" user)",
        "    (44 \"Edge.Cuts\" user)",
        "  )",
        "",
        "  # ==========================================",
        "  # 1. CONTORNO FÍSICO DE LA PLACA (60x40mm)",
        "  # ==========================================",
        f"  (gr_line (start 0 0) (end {ancho} 0) (layer \"Edge.Cuts\") (width 0.15))",
        f"  (gr_line (start {ancho} 0) (end {ancho} {alto}) (layer \"Edge.Cuts\") (width 0.15))",
        f"  (gr_line (start {ancho} {alto}) (end 0 {alto}) (layer \"Edge.Cuts\") (width 0.15))",
        f"  (gr_line (start 0 {alto}) (end 0 0) (layer \"Edge.Cuts\") (width 0.15))",
        "",
        "  # ==========================================",
        "  # 2. HELTEC WIFI LORA 32 V3 (CENTRO TOP)",
        "  # ==========================================",
    ]
    
    # Rieles de la Heltec V3 (Ancho estándar de 22.86mm entre filas)
    dist_rieles = 22.86
    x_heltec_izq = cx - (dist_rieles / 2.0)  # 18.57 mm
    x_heltec_der = cx + (dist_rieles / 2.0)  # 41.43 mm
    
    # Generar los 18 pines del lado izquierdo (GPIOs, 3V3, GND)
    for i in range(18):
        y_pin = cy - (17 * 2.54 / 2.0) + (i * 2.54)
        contenido.append(f"  (pad \"H_L{i+1}\" thru_hole circle (at {x_heltec_izq:.4f} {y_pin:.4f}) (size 1.7 1.7) (drill 1.0) (layers *.Cu *.Mask))")
        
    # Generar los 18 pines del lado derecho (5V, Ve, GPIOs)
    for i in range(18):
        y_pin = cy - (17 * 2.54 / 2.0) + (i * 2.54)
        contenido.append(f"  (pad \"H_R{i+1}\" thru_hole circle (at {x_heltec_der:.4f} {y_pin:.4f}) (size 1.7 1.7) (drill 1.0) (layers *.Cu *.Mask))")

    # ==========================================
    # 3. ZONA DE RESERVA MT3608 (CENTRO BOTTOM)
    # ==========================================
    contenido.extend([
        "  # Espacio seguro para el MT3608 debajo de la Heltec",
        f"  (gr_rect (start {cx-8:.2f} {cy-11:.2f}) (end {cx+8:.2f} {cy+11:.2f}) (layer \"B.SilkS\") (width 0.12))",
        f"  (gr_text \"MT3608 HW-045 UNDER\" (at {cx:.4f} {cy:.4f}) (layer \"B.SilkS\") (effects (font (size 1 1) (thickness 0.15)) (justify mirror)))",
        "",
        "  # ==========================================",
        "  # 4. COMPACTO & KISS: BORNERAS EN EL BORDE DERECHO (Pitch 2.54mm)",
        "  # Alineadas a X = 55.0mm para salida directa a las glándulas",
        "  # ==========================================",
    ])
    
    x_borneras = 56.0
    
    # Bornera Solenoide (2 Pines) - Superior Derecho
    contenido.append("  # Terminal Solenoide (2 pines)")
    contenido.append(f"  (pad \"SOL_1\" thru_hole circle (at {x_borneras:.2f} 32.00) (size 1.8 1.8) (drill 1.1) (layers *.Cu *.Mask))")
    contenido.append(f"  (pad \"SOL_2\" thru_hole circle (at {x_borneras:.2f} 29.46) (size 1.8 1.8) (drill 1.1) (layers *.Cu *.Mask))")
    
    # Bornera Speaker (2 Pines) - Medio Derecho
    contenido.append("  # Terminal Bocina (2 pines)")
    contenido.append(f"  (pad \"SPK_1\" thru_hole circle (at {x_borneras:.2f} 23.00) (size 1.8 1.8) (drill 1.1) (layers *.Cu *.Mask))")
    contenido.append(f"  (pad \"SPK_2\" thru_hole circle (at {x_borneras:.2f} 20.46) (size 1.8 1.8) (drill 1.1) (layers *.Cu *.Mask))")
    
    # Bornera Sensor de Flujo YF-S201 (3 Pines) - Inferior Derecho
    contenido.append("  # Terminal Sensor de Flujo (3 pines: 5V, SIG, GND)")
    contenido.append(f"  (pad \"FLOW_VCC\" thru_hole circle (at {x_borneras:.2f} 14.00) (size 1.8 1.8) (drill 1.1) (layers *.Cu *.Mask))")
    contenido.append(f"  (pad \"FLOW_SIG\" thru_hole circle (at {x_borneras:.2f} 11.46) (size 1.8 1.8) (drill 1.1) (layers *.Cu *.Mask))")
    contenido.append(f"  (pad \"FLOW_GND\" thru_hole circle (at {x_borneras:.2f} 8.92) (size 1.8 1.8) (drill 1.1) (layers *.Cu *.Mask))")

    # ==========================================
    # 5. CONECTOR JST DE BATERÍA 18650 (BORDE IZQUIERDO)
    # ==========================================
    contenido.extend([
        "  # Entrada de Batería JST PH 2.0mm (Lado Izquierdo)",
        "  (pad \"BAT_POS\" thru_hole circle (at 4.00 21.00) (size 1.6 1.6) (drill 0.9) (layers *.Cu *.Mask))",
        "  (pad \"BAT_NEG\" thru_hole circle (at 4.00 19.00) (size 1.6 1.6) (drill 0.9) (layers *.Cu *.Mask))",
        "",
        "  # ==========================================",
        "  # 6. DIVISOR DE VOLTAJE (R1/R2 THROUGH-HOLE) - PROTECCIÓN GPIO3",
        "  # Posicionado estratégicamente cerca de la bornera de flujo e inspección",
        "  # ==========================================",
        "  # Resistencia R1 (10k) - Distancia estándar entre patas: 7.62mm (0.3 pulgadas)",
        "  (pad \"R1_1\" thru_hole circle (at 48.00 11.46) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))",
        "  (pad \"R1_2\" thru_hole circle (at 48.00 3.84) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))",
        "",
        "  # Resistencia R2 (20k)",
        "  (pad \"R2_1\" thru_hole circle (at 52.00 11.46) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))",
        "  (pad \"R2_2\" thru_hole circle (at 52.00 3.84) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))",
        ")"
    ])
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("\n".join(contenido))
        
    print("\n" + "="*60)
    print("🚀 ¡PCB DISEÑADA BAJO CONCEPTO KISS!")
    print(f"Archivo generado: {os.path.abspath(nombre_archivo)}")
    print("Distribución: Heltec y MT3608 al centro. Borneras agrupadas a la derecha.")
    print("="*60)

if __name__ == "__main__":
    generar_pcb_final_kiss()
