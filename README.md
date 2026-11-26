# Support horizontal pour Samsung Galaxy S23 (STL)

Support imprimé en 3D qui maintient le Galaxy S23 **à l'horizontale (paysage)**, bien "anglobé" :
fond plein + 4 parois + baguette frontale de 3 mm tout autour, seul l'écran dépasse.

## Fichiers

- `support_s23_horizontal.stl` — le modèle 3D (unités : **mm**, STL binaire, maillage étanche, 1 seul corps)
- `gen_support_s23.py` — script de génération (Python). Pour régénérer/modifier :
  `pip install trimesh manifold3d shapely numpy matplotlib` puis `python3 gen_support_s23.py`

## Cotes du téléphone utilisées (officielles)

- Galaxy S23 : **146,3 × 70,9 × 7,6 mm**
- Écran 6,1" 2340×1080 (19.5:9) → fenêtre du support : 141,3 × 65,9 mm (coins arrondis r6)
- Port **USB-C au centre du bord inférieur** → placé **à gauche du support** (charge par la gauche)
- Boutons **volume + power sur le bord droit (partie haute)** → paroi basse du support, avec logement dédié
- Tiroir SIM sur le bord inférieur (gauche de l'USB-C) et enceinte sur ce même bord → dégagés par l'ouverture latérale
- Capteurs photo (dos, coin haut-gauche) → poche dans le fond (coin bas-droit du support)

## Caractéristiques du support

- Cotes globales : **155,3 × 51,6 × 81,9 mm**, volume ≈ 112 cm³ (~30 g en PLA 20 %)
- Cavité : 147,3 × 71,9 × 8,6 mm (jeu de 0,5 mm autour du téléphone)
- **Ouverture USB-C à gauche : 38 mm de haut, sur toute la profondeur** → n'importe quelle fiche
  USB-C passe, et le câble peut aussi ressortir directement vers l'arrière
- Logement des boutons volume/power dans la paroi basse (côté droit)
- Embase arrière de 34 mm pour la stabilité

## Impression recommandée

- À plat **sur le dos** (face arrière au plateau) : aucun support nécessaire
- Buse 0,2 mm, remplissage 20–30 %, PLA
