import pyvista as pv
import os
import tkinter as tk
from threading import Thread


# Clase que representa una región cognitiva
class RegionCognitiva:
    def __init__(self, nombre, posicion, descripcion):
        self.nombre = nombre
        self.posicion = posicion
        self.descripcion = descripcion


# Clase que muestra la ventana educativa con información
class InterfazEducativa:
    @staticmethod
    def mostrar(region: RegionCognitiva):
        def ventana():
            root = tk.Tk()
            root.title(f"Región: {region.nombre}")
            root.geometry("400x150")
            tk.Label(root, text=region.nombre, font=("Arial", 14, "bold")).pack(pady=5)
            tk.Message(
                root, text=region.descripcion, width=380, font=("Arial", 12)
            ).pack(pady=10)
            tk.Button(root, text="Cerrar", command=root.destroy).pack(pady=5)
            root.mainloop()

        Thread(target=ventana).start()


# Clase principal para la visualización 3D del cerebro
class Cerebro3D:
    def __init__(self, modelo_path, textura_path):
        self.modelo_path = modelo_path
        self.textura_path = textura_path
        self.brain = None
        self.textura = None
        self.regiones = {}
        self.marcadores = pv.PolyData()
        self.plotter = pv.Plotter()

    def cargar_modelo(self):
        self.brain = pv.read(self.modelo_path)
        self.textura = pv.read_texture(self.textura_path)

    def definir_regiones(self):
        # Diccionario de regiones: ID -> Objeto
        self.regiones = {
            1: RegionCognitiva(
                "Lóbulo frontal", [0.1, 0.0, 0.1], "Planificación, decisiones, control."
            ),
            2: RegionCognitiva(
                "Lóbulo parietal", [0.0, 0.1, 0.1], "Procesamiento sensorial."
            ),
            3: RegionCognitiva(
                "Lóbulo temporal", [0.1, -0.1, 0.0], "Audición, lenguaje, memoria."
            ),
            4: RegionCognitiva(
                "Lóbulo occipital", [-0.1, 0.0, 0.0], "Procesamiento visual."
            ),
            5: RegionCognitiva(
                "Cerebelo", [0.0, -0.15, -0.1], "Movimiento y equilibrio."
            ),
            6: RegionCognitiva(
                "Tronco encefálico", [0.0, -0.05, -0.15], "Funciones vitales."
            ),
        }

    def generar_marcadores(self):
        for id_region, region in self.regiones.items():
            esfera = pv.Sphere(radius=0.01, center=region.posicion)
            # Usar ID numérico para etiquetar
            esfera.point_data["region_id"] = [id_region] * esfera.n_points
            self.marcadores = self.marcadores.merge(esfera)

    def mostrar(self):
        self.cargar_modelo()
        self.definir_regiones()
        self.generar_marcadores()

        self.plotter.add_mesh(self.brain, texture=self.textura)
        self.plotter.add_mesh(self.marcadores, color="red", opacity=0.0, pickable=True)

        def callback(picked):
            try:
                if hasattr(picked, "point_data") and "region_id" in picked.point_data:
                    id_region = int(picked.point_data["region_id"][0])
                    region = self.regiones.get(id_region)
                    if region:
                        print(f"🧠 Región seleccionada: {region.nombre}")
                        InterfazEducativa.mostrar(region)
            except Exception as e:
                print(f"❌ Error en el callback: {e}")

        self.plotter.enable_point_picking(
            callback=callback, use_picker=True, show_message=False, show_point=False
        )

        self.plotter.add_title("Explorador Cognitivo del Cerebro Humano", font_size=14)
        self.plotter.show()


# --------- Punto de entrada ---------
if __name__ == "__main__":
    modelo = os.path.join("..", "models", "brain", "brain.obj")
    textura = os.path.join("..", "models", "brain", "texture_0.png")
    cerebro = Cerebro3D(modelo, textura)
    cerebro.mostrar()
