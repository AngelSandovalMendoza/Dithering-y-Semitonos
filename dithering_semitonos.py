import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random

# Rutas de las imágenes de puntos y matrices
PUNTOS_PATHS = [
    './semitonos/puntos/punto_1.jpg', './semitonos/puntos/punto_2.jpg', './semitonos/puntos/punto_3.jpg',
    './semitonos/puntos/punto_4.jpg', './semitonos/puntos/punto_5.jpg', './semitonos/puntos/punto_6.jpg',
    './semitonos/puntos/punto_7.jpg', './semitonos/puntos/punto_8.jpg', './semitonos/puntos/punto_9.jpg'
]
MATRICES_PATHS = [
    './semitonos/matrices/matriz_1.jpg', './semitonos/matrices/matriz_2.jpg', './semitonos/matrices/matriz_3.jpg',
    './semitonos/matrices/matriz_4.jpg', './semitonos/matrices/matriz_5.jpg', './semitonos/matrices/matriz_6.jpg',
    './semitonos/matrices/matriz_7.jpg', './semitonos/matrices/matriz_8.jpg', './semitonos/matrices/matriz_9.jpg'
]

PUNTOS = [Image.open(path) for path in PUNTOS_PATHS]
MATRICES = [Image.open(path) for path in MATRICES_PATHS]

def promedio_gris(bloque):
    return sum(bloque.getdata()) // (bloque.width * bloque.height)

def aplica_matriz(matriz, bloque):
    resultado = Image.new('L', bloque.size)
    for i in range(bloque.width):
        for j in range(bloque.height):
            pixel = bloque.getpixel((i, j))
            if pixel < matriz[i % 3][j % 3] * 28:
                resultado.putpixel((i, j), 0)
            else:
                resultado.putpixel((i, j), 255)
    return resultado

def dithering_azar(imagen):
    imagen_grayscale = imagen.convert('L')
    nueva_imagen = Image.new('L', imagen.size)
    for x in range(imagen.width):
        for y in range(imagen.height):
            pixel = imagen_grayscale.getpixel((x, y))
            valor_random = random.randint(0, 255)
            nueva_imagen.putpixel((x, y), 0 if pixel <= valor_random else 255)
    return nueva_imagen

def dithering_ordenado(imagen):
    MATRIZ_ORDENADA = [[8, 3, 4], [6, 1, 2], [7, 5, 9]]
    imagen_grayscale = imagen.convert('L')
    nueva_imagen = Image.new('L', imagen.size)
    for x in range(0, imagen.width, 3):
        for y in range(0, imagen.height, 3):
            bloque = imagen_grayscale.crop((x, y, x + 3, y + 3))
            nuevo_bloque = aplica_matriz(MATRIZ_ORDENADA, bloque)
            nueva_imagen.paste(nuevo_bloque, (x, y))
    return nueva_imagen

def dithering_disperso(imagen):
    MATRIZ_DISPERSA = [[1, 7, 4], [5, 8, 3], [6, 2, 9]]
    imagen_grayscale = imagen.convert('L')
    nueva_imagen = Image.new('L', imagen.size)
    for x in range(0, imagen.width, 3):
        for y in range(0, imagen.height, 3):
            bloque = imagen_grayscale.crop((x, y, x + 3, y + 3))
            nuevo_bloque = aplica_matriz(MATRIZ_DISPERSA, bloque)
            nueva_imagen.paste(nuevo_bloque, (x, y))
    return nueva_imagen

def semitonos_puntos(imagen):
    step = 28
    punto_ancho, punto_alto = PUNTOS[0].size
    imagen_grayscale = imagen.convert('L')
    nueva_imagen = Image.new('L', imagen.size)
    for x in range(0, imagen.width, punto_ancho):
        for y in range(0, imagen.height, punto_alto):
            bloque = imagen_grayscale.crop((x, y, x + punto_ancho, y + punto_alto))
            promedio = promedio_gris(bloque)
            indice = min(promedio // step, len(PUNTOS) - 1)
            nueva_imagen.paste(PUNTOS[indice], (x, y))
    return nueva_imagen

def semitonos_matrices(imagen):
    step = 28
    matriz_ancho, matriz_alto = MATRICES[0].size
    imagen_grayscale = imagen.convert('L')
    nueva_imagen = Image.new('L', imagen.size)
    for x in range(0, imagen.width, matriz_ancho):
        for y in range(0, imagen.height, matriz_alto):
            bloque = imagen_grayscale.crop((x, y, x + matriz_ancho, y + matriz_alto))
            promedio = promedio_gris(bloque)
            indice = min(promedio // step, len(MATRICES) - 1)
            nueva_imagen.paste(MATRICES[indice], (x, y))
    return nueva_imagen

class ImageEditorApp:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Dithering y Semitonos")
        self.original_image = None
        self.processed_image = None
        self.image_label = tk.Label(ventana)
        self.image_label.pack()

        self.open_button = tk.Button(ventana, text="Abrir Imagen", command=self.abrir_imagen)
        self.open_button.pack()

        self.effects_frame = tk.Frame(ventana)
        self.effects_frame.pack()
        
        tk.Button(self.effects_frame, text="Dithering Azar", command=self.apply_dithering_azar).grid(row=0, column=0)
        tk.Button(self.effects_frame, text="Dithering Ordenado", command=self.apply_dithering_ordenado).grid(row=0, column=1)
        tk.Button(self.effects_frame, text="Dithering Disperso", command=self.apply_dithering_disperso).grid(row=0, column=2)
        tk.Button(self.effects_frame, text="Semitonos con Puntos", command=self.apply_semitonos_puntos).grid(row=1, column=0)
        tk.Button(self.effects_frame, text="Semitonos con Matrices", command=self.apply_semitonos_matrices).grid(row=1, column=1)
        
        self.save_button = tk.Button(ventana, text="Guardar Imagen", command=self.save_image)
        self.save_button.pack()

    def abrir_imagen(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.mostrar_imagen(self.original_image)

    def mostrar_imagen(self, img):
        img.thumbnail((400, 400))
        self.tk_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_image)

    def apply_effect(self, effect_func):
        if self.original_image:
            self.processed_image = effect_func(self.original_image)
            self.mostrar_imagen(self.processed_image)
        else:
            messagebox.showwarning("Advertencia", "Primero debes cargar una imagen.")

    def apply_dithering_azar(self):
        self.apply_effect(dithering_azar)

    def apply_dithering_ordenado(self):
        self.apply_effect(dithering_ordenado)

    def apply_dithering_disperso(self):
        self.apply_effect(dithering_disperso)

    def apply_semitonos_puntos(self):
        self.apply_effect(semitonos_puntos)

    def apply_semitonos_matrices(self):
        self.apply_effect(semitonos_matrices)

    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.processed_image.save(file_path)
        else:
            messagebox.showwarning("Advertencia", "No hay imagen para guardar.")

if __name__ == "__main__":
    ventana = tk.Tk()
    app = ImageEditorApp(ventana)
    ventana.mainloop()
