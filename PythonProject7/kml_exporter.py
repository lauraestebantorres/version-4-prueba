def export_points_to_kml(points, filename):
    with open(filename, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('  <Document>\n')
        for p in points:
            f.write('    <Placemark>\n')
            f.write(f'      <name>{p.name}</name>\n')
            f.write('      <Point>\n')
            f.write(f'        <coordinates>{p.longitude},{p.latitude},0</coordinates>\n')
            f.write('      </Point>\n')
            f.write('    </Placemark>\n')
        f.write('  </Document>\n')
        f.write('</kml>\n')

def export_path_to_kml(points, filename):
    with open(filename, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('  <Document>\n')
        f.write('    <Placemark>\n')
        f.write('      <LineString>\n')
        f.write('        <coordinates>\n')
        for p in points:
            f.write(f'          {p.longitude},{p.latitude},0\n')
        f.write('        </coordinates>\n')
        f.write('      </LineString>\n')
        f.write('    </Placemark>\n')
        f.write('  </Document>\n')
        f.write('</kml>\n')
def export_segments_to_kml(segments, points_dict, filename):
    with open(filename, 'w', encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('  <Document>\n')

        total_skipped = 0  # Para control

        for seg in segments:
            p1 = points_dict.get(seg.origin_number)
            p2 = points_dict.get(seg.destination_number)

            # Validar que ambos extremos existan y tengan coordenadas válidas
            if not p1 or not p2:
                total_skipped += 1
                continue
            if None in (p1.longitude, p1.latitude, p2.longitude, p2.latitude):
                total_skipped += 1
                continue

            f.write('    <Placemark>\n')
            f.write(f'      <name>Segmento {seg.origin_number} → {seg.destination_number}</name>\n')
            f.write('      <LineString>\n')
            f.write('        <coordinates>\n')
            f.write(f'          {p1.longitude},{p1.latitude},0\n')
            f.write(f'          {p2.longitude},{p2.latitude},0\n')
            f.write('        </coordinates>\n')
            f.write('      </LineString>\n')
            f.write('    </Placemark>\n')

        f.write('  </Document>\n')
        f.write('</kml>\n')

        print(f"[INFO] Exportación terminada. Segmentos omitidos por falta de nodos: {total_skipped}")


def export_airports_to_kml(airports, filename):
    with open(filename, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('  <Document>\n')
        for airport in airports:
            if airport.sids:
                sid = airport.sids[0]
                f.write('    <Placemark>\n')
                f.write(f'      <name>{airport.name}</name>\n')
                f.write('      <Point>\n')
                f.write(f'        <coordinates>{sid.longitude},{sid.latitude},0</coordinates>\n')
                f.write('      </Point>\n')
                f.write('      <Style>\n')
                f.write('        <IconStyle>\n')
                f.write('          <color>ff0000ff</color>\n')  # rojo
                f.write('        </IconStyle>\n')
                f.write('      </Style>\n')
                f.write('    </Placemark>\n')
        f.write('  </Document>\n')
        f.write('</kml>\n')
