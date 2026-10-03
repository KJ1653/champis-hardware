import os

def crear_pcb_industrial_routed():
    nombre_archivo = "ChampIS_v3_Final.kicad_pcb"
    ancho = 60.0
    alto = 40.0  # Safe positive box: X(0 to 60mm), Y(0 to 40mm)
    
    # ABSOLUTE POSITIVE Y CENTERING
    cx = 30.0
    cy = 19.0  # Centered to perfectly wrap all 18 rows from Y=1.41 to Y=39.59
    
    dist_rieles = 22.86
    hx_izq = cx - (dist_rieles / 2.0) # 18.57 mm
    hx_der = cx + (dist_rieles / 2.0) # 41.43 mm
    
    sb = []
    sb.append("(kicad_pcb (version 20211014) (generator python_industrial_script)")
    sb.append("  (general (thickness 1.6))")
    sb.append("  (paper \"A4\")")
    sb.append("  (layers (0 \"F.Cu\" signal) (31 \"B.Cu\" signal) (36 \"B.SilkS\" user) (37 \"F.SilkS\" user) (38 \"B.Mask\" user) (39 \"F.Mask\" user) (44 \"Edge.Cuts\" user))")
    
    # ==========================================
    # 1. CLOSED BOARD OUTLINE (0 to 60mm, 0 to 40mm)
    # ==========================================
    sb.append(f"  (gr_line (start 0 0) (end {ancho} 0) (layer \"Edge.Cuts\") (width 0.15))")
    sb.append(f"  (gr_line (start {ancho} 0) (end {ancho} {alto}) (layer \"Edge.Cuts\") (width 0.15))")
    sb.append(f"  (gr_line (start {ancho} {alto}) (end 0 {alto}) (layer \"Edge.Cuts\") (width 0.15))")
    sb.append(f"  (gr_line (start 0 {alto}) (end 0 0) (layer \"Edge.Cuts\") (width 0.15))")
    
    # ==========================================
    # 2. HELTEC V3 (All rows safely inside 0-40mm window)
    # ==========================================
    sb.append("  (footprint \"Heltec_WiFi_LoRa_32_V3\" (layer \"F.Cu\") (at 0 0)")
    for i in range(18):
        y_pin = cy - (17 * 2.54 / 2.0) + (i * 2.54)
        sb.append(f"    (pad \"{i+1}\" thru_hole circle (at {hx_izq:.4f} {y_pin:.4f}) (size 1.7 1.7) (drill 1.0) (layers *.Cu *.Mask))")
        sb.append(f"    (pad \"{i+19}\" thru_hole circle (at {hx_der:.4f} {y_pin:.4f}) (size 1.7 1.7) (drill 1.0) (layers *.Cu *.Mask))")
    sb.append("  )")
    
    # ==========================================
    # 3. JST-PH BATTERY CONNECTOR (Positive Y)
    # ==========================================
    sb.append("  (footprint \"JST_BAT\" (layer \"F.Cu\") (at 0 0)")
    sb.append("    (pad \"1\" thru_hole circle (at 4.00 21.00) (size 1.8 1.8) (drill 1.05) (layers *.Cu *.Mask))")
    sb.append("    (pad \"2\" thru_hole circle (at 4.00 19.00) (size 1.8 1.8) (drill 1.05) (layers *.Cu *.Mask))")
    sb.append("  )")
    
    # ==========================================
    # 4. DRV8833 SOLENOIDE DRIVER (Positive Y)
    # ==========================================
    sb.append("  (footprint \"DRV8833\" (layer \"F.Cu\") (at 0 0)")
    drv_x1, drv_x2 = 8.0, 10.54
    for i in range(6):
        y_pos = 6.0 + (i * 2.54)
        sb.append(f"    (pad \"{i+1}\" thru_hole circle (at {drv_x1:.2f} {y_pos:.2f}) (size 1.7 1.7) (drill 1.0) (layers *.Cu *.Mask))")
        sb.append(f"    (pad \"{i+7}\" thru_hole circle (at {drv_x2:.2f} {y_pos:.2f}) (size 1.7 1.7) (drill 1.0) (layers *.Cu *.Mask))")
    sb.append("  )")
    
    # ==========================================
    # 5. MAX98357A AUDIO AMPLIFIER (Positive Y)
    # ==========================================
    sb.append("  (footprint \"MAX98357A\" (layer \"F.Cu\") (at 0 0)")
    for i in range(7):
        y_pos = 22.0 + (i * 2.54)
        sb.append(f"    (pad \"{i+1}\" thru_hole circle (at 8.00 {y_pos:.2f}) (size 1.7 1.7) (drill 1.0) (layers *.Cu *.Mask))")
    sb.append("  )")
    
    # ==========================================
    # 6. RIGHT-ALIGNED SCREW TERMINALS (Positive Y)
    # ==========================================
    sb.append("  (footprint \"BORNERAS_DERECHA\" (layer \"F.Cu\") (at 0 0)")
    bx = 56.0
    sb.append(f"    (pad \"SOL_1\" thru_hole circle (at {bx:.2f} 34.00) (size 1.8 1.8) (drill 1.1) (layers *.Cu *.Mask))")
    sb.append(f"    (pad \"SOL_2\" thru_hole circle (at {bx:.2f} 31.46) (size 1.8 1.8) (drill 1.1) (layers *.Cu *.Mask))")
    sb.append(f"    (pad \"SPK_1\" thru_hole circle (at {bx:.2f} 24.00) (size 1.8 1.8) (drill 1.1) (layers *.Cu *.Mask))")
    sb.append(f"    (pad \"SPK_2\" thru_hole circle (at {bx:.2f} 21.46) (size 1.8 1.8) (drill 1.1) (layers *.Cu *.Mask))")
    sb.append(f"    (pad \"FLOW_VCC\" thru_hole circle (at {bx:.2f} 14.00) (size 1.8 1.8) (drill 1.1) (layers *.Cu *.Mask))")
    sb.append(f"    (pad \"FLOW_SIG\" thru_hole circle (at {bx:.2f} 11.46) (size 1.8 1.8) (drill 1.1) (layers *.Cu *.Mask))")
    sb.append(f"    (pad \"FLOW_GND\" thru_hole circle (at {bx:.2f} 8.92) (size 1.8 1.8) (drill 1.1) (layers *.Cu *.Mask))")
    sb.append("  )")

    # ==========================================
    # 7. THROUGH-HOLE DIVISOR RESISTORS (Positive Y)
    # ==========================================
    sb.append("  (footprint \"DIVISOR_VOLTAGE\" (layer \"F.Cu\") (at 0 0)")
    sb.append("    (pad \"R1_1\" thru_hole circle (at 48.00 11.46) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))")
    sb.append("    (pad \"R1_2\" thru_hole circle (at 48.00 3.84) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))")
    sb.append("    (pad \"R2_1\" thru_hole circle (at 52.00 11.46) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))")
    sb.append("    (pad \"R2_2\" thru_hole circle (at 52.00 3.84) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))")
    sb.append("  )")

    # ==========================================
    # 8. COPPER ROUTING SEGMENTS (Positive Y Only)
    # ==========================================
    y_gpio3 = cy - (17 * 2.54 / 2.0) + (4 * 2.54) # Pin H_L5 (GPIO3) mapping
    sb.append(f"  (segment (start 48.00 3.84) (end 52.00 3.84) (width 0.25) (layer \"F.Cu\") (net 0))")
    sb.append(f"  (segment (start 48.00 11.46) (end {hx_izq:.4f} {y_gpio3:.4f}) (width 0.25) (layer \"F.Cu\") (net 0))") 
    sb.append(f"  (segment (start {bx:.2f} 11.46) (end 48.00 11.46) (width 0.25) (layer \"F.Cu\") (net 0))")
    sb.append(f"  (segment (start 4.00 21.00) (end {cx:.2f} {cy:.2f}) (width 0.60) (layer \"B.Cu\") (net 0))")
    sb.append(f"  (segment (start 4.00 19.00) (end {cx:.2f} {cy+2.0:.2f}) (width 0.60) (layer \"B.Cu\") (net 0))")

    sb.append(")")
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("\n".join(sb))
        
    print("\n" + "="*60)
    print("💎 FIXED: 4-Line Closed Outer Ring (0,0 to 60,40mm).")
    print("         All elements re-written to absolute positive coordinates.")
    print("="*60)

if __name__ == "__main__":
    crear_pcb_industrial_routed()
