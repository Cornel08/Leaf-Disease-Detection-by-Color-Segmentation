import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.draw import polygon2mask
import os
import sys

# Liste pentru a stoca markerii [ea, eb] din FIECARE imagine
markeri_sanatosi = []
markeri_boala = []
markeri_fundal = []

cale_folder = "dataset/" # Folderul cu imaginile de antrenare

def selecteaza_regiune(img_display, titlu):
    """
    Afișează o imagine și permite utilizatorului să selecteze un poligon.
    Returnează o mască binară a poligonului.
    """

    fig, ax = plt.subplots()
    ax.imshow(img_display)
    ax.set_title(titlu)

    puncte = plt.ginput(n=0, timeout=0) # programul se opreste si asteapta sa facem poligonul
    plt.close(fig)

    if not puncte or len(puncte) < 3:
        print(f"Atenție: Nu au fost selectate suficiente puncte pentru '{titlu}'. Regiunea va fi omisă.")
        return None

    print(f"Au fost selectate {len(puncte)} puncte.")

    # Conversie puncte pentru polygon2mask
    puncte_np = np.array([(p[1], p[0]) for p in puncte])

    # Creăm masca binară
    forma_imaginii = img_display.shape[:2]
    masca = polygon2mask(forma_imaginii, puncte_np)
    return masca


def calculeaza_marker(canal_a, canal_b, masca):
    #Calculează markerul de culoare medie [ea, eb] dintr-o mască
    if masca is None:
        return None

    if np.sum(masca) == 0:
        return None

    # Extragem pixelii
    pixeli_a = canal_a[masca]
    pixeli_b = canal_b[masca]

    # Calculăm media
    ea = np.mean(pixeli_a)
    eb = np.mean(pixeli_b)

    return [ea, eb]

#BUCLA PRINCIPALA

if not os.path.exists(cale_folder):# Verificăm folderul
    print(f"EROARE: Folderul '{cale_folder}' nu a fost găsit.")
    sys.exit()

lista_imagini = os.listdir(cale_folder)
if not lista_imagini:
    print(f"EROARE: Folderul '{cale_folder}' este gol.")
    sys.exit()

numar_imagini = len(lista_imagini)

for i, nume_imagine in enumerate(lista_imagini):# Parcurgem imaginile

    # Filtru extensii
    if not (nume_imagine.endswith('.jpg') or nume_imagine.endswith('.png') or nume_imagine.endswith('.JPG')):
        continue

    cale_completa = os.path.join(cale_folder, nume_imagine)

    print(f"\n--- Procesare Imagine {i + 1}/{numar_imagini}: {nume_imagine} ---")

    img_bgr = cv2.imread(cale_completa) # 1. Citim imaginea
    if img_bgr is None:
        print(f"Atenție: Nu am putut citi imaginea {nume_imagine}. Trec la următoarea.")
        continue

    # Conversii
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB) #o copie ca sa o afisam pe ecran
    img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2Lab)
    canal_l, canal_a, canal_b = cv2.split(img_lab)  #pastram doar canalele a si b

    # 2. Selectăm manual cele 3 regiuni
    # R1: Sănătos
    masca_sanatos = selecteaza_regiune(img_rgb, "R1: Regiunea SĂNĂTOASĂ (Verde Curat)")
    marker_s = calculeaza_marker(canal_a, canal_b, masca_sanatos)
    if marker_s:
        markeri_sanatosi.append(marker_s)
        print(f"Marker Sănătos: {marker_s}")

    # R2: Boală
    masca_boala = selecteaza_regiune(img_rgb, "R2: Regiunea BOLNAVĂ (Pată)")
    marker_b = calculeaza_marker(canal_a, canal_b, masca_boala)
    if marker_b:
        markeri_boala.append(marker_b)
        print(f"Marker Boală: {marker_b}")

    # R3: Fundal
    masca_fundal = selecteaza_regiune(img_rgb, "R3: Regiunea FUNDAL (Gri)")
    marker_f = calculeaza_marker(canal_a, canal_b, masca_fundal)
    if marker_f:
        markeri_fundal.append(marker_f)
        print(f"Marker Fundal: {marker_f}")

#CALCULUL FINAL

# Calculăm mediile finale
U_sanatos = np.mean(markeri_sanatosi, axis=0) if markeri_sanatosi else [0, 0]
U_boala = np.mean(markeri_boala, axis=0) if markeri_boala else [0, 0]
U_fundal = np.mean(markeri_fundal, axis=0) if markeri_fundal else [0, 0]

#Cream Matricea U
U = {
    "sanatos": U_sanatos,
    "boala": U_boala,
    "fundal": U_fundal
}

print("\n--- 5. REZULTATE (Matricea U Simplificată) ---")
print("Markerii medii globali [ea, eb] sunt:")
print(f"U Sănătos:  {U['sanatos']}")
print(f"U Boală:    {U['boala']}")
print(f"U Fundal:   {U['fundal']}")

#SALVAREA REZULTATELOR

np.savez("markeri_U.npz",
         sanatos=U['sanatos'],
         boala=U['boala'],
         fundal=U['fundal'])

print("\nMarkerii au fost salvați cu succes în fișierul 'markeri_U.npz'.")
