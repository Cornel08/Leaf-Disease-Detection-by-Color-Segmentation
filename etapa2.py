import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np


# 1.Procesare

class ProcesorImagine:
    def __init__(self):
        # Încărcăm direct datele
        date = np.load("markeri_U.npz")
        self.U = {"sanatos": date["sanatos"], "boala": date["boala"], "fundal": date["fundal"]}


    def calculeaza_distanta(self, pixel_ab, marker):
        return np.sqrt(np.sum((pixel_ab - marker) ** 2))

    def proceseaza(self, cale_imagine):
        img_bgr = cv2.imread(cale_imagine)
        if img_bgr is None:
            return None

        # Redimensionare la 500px
        h, w = img_bgr.shape[:2]
        if w > h:
            scara = 500 / w
            dim = (500, int(h * scara))
        else:
            scara = 500 / h
            dim = (int(w * scara), 500)
        img_bgr = cv2.resize(img_bgr, dim)

        # Conversii
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2Lab)
        canal_l, canal_a, canal_b = cv2.split(img_lab)

        h, w = canal_a.shape
        # Măști goale
        mask_s = np.zeros((h, w), dtype=np.uint8)
        mask_b = np.zeros((h, w), dtype=np.uint8)
        mask_f = np.zeros((h, w), dtype=np.uint8)

        # Clasificare
        for y in range(h):
            for x in range(w):
                pixel = np.array([canal_a[y, x], canal_b[y, x]])
                d1 = self.calculeaza_distanta(pixel, self.U["sanatos"])
                d2 = self.calculeaza_distanta(pixel, self.U["boala"])
                d3 = self.calculeaza_distanta(pixel, self.U["fundal"])

                min_d = min(d1, d2, d3)
                if min_d == d1:
                    mask_s[y, x] = 255
                elif min_d == d3:
                    mask_f[y, x] = 255
                else:
                    mask_b[y, x] = 255

        # Curățare zgomot
        kernel = np.ones((3, 3), np.uint8)
        mask_b = cv2.morphologyEx(mask_b, cv2.MORPH_OPEN, kernel, iterations=2)
        mask_s = cv2.morphologyEx(mask_s, cv2.MORPH_OPEN, kernel, iterations=2)

        # Aplicăm masca peste imaginea originală RGB
        # Unde masca e albă, păstrăm culoarea. Unde e neagră, devine negru.
        seg_sanatos = cv2.bitwise_and(img_rgb, img_rgb, mask=mask_s)
        seg_boala = cv2.bitwise_and(img_rgb, img_rgb, mask=mask_b)
        seg_fundal = cv2.bitwise_and(img_rgb, img_rgb, mask=mask_f)

        # Statistici
        aria_b = np.sum(mask_b == 255)
        aria_s = np.sum(mask_s == 255)
        total = aria_b + aria_s
        procent = (aria_b / total * 100) if total > 0 else 0.0

        return img_rgb, seg_sanatos, seg_boala, seg_fundal, procent


# 2.Interfata

class AplicatieFinala:
    def __init__(self, root):
        self.root = root
        self.root.title("Proiect Detectie Frunze")
        self.root.geometry("1200x750")
        self.root.configure(bg="#f0f0f0")

        self.procesor = ProcesorImagine()
        self.cale = None

        self.setup_ui()

    def setup_ui(self):
        # Bara de sus
        top_frame = tk.Frame(self.root, bg="#333", pady=10)
        top_frame.pack(fill=tk.X)

        btn_load = tk.Button(top_frame, text="📂 Deschide Imagine", bg="#3498db", fg="white",
                             font=("Arial", 12), command=self.incarca)
        btn_load.pack(side=tk.LEFT, padx=20)

        self.btn_run = tk.Button(top_frame, text="▶ Analizează", bg="#27ae60", fg="white",
                                 font=("Arial", 12), state="disabled", command=self.analizeaza)
        self.btn_run.pack(side=tk.LEFT, padx=20)

        self.lbl_rez = tk.Label(top_frame, text="Rezultat: -- %", bg="#333", fg="white", font=("Arial", 14, "bold"))
        self.lbl_rez.pack(side=tk.RIGHT, padx=20)

        # Zona principala (Grid 2x2)
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Configure grid weight
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        self.p1 = self.make_panel(main_frame, "Imagine Originală", 0, 0)
        self.p2 = self.make_panel(main_frame, "Partea Sănătoasă ", 0, 1)
        self.p3 = self.make_panel(main_frame, "Partea Bolnavă ", 1, 0)
        self.p4 = self.make_panel(main_frame, "Fundal ", 1, 1)

    def make_panel(self, parent, title, r, c):
        f = tk.Frame(parent, bg="white", bd=2, relief="groove")
        f.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        tk.Label(f, text=title, bg="#ddd", font=("Arial", 10, "bold")).pack(fill=tk.X)
        l = tk.Label(f, bg="white", text="Fără imagine")
        l.pack(expand=True, fill=tk.BOTH)
        return l

    def incarca(self):
        path = filedialog.askopenfilename()
        if path:
            self.cale = path
            img = Image.open(path)
            img.thumbnail((400, 300))
            photo = ImageTk.PhotoImage(img)
            self.p1.config(image=photo, text="")
            self.p1.image = photo
            self.btn_run.config(state="normal")
            # Reset
            for p in [self.p2, self.p3, self.p4]: p.config(image="", text="...")

    def analizeaza(self):
        if not self.cale: return
        self.lbl_rez.config(text="Procesare...", fg="yellow")
        self.root.update()

        res = self.procesor.proceseaza(self.cale)
        if not res: return

        img_orig, img_s, img_b, img_f, proc = res

        self.show_img(self.p1, img_orig)
        self.show_img(self.p2, img_s)
        self.show_img(self.p3, img_b)
        self.show_img(self.p4, img_f)

        col = "#e74c3c" if proc > 15 else "#2ecc71"
        self.lbl_rez.config(text=f"Severitate Boală: {proc:.2f}%", fg=col)

    def show_img(self, panel, img_arr):
        im = Image.fromarray(img_arr)
        im.thumbnail((400, 300))
        ph = ImageTk.PhotoImage(im)
        panel.config(image=ph, text="")
        panel.image = ph


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicatieFinala(root)
    root.mainloop()