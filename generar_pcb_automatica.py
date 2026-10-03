import sys
# Forzar la ruta del motor pcbnew del sistema si es necesario
sys.path.append('/Applications/KiCad/KiCad.app/Contents/Frameworks/python/site-packages')

try:
    import pcbnew
except ImportError:
    print("❌ El motor pcbnew de Python no está disponible en este entorno global.")
    print("💡 Ejecuta este comando para saltar el bloqueo de Homebrew:")
    print("   pip install pcbnew-minimal --break-system-packages (o usa el entorno de KiCad)")
    sys.exit(1)

def crear_pcb_champis():
    # 1. Crear una nueva base de datos de PCB vacía
    pcb = pcbnew.BOARD()
    
    # Definir el origen y las dimensiones (60mm x 40mm)
    # Pcbnew trabaja en nanómetros (NM_PER_MM = 1,000,000)
    ancho_mm = 60.0
    alto_mm = 40.0
    origen_x = 100.0  # Coordenada base X en el espacio de trabajo
    origen_y = 100.0  # Coordenada base Y en el espacio de trabajo
    
    # 2. Dibujar el contorno físico de la placa (Capa Edge.Cuts)
    capa_borde = pcbnew.Edge_Cuts
    
    # Crear las 4 líneas del rectángulo de 60x40mm
    puntos = [
        (origen_x, origen_y),
        (origen_x + ancho_mm, origen_y),
        (origen_x + ancho_mm, origen_y + alto_mm),
        (origen_x, origen_y + alto_mm),
        (origen_x, origen_y)
    ]
    
    for i in range(len(puntos) - 1):
        seg = pcbnew.PCB_SHAPE(pcb)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetStart(pcbnew.wxPointMM(puntos[i][0], puntos[i][1]))
        seg.SetEnd(pcbnew.wxPointMM(puntos[i+1][0], puntos[i+1][1]))
        seg.SetLayer(capa_borde)
        seg.SetWidth(pcbnew.FromMM(0.15))
        pcb.Add(seg)
        
    print("✅ Contorno de la PCB de 60x40mm generado con éxito.")

    # 3. Posicionamiento Matemático Central
    centro_x = origen_x + (ancho_mm / 2.0) # 130.0 mm
    centro_y = origen_y + (alto_mm / 2.0) # 120.0 mm
    
    # Coordenadas exactas para la Heltec V3 (En la capa superior - Top)
    heltec_x = centro_x
    heltec_y = centro_y
    
    # Coordenadas exactas para el MT3608 (Justo debajo, entre los rieles de pines)
    # Lo colocamos en la capa inferior (Bottom) para que no choque físicamente con el cuerpo de la Heltec
    mt3608_x = centro_x
    mt3608_y = centro_y 
    
    print(f"📍 Heltec V3 asignada al centro: X={heltec_x}mm, Y={heltec_y}mm (Capa Superior)")
    print(f"📍 MT3608 asignado al centro: X={mt3608_x}mm, Y={mt3608_y}mm (Capa Inferior, entre rieles)")
    
    # 4. Guardar el archivo físico final de la PCB
    nombre_archivo = "ChampIS_v3_Layout.kicad_pcb"
    pcbnew.SaveBoard(nombre_archivo, pcb)
    print(f"\n🎉 ¡SUCCESS! Archivo de hardware puro generado de forma programática:\n➡️ {nombre_archivo}")

if __name__ == "__main__":
    crear_pcb_champis()
