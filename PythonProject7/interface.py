import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from airSpace import AirSpace
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from math import sqrt
from collections import deque
from queue import PriorityQueue
from kml_exporter import export_points_to_kml
from tkinter import filedialog
import subprocess  # Agregado para la función open_in_google_earth
from kml_exporter import (
   export_points_to_kml,
   export_path_to_kml,
   export_segments_to_kml,
   export_airports_to_kml,
)




class AirSpaceGUI:
   def __init__(self, master):
       self.master = master
       self.master.title("Visualizador de Espacio Aéreo")
       self.airspace = AirSpace()


       # SOLUCIÓN: Definimos el color de los aeropuertos
       self.airport_color = 'red'  # O cualquier color que prefieras


       self.figure, self.ax = plt.subplots(figsize=(8, 6))
       self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
       self.toolbar = NavigationToolbar2Tk(self.canvas, self.master)
       self.toolbar.update()
       self.toolbar.grid(row=6, column=0, columnspan=4)
       self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=4)
       self.canvas.draw()
       self.canvas.mpl_connect('button_press_event', self.on_click)


       ttk.Label(master, text="Zona de vuelo:").grid(row=0, column=0, padx=5, pady=5)
       self.dataset_selector = ttk.Combobox(master, values=["Catalunya", "España", "Europa"], state="readonly")
       self.dataset_selector.grid(row=0, column=1, padx=5, pady=5)
       self.dataset_selector.current(0)
       ttk.Button(master, text="Cargar espacio aéreo", command=self.load_selected_data).grid(row=0, column=2, padx=5,
                                                                                             pady=5)


       ttk.Label(master, text="Nombre del punto:").grid(row=1, column=0, sticky="e")
       self.point_entry = ttk.Entry(master)
       self.point_entry.grid(row=1, column=1, sticky="w")
       ttk.Button(master, text="Mostrar vecinos", command=self.plot_neighbors).grid(row=3, column=2, padx=5, pady=5)


       ttk.Label(master, text="Origen:").grid(row=3, column=0, sticky="e")
       self.origin_entry = ttk.Entry(master)
       self.origin_entry.grid(row=3, column=1, sticky="w")
       ttk.Label(master, text="Destino:").grid(row=4, column=0, sticky="e")
       self.dest_entry = ttk.Entry(master)
       self.dest_entry.grid(row=4, column=1, sticky="w")
       ttk.Button(master, text="Camino más corto", command=self.plot_shortest_path).grid(row=4, column=2, padx=5,
                                                                                         pady=5)


       ttk.Button(master, text="Puntos Alcanzables", command=self.show_reachable_points).grid(row=1, column=2, padx=5,
                                                                                              pady=5)
       ttk.Button(master, text="Exportar NavPoints a KML", command=self.export_all_navpoints_to_kml).grid(row=1,
                                                                                                          column=3,
                                                                                                          padx=5,
                                                                                                          pady=5)
       ttk.Button(master, text="Exportar Ruta a KML", command=self.export_last_path_to_kml).grid(row=5, column=3,
                                                                                                 padx=5, pady=5)
       ttk.Button(master, text="Exportar Segmentos a KML", command=self.export_segments_to_kml).grid(row=2, column=3,
                                                                                                     padx=5, pady=5)
       ttk.Button(master, text="Exportar Aeropuertos a KML", command=self.export_airports_to_kml).grid(row=6, column=3,
                                                                                                       padx=5, pady=5)
       ttk.Button(master, text="Exportar Vuelo Animado", command=self.export_animated_flight).grid(row=3, column=3,
                                                                                                   padx=5, pady=5)


       self.info_label = ttk.Label(master, text="")
       self.info_label.grid(row=5, column=0, columnspan=2)


   def load_selected_data(self):
       zona = self.dataset_selector.get()
       try:
           if zona == "Catalunya":
               self.airspace.load_all("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")
           elif zona == "España":
               self.airspace.load_all("Esp_nav.txt", "Esp_seg.txt", "Esp_aer.txt")
           elif zona == "Europa":
               self.airspace.load_all("Eur_nav.txt", "Eur_seg.txt", "Eur_aer.txt")


           self.plot_graph()
           self.info_label.config(text=f"Datos de {zona} cargados: {len(self.airspace.nav_points)} puntos")
       except Exception as e:
           messagebox.showerror("Error", f"No se pudieron cargar los datos:\n{str(e)}")


   def on_click(self, event):
       """Maneja el clic: muestra un menú de acciones para el punto seleccionado."""
       if not event.inaxes:
           return
       # Obtener coordenadas y punto más cercano (sin zoom)
       clicked_lon, clicked_lat = event.xdata, event.ydata
       closest = min(
           self.airspace.nav_points,
           key=lambda p: self.euclidean_distance_coords(clicked_lat, clicked_lon, p.latitude, p.longitude)
       )
       # Marcar el punto en el gráfico (opcional, sin zoom)
       self.ax.plot(clicked_lon, clicked_lat, marker='x', color='purple', markersize=10)
       self.canvas.draw_idle()
       # Crear ventana emergente personalizada
       popup = tk.Toplevel()
       popup.title(f"Acciones para {closest.name}")
       popup.geometry("300x150")


       # Función para manejar la selección
       def handle_action(action):
           if action == "origen":
               self.origin_entry.delete(0, tk.END)
               self.origin_entry.insert(0, closest.name)
               self.info_label.config(text=f"Origen asignado: {closest.name}")
           elif action == "destino":
               self.dest_entry.delete(0, tk.END)
               self.dest_entry.insert(0, closest.name)
               self.info_label.config(text=f"Destino asignado: {closest.name}")
           elif action == "punto":
               self.point_entry.delete(0, tk.END)
               self.point_entry.insert(0, closest.name)
               self.info_label.config(text=f"Punto actual: {closest.name}")
           # "cancelar" no hace nada
           popup.destroy()


       # Botones de acciones
       tk.Button(
           popup, text="Usar como ORIGEN",
           command=lambda: handle_action("origen"), bg="#FFCCCC"
       ).pack(pady=5, fill=tk.X, padx=10)
       tk.Button(
           popup, text="Usar como DESTINO",
           command=lambda: handle_action("destino"), bg="#CCE5FF"
       ).pack(pady=5, fill=tk.X, padx=10)
       tk.Button(
           popup, text="Usar como NOMBRE DE PUNTO",
           command=lambda: handle_action("punto"), bg="#E5FFCC"
       ).pack(pady=5, fill=tk.X, padx=10)
       tk.Button(
           popup, text="CANCELAR",
           command=lambda: handle_action("cancelar"), bg="#F0F0F0"
       ).pack(pady=5, fill=tk.X, padx=10)


   def show_reachable_points(self):
       point_name = self.point_entry.get().strip()
       point = self.airspace.get_point_by_name(point_name)
       if not point:
           self.info_label.config(text="Punto no encontrado.")
           return
       reached = set()
       queue = deque([point])
       while queue:
           current = queue.popleft()
           if current.number not in reached:
               reached.add(current.number)
               for segment in self.airspace.nav_segments:
                   # Verificar que el segmento es dirigido desde el nodo actual
                   if segment.origin_number == current.number:
                       neighbor = self.airspace.get_point_by_number(segment.destination_number)
                       if neighbor and neighbor.number not in reached:
                           queue.append(neighbor)


       self.plot_graph()  # Limpiar y redibujar
       for p in self.airspace.nav_points:
           if p.number in reached:
               self.ax.scatter(p.longitude, p.latitude, s=20, color='green')  # Puntos alcanzables en verde


       self.ax.scatter(point.longitude, point.latitude, s=40, color='blue')  # Origen en azul
       self.canvas.draw()


       # Mostrar ventana emergente con los nombres de los puntos alcanzables
       reachable_names = [p.name for p in self.airspace.nav_points if p.number in reached]
       messagebox.showinfo("Puntos Alcanzables", "\n".join(reachable_names))
       self.info_label.config(text=f"Puntos alcanzables desde {point.name}: {len(reached)}")


   def plot_graph(self):
       self.ax.clear()
       self.ax.set_title("Espacio Aéreo Catalunya - Puntos y Rutas")
       self.ax.set_xlabel("Longitud")
       self.ax.set_ylabel("Latitud")


       # Puntos de navegación
       for point in self.airspace.nav_points:
           self.ax.scatter(point.longitude, point.latitude, s=20, color='black', alpha=0.7)
           self.ax.text(point.longitude, point.latitude, point.name, fontsize=6, color='black')


       # Segmentos
       for segment in self.airspace.nav_segments:
           origin = self.airspace.get_point_by_number(segment.origin_number)
           destination = self.airspace.get_point_by_number(segment.destination_number)
           if origin and destination:
               self.ax.plot([origin.longitude, destination.longitude],
                            [origin.latitude, destination.latitude],
                            '#40E0D0', linewidth=0.7, alpha=0.5,
                            label='Segmentos' if segment == self.airspace.nav_segments[0] else "")


       # Aeropuertos
       for airport in self.airspace.nav_airports:
           if airport.sids:
               for sid in airport.sids:
                   self.ax.scatter(sid.longitude, sid.latitude, s=100, color=self.airport_color)
                   self.ax.text(sid.longitude, sid.latitude, airport.name, fontsize=8, color=self.airport_color)
           elif hasattr(airport, 'latitude') and hasattr(airport, 'longitude'):
               self.ax.scatter(airport.longitude, airport.latitude, s=100, color=self.airport_color)
               self.ax.text(airport.longitude, airport.latitude, airport.name, fontsize=8, color=self.airport_color)


       # Leyenda solo si hay elementos con label
       handles, labels = self.ax.get_legend_handles_labels()
       if handles:
           self.ax.legend(handles=handles, labels=labels)


       self.canvas.draw()


   def plot_neighbors(self):
       name = self.point_entry.get().strip()
       point = self.airspace.get_point_by_name(name)
       if not point:
           self.info_label.config(text=f"No se ha encontrado el punto {name}")
           return
       self.plot_graph()
       for s in self.airspace.nav_segments:
           if s.origin_number == point.number:
               neighbor = self.airspace.get_point_by_number(s.destination_number)
               if neighbor:
                   self.ax.plot([point.longitude, neighbor.longitude], [point.latitude, neighbor.latitude], 'r-')
                   self.ax.scatter(neighbor.longitude, neighbor.latitude, color='green', s=20)
       self.ax.scatter(point.longitude, point.latitude, color='blue', s=30)
       self.canvas.draw()


   def plot_shortest_path(self):
       origin_name = self.origin_entry.get().strip()
       dest_name = self.dest_entry.get().strip()
       origin = self.airspace.get_point_by_name(origin_name)
       dest = self.airspace.get_point_by_name(dest_name)
       if not origin or not dest:
           self.info_label.config(text="Origen o destino no encontrado")
           return
       open_set = PriorityQueue()
       open_set.put((0, [origin]))
       visited = set()
       while not open_set.empty():
           _, path = open_set.get()
           current = path[-1]
           if current.number == dest.number:
               self.last_path = path  # Guardamos el camino para posible exportación
               self.draw_path(path)
               return
           if current.number in visited:
               continue
           visited.add(current.number)
           for s in self.airspace.nav_segments:
               if s.origin_number == current.number:
                   neighbor = self.airspace.get_point_by_number(s.destination_number)
                   if neighbor and neighbor.number not in visited:
                       new_path = list(path)
                       new_path.append(neighbor)
                       cost = self.path_cost(new_path) + self.euclidean_distance(neighbor, dest)
                       open_set.put((cost, new_path))
       self.info_label.config(text="No se encontró camino")


   def draw_path(self, path):
       self.plot_graph()
       for i in range(len(path) - 1):
           p1, p2 = path[i], path[i + 1]
           self.ax.plot([p1.longitude, p2.longitude], [p1.latitude, p2.latitude], 'b-', linewidth=2)
       for p in path:
           self.ax.scatter(p.longitude, p.latitude, color='orange', s=30)
       self.canvas.draw()


   def path_cost(self, path):
       total = 0
       for i in range(len(path) - 1):
           for seg in self.airspace.nav_segments:
               if seg.origin_number == path[i].number and seg.destination_number == path[i + 1].number:
                   total += seg.distance
                   break
       return total


   def euclidean_distance(self, p1, p2):
       return sqrt((p1.latitude - p2.latitude) ** 2 + (p1.longitude - p2.longitude) ** 2)


   def euclidean_distance_coords(self, lat1, lon1, lat2, lon2):
       return sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)


   def export_all_navpoints_to_kml(self):
       if not self.airspace or not self.airspace.nav_points:
           messagebox.showerror("Error", "No hay puntos de navegación cargados.")
           return
       file_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
       if file_path:
           export_points_to_kml(self.airspace.nav_points, file_path)
           self.open_in_google_earth(file_path)


   def export_last_path_to_kml(self):
       if not hasattr(self, 'last_path') or not self.last_path:
           messagebox.showerror("Error", "No hay camino más corto calculado.")
           return
       file_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
       if file_path:
           export_path_to_kml(self.last_path, file_path)
           self.open_in_google_earth(file_path)


   def export_segments_to_kml(self):
       points_dict = {p.number: p for p in self.airspace.nav_points}
       file_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
       if file_path:
           export_segments_to_kml(self.airspace.nav_segments, points_dict, file_path)
           self.open_in_google_earth(file_path)


   def export_airports_to_kml(self):
       file_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
       if file_path:
           export_airports_to_kml(self.airspace.nav_airports, file_path)
           self.open_in_google_earth(file_path)


   def open_in_google_earth(self, file_path):
       try:
           subprocess.run([
               r"C:\\Program Files\\Google\\Google Earth Pro\\client\\googleearth.exe", file_path
           ], check=False)
       except Exception as e:
           messagebox.showinfo("KML guardado",
                               f"Archivo guardado en:\n{file_path}\n\nNo se pudo abrir Google Earth automáticamente.")


   def export_animated_flight(self):
       from kml_exporter import export_flight_animation_to_kml


       if not hasattr(self, 'last_path') or not self.last_path:
           messagebox.showerror("Error", "No hay camino más corto calculado.")
           return


       file_path = filedialog.asksaveasfilename(
           defaultextension=".kml",
           filetypes=[("KML files", "*.kml")]
       )


       if file_path:
           export_flight_animation_to_kml(self.last_path, file_path)
           # Abrir automáticamente en Google Earth después de exportar
           self.open_in_google_earth(file_path)
           messagebox.showinfo("Exportado", f"Vuelo animado exportado y abierto en Google Earth: {file_path}")




if __name__ == "__main__":
   root = tk.Tk()
   app = AirSpaceGUI(root)
   root.mainloop()








if __name__ == "__main__":
    root = tk.Tk()
    app = AirSpaceGUI(root)
    root.mainloop()
