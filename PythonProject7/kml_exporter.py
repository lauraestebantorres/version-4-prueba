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
def export_flight_animation_to_kml(points, filename):
   from datetime import datetime, timedelta


   start_time = datetime(2025, 1, 1, 12, 0, 0)  # hora inicial ficticia
   time_step = timedelta(seconds=3)  # tiempo entre puntos


   with open(filename, 'w', encoding='utf-8') as f:
       f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
       f.write('<kml xmlns="http://www.opengis.net/kml/2.2"\n')
       f.write('     xmlns:gx="http://www.google.com/kml/ext/2.2">\n')
       f.write('  <Document>\n')
       f.write('    <name>Animación de vuelo</name>\n')


       # Estilo con icono de avión grande
       f.write('    <Style id="planeStyle">\n')
       f.write('      <IconStyle>\n')
       f.write('        <scale>2.0</scale>\n')  # tamaño grande
       f.write('        <Icon>\n')
       f.write('          <href>http://maps.google.com/mapfiles/kml/shapes/airports.png</href>\n')
       f.write('        </Icon>\n')
       f.write('      </IconStyle>\n')
       f.write('    </Style>\n')


       # Animación de cámara que sigue al avión
       f.write('    <gx:Tour>\n')
       f.write('      <name>Seguimiento de cámara</name>\n')
       f.write('      <gx:Playlist>\n')
       # Mensajes automáticos en momentos clave
       f.write('        <gx:AnimatedUpdate>\n')
       f.write('          <gx:duration>3.0</gx:duration>\n')
       f.write('          <Update>\n')
       f.write('            <targetHref/>\n')
       f.write('            <Change>\n')
       f.write('              <Placemark>\n')
       f.write('                <description><![CDATA[🚀 Despegando de Barcelona...]]></description>\n')
       f.write('              </Placemark>\n')
       f.write('            </Change>\n')
       f.write('          </Update>\n')
       f.write('        </gx:AnimatedUpdate>\n')

       f.write('        <gx:Wait>\n')
       f.write('          <gx:duration>5.0</gx:duration>\n')
       f.write('        </gx:Wait>\n')

       for i, point in enumerate(points):
           when = start_time + i * time_step
           f.write('        <gx:FlyTo>\n')
           f.write('          <gx:duration>1.5</gx:duration>\n')
           f.write('          <gx:flyToMode>smooth</gx:flyToMode>\n')
           f.write('          <LookAt>\n')
           f.write(f'            <longitude>{point.longitude}</longitude>\n')
           f.write(f'            <latitude>{point.latitude}</latitude>\n')
           f.write('            <altitude>0</altitude>\n')
           f.write('            <heading>0</heading>\n')
           f.write('            <tilt>70</tilt>\n')
           f.write('            <range>50000</range>\n')
           f.write('            <altitudeMode>relativeToGround</altitudeMode>\n')
           f.write('          </LookAt>\n')
           f.write('        </gx:FlyTo>\n')


       f.write('      </gx:Playlist>\n')
       f.write('    </gx:Tour>\n')




       f.write('    <Placemark>\n')
       f.write('      <name>Vuelo animado</name>\n')
       f.write('      <styleUrl>#planeStyle</styleUrl>\n')  # aplica el estilo del avión
       f.write('      <gx:Track>\n')
       f.write('        <altitudeMode>clampToGround</altitudeMode>\n')


       for i, point in enumerate(points):
           when = start_time + i * time_step
           f.write(f'        <when>{when.isoformat()}Z</when>\n')


       for point in points:
           f.write(f'        <gx:coord>{point.longitude} {point.latitude} 0</gx:coord>\n')


       f.write('      </gx:Track>\n')
       f.write('    </Placemark>\n')


       f.write('  </Document>\n')
       f.write('</kml>\n')


