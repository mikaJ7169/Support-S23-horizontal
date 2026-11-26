# Support horizontal pour Samsung Galaxy S23 (STL) — v3

Support imprimé en 3D qui maintient le Galaxy S23 **à l'horizontale (paysage)**, bien « anglobé » :
fond + parois + baguette frontale de 3 mm, seul l'écran dépasse. Le berceau est **incliné de 10° vers
l'arrière** : le téléphone repose contre le fond et ne peut pas basculer vers l'avant.

## Fichiers

- `support_s23_horizontal.stl` — modèle 3D (unités **mm**, STL binaire, maillage étanche, 1 seul corps)
- `gen_support_s23.py` — script de génération. Régénérer/modifier :
  `pip install trimesh manifold3d shapely numpy matplotlib` puis `python3 gen_support_s23.py`
- `preview_ortho.png`, `preview_iso.png` — aperçus du rendu (avec le téléphone inséré sur l'iso)

## Cotes du téléphone utilisées (officielles)

- Galaxy S23 : **146,3 × 70,9 × 7,6 mm**, coins du châssis ≈ **r11 mm** (design identique au S22)
- Écran 6,1" 2340×1080 (19.5:9) → 140,7 × 64,9 mm, coins d'écran ≈ r8
- Port **USB-C au centre du bord inférieur**, boutons **volume + power sur le bord droit (partie haute)**,
  tiroir SIM + enceinte sur le bord inférieur, micro sur le bord supérieur, capteurs photo en haut à gauche du dos

## v3 — ce qui change

- **USB-C à GAUCHE du support en regardant l'écran** (repère : +X = gauche vue de l'écran)
- **Bas du téléphone à 80 mm du sol** ; le câble USB-C peut passer **sous le téléphone**
  (ouverture 48 mm dans la paroi gauche + canal dans le seuil)
- **Cavité aux coins arrondis r12,5 mm** qui épouse la courbe du téléphone (jeu 0,5 mm) → rentre parfaitement
- Fenêtre 141,3 × 65,9 mm, coins r9 → tout l'écran visible, aucun recouvrement
- Insertion du téléphone **par le dessus** (ouverture supérieure)
- Logement des boutons volume/power dans le seuil (côté opposé à l'USB), poche pour les capteurs photo
- Corps, colonnes et embase entièrement **arrondis** (aucun coin saillant)

## Caractéristiques

- Cotes globales : **155,3 × 49,1 × 156,4 mm**, volume ≈ 156 cm³ (~40 g en PLA 20 %)
- Cavité : 147,3 × 71,9 × 8,6 mm ; baguette frontale 3 mm sur tout le pourtour
- Embase arrière de 34 mm pour la stabilité

## Impression recommandée

- À l'endroit (embase sur le plateau), buse 0,2 mm, remplissage 20–30 %, PLA
- Supports automatiques conseillés sous le « pont » central (espace sous le téléphone)
