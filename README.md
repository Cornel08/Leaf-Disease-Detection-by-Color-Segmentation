# Leaf Disease Detection by Color Segmentation 

### Sistem Automat de Detectare a Bolii "Black Rot" la Măr

Acest proiect propune o soluție software desktop ("EcoPlant AI") pentru detectarea automată a bolilor foliare la măr, cu accent pe **Putregaiul Negru (Black Rot)**. Aplicația utilizează tehnici de procesare a imaginilor și segmentare cromatică pentru a oferi un diagnostic rapid și o estimare a severității atacului.

---

## 📝 Descriere

Agricultura de precizie necesită metode rapide și neinvazive pentru monitorizarea sănătății culturilor. Metodele tradiționale de inspecție vizuală sunt subiective și lente.

Acest proiect rezolvă problema **detectării bolilor în condiții de iluminare variabilă** (umbre, soare puternic) prin utilizarea spațiului de culoare **CIELAB**. Algoritmul ignoră componenta de luminozitate ($L^*$) și analizează doar informația cromatică ($a^*, b^*$), permițând o segmentare robustă a zonelor afectate.

### Funcționalități Principale:
* 📸 **Încărcare Imagini:** Suport pentru formatele standard (.jpg, .png).
* 🔍 **Analiză Automată:** Segmentarea imaginii în: Țesut Sănătos, Boală (Black Rot) și Fundal.
* 📊 **Calcul Severitate:** Estimarea automată a procentului de suprafață afectată.
* 🎨 **Vizualizare Avansată:** Interfață grafică modernă cu hărți de segmentare și grafice statistice.
* 🧠 **Post-procesare Inteligentă:** Filtrare morfologică pentru eliminarea zgomotului și a detecțiilor false.

---

## 🛠️ Tehnologii Utilizate

Proiectul este dezvoltat în **Python 3.x** și utilizează următoarele biblioteci:

* **OpenCV (`cv2`):** Pentru procesarea imaginilor, conversii de culoare și operații morfologice.
* **NumPy:** Pentru calcule matematice și manipularea matricilor.
* **Tkinter:** Pentru interfața grafică (GUI) nativă.
* **Pillow (PIL):** Pentru manipularea imaginilor în interfață.
* **Matplotlib:** Pentru generarea graficelor statistice (Pie Chart).

---

## 🚀 Cum să rulezi proiectul

### 1. Instalare Dependințe
Asigură-te că ai Python instalat. Apoi, instalează bibliotecile necesare:

```bash
pip install opencv-python numpy matplotlib pillow scikit-image
