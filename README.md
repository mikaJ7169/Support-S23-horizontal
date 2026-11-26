# Support horizontal pour Samsung Galaxy S23 (STL) — v4

Support imprimé en 3D, monolithique en L (style mini-écran) : une **embase plate** + un **panneau arrière
incliné de 10°** qui porte le berceau en haut. Le Galaxy S23 est en **paysage**, inséré par le dessus,
bien « anglobé » (fond + parois + baguette frontale de 3 mm) : **seul l'écran est visible**.

## Fichiers

- `support_s23_horizontal.stl` — modèle 3D (unités **mm**, STL binaire, maillage étanche, 1 seul corps)
- `gen_support_s23.py` — script de génération. Régénérer/modifier :
  `pip install trimesh manifold3d shapely numpy matplotlib` puis `python3 gen_support_s23.py`
- `preview_ortho.png`, `preview_iso.png` — aperçus (téléphone inséré sur l'iso)

## Règles respectées

- **Charge par la gauche** : en regardant l'écran du téléphone, le port USB-C est à gauche du support.
  Fente arrondie de 44 mm sur le flanc gauche (USB-C + SIM + enceinte) : n'importe quelle fiche USB-C passe.
- **Boutons volume + power** (bord droit du S23, partie haute → seuil du berceau côté opposé) : logement dédié.
- **Hauteur 8 cm** : bas du téléphone à exactement 80 mm du sol ; le câble peut passer **sous** le support.
- **Incliné de 10° vers l'arrière** : le téléphone repose contre le fond, il ne bascule pas vers l'avant.
- **Courbes du téléphone** : cavité aux coins arrondis r12,5 mm (châssis ≈ r11 + jeu 0,5 mm), fenêtre coins r9
  (écran ≈ r8) → le téléphone rentre parfaitement, tout l'écran est dégagé.
- **Beauté** : tous les bords extérieurs arrondis (corps r6, panneau r8, embase r10), fente USB à coins arrondis,
  fenêtre d'allègement dans le panneau arrière. Aucun coin saillant.
- Poche pour les capteurs photo dans le fond, fente pour le micro du bord supérieur.

## Cotes du téléphone (officielles)

146,3 × 70,9 × 7,6 mm — écran 6,1" 2340×1080 (19.5:9) = 140,7 × 64,9 mm — USB-C au centre du bord inférieur.

## Caractéristiques du support

- Cotes globales : **160 × 64 × 157,4 mm**, volume ≈ 243 cm³ (~60 g en PLA 20 %)
- Cavité : 147,3 × 71,9 × 8,6 mm (jeu 0,5 mm), ouverte en haut pour l'insertion
- Fenêtre écran : 141,3 × 76 mm (ouverte en haut), baguette frontale 3 mm

## Impression recommandée

- À l'endroit (embase sur le plateau), buse 0,2 mm, remplissage 20–30 %, PLA
- Supports automatiques conseillés sous le berceau (pont au-dessus du vide de 8 cm)
