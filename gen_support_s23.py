#!/usr/bin/env python3
"""
Support horizontal (paysage) pour Samsung Galaxy S23 -> fichier STL (unites : mm).

Cotes officielles Galaxy S23 : 146.3 x 70.9 x 7.6 mm, ecran 6.1" 2340x1080 (19.5:9).
Layout : port USB-C au centre du bord inferieur, boutons volume + power sur le
bord droit (partie haute), tiroir SIM sur le bord inferieur a gauche de l'USB-C,
micro sur le bord superieur, 3 capteurs photo en haut a gauche du dos.

Orientation choisie : le bord inferieur du telephone (USB-C) fait face a la
GAUCHE du support -> charge par la gauche. Apres rotation paysage :
  - paroi gauche du support  = bord USB-C / enceinte / SIM du telephone
  - paroi basse du support   = bord des boutons (volume + power)
  - paroi droite             = bord superieur (micro)
  - paroi haute              = bord gauche (rien)
  - capteurs photo (dos)     = coin bas-droit du fond

Le telephone est "anglobe" : fond plein + 4 parois + baguette frontale qui
recouvre 3 mm tout autour -> seul l'ecran depasse.
"""

import numpy as np
import trimesh
from trimesh.creation import box as tbox, extrude_polygon
from trimesh.transformations import translation_matrix, rotation_matrix
from shapely.geometry import box as sbox

# ---------------- Telephone (mm) ----------------
PHONE_L = 146.3   # longueur -> axe X du support (paysage)
PHONE_W = 70.9    # largeur  -> axe Z du support
PHONE_T = 7.6     # epaisseur-> axe Y du support

# ---------------- Parametres du support (mm) ----------------
CLEAR  = 0.5    # jeu autour du telephone
WALL   = 4.0    # epaisseur parois
BACK   = 5.0    # epaisseur du fond
LIP_T  = 4.0    # epaisseur baguette frontale
LIP    = 3.0    # recouvrement frontal (maintien)
BOT    = 6.0    # hauteur paroi basse (le telephone repose dessus)
FOOT_D = 34.0   # profondeur de l'embase vers l'arriere
R_OUT  = 6.0    # rayon coins exterieurs
R_WIN  = 6.0    # rayon coins de la fenetre ecran

# ---------------- Geometrie derivee ----------------
cav_x = PHONE_L + 2 * CLEAR                 # 147.3
cav_z = PHONE_W + 2 * CLEAR                 # 71.9
cav_y = PHONE_T + 2 * CLEAR                 # 8.6
body_x = cav_x + 2 * WALL                   # 155.3
body_z = BOT + cav_z + WALL                 # 81.9
body_y = BACK + cav_y + LIP_T               # 17.6
zc = BOT + cav_z / 2                        # centre vertical de la cavite (41.95)
win_x = cav_x - 2 * LIP                     # 141.3
win_z = cav_z - 2 * LIP                     # 65.9

# Ouvertures (x0,x1,y0,y1,z0,z1)
USB_CUT = (-78.5, -72.5, -1.0, body_y + 1, 23.0, 61.0)   # passage cable USB-C (38 mm de haut, toute la profondeur)
BTN_CUT = (-10.0, 74.5, -1.0, body_y + 1, -1.0, BOT + 0.2)  # logement boutons volume/power (paroi basse, cote droit)
MIC_R   = (body_x / 2 - 5.0, body_x / 2 + 1.0, -1.0, body_y + 1, zc - 4.0, zc + 4.0)  # micro bord superieur du tel
MIC_T   = (-6.0, 6.0, -1.0, body_y + 1, body_z - 5.0, body_z + 1.0)                    # bord gauche du tel
CAM     = (40.0, cav_x / 2, BACK - 2.6, BACK + 0.2, BOT, BOT + 16.0)  # poche capteurs photo (coin bas-droit du fond)


def rrect(w, h, r):
    """Polygone rectangle arrondi w x h, rayon r, centre a l'origine."""
    return sbox(-w / 2, -h / 2, w / 2, h / 2).buffer(r, join_style=1).buffer(-r, join_style=1)


def prism_xz(poly, y0, y1, xc=0.0, zc=0.0):
    """Prisme : polygone dans le plan XZ, extrude selon Y de y0 a y1."""
    m = extrude_polygon(poly, y1 - y0)
    m.apply_transform(rotation_matrix(-np.pi / 2, [1, 0, 0]))  # extrusion Z -> +Y, plan XY -> XZ
    m.apply_translation([xc, y0, zc])
    return m


def prism_xy(poly, z0, z1, xc=0.0, yc=0.0):
    m = extrude_polygon(poly, z1 - z0)
    m.apply_translation([xc, yc, z0])
    return m


def bbox(x0, x1, y0, y1, z0, z1):
    c = [(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]
    return tbox(extents=[x1 - x0, y1 - y0, z1 - z0], transform=translation_matrix(c))


# ---------------- Construction ----------------
body = prism_xz(rrect(body_x, body_z, R_OUT), 0.0, body_y, zc=body_z / 2)
foot = prism_xy(rrect(body_x, FOOT_D + BACK, 8.0), 0.0, BOT, yc=(BACK - FOOT_D) / 2)

solid = trimesh.boolean.union([body, foot], engine="manifold")

cavity = bbox(-cav_x / 2, cav_x / 2, BACK, BACK + cav_y, BOT, BOT + cav_z)
window = prism_xz(rrect(win_x, win_z, R_WIN), BACK + cav_y - 0.2, body_y + 1.0, zc=zc)
cuts = [cavity, window]
for c in (USB_CUT, BTN_CUT, MIC_R, MIC_T, CAM):
    cuts.append(bbox(*c))

mesh = trimesh.boolean.difference([solid] + cuts, engine="manifold")
mesh.merge_vertices()

# ---------------- Validation ----------------
print("watertight :", mesh.is_watertight)
print("winding ok :", mesh.is_winding_consistent)
print("corps      :", mesh.body_count)
print("volume     : %.1f cm3" % (mesh.volume / 1000.0))
print("dimensions : %.1f x %.1f x %.1f mm" % tuple(mesh.extents))

# Le telephone + ses boutons + une fiche USB doivent passer sans collision
tests = {
    "telephone": ([-PHONE_L / 2, PHONE_L / 2], [BACK + CLEAR, BACK + CLEAR + PHONE_T], [BOT + CLEAR, BOT + CLEAR + PHONE_W]),
    "boutons":   ([15.0, 73.0], [BACK + CLEAR, BACK + CLEAR + PHONE_T], [BOT - 1.2, BOT + CLEAR]),
    "fiche USB": ([-82.0, -PHONE_L / 2 + 0.15], [BACK + CLEAR, BACK + CLEAR + PHONE_T], [zc - 5.5, zc + 5.5]),
}
for name, (xr, yr, zr) in tests.items():
    t = bbox(xr[0], xr[1], yr[0], yr[1], zr[0], zr[1])
    inter = trimesh.boolean.intersection([mesh, t], engine="manifold")
    print("collision %-10s : %.3f mm3 (attendu 0)" % (name, inter.volume if inter is not None else 0.0))

# Tests de matiere ponctuels : volume d'intersection d'une petite sonde avec le support
probes = {  # (centre, taille, volume attendu si plein)
    "fenetre (vide)":        ((0, 15.0, zc), (10, 2, 10), 0),
    "baguette basse (plein)": ((0, 15.0, BOT + 1.5), (10, 2, 3), 60),
    "cavite (vide)":         ((0, 9.3, zc), (10, 2, 10), 0),
    "fond (plein)":          ((0, 2.5, zc), (10, 2, 10), 200),
    "paroi gauche (plein)":  ((-75.5, 9.0, 10.0), (2, 8, 8), 128),
    "ouverture USB (vide)":  ((-75.5, 9.0, zc), (2, 8, 20), 0),
    "logement boutons(vide)": ((30.0, 9.0, 3.0), (10, 8, 4), 0),
    "paroi basse (plein)":   ((-40.0, 9.0, 3.0), (10, 8, 4), 320),
    "embase (plein)":        ((0, -20.0, 3.0), (10, 8, 4), 320),
    "poche capteurs(vide)":  ((60.0, 3.8, 14.0), (10, 1.5, 8), 0),
}
for name, (c, s, expect) in probes.items():
    t = bbox(c[0] - s[0] / 2, c[0] + s[0] / 2, c[1] - s[1] / 2, c[1] + s[1] / 2, c[2] - s[2] / 2, c[2] + s[2] / 2)
    inter = trimesh.boolean.intersection([mesh, t], engine="manifold")
    v = inter.volume if inter is not None else 0.0
    ok = "OK" if (v < 1e-6) == (expect == 0) else "ERREUR"
    print("sonde %-24s : %.1f mm3 (attendu %s) %s" % (name, v, expect, ok))

# ---------------- Export STL ----------------
out = "/workspace/support_s23_horizontal.stl"
mesh.export(out)
print("STL ecrit :", out)

# ---------------- Apercus PNG ----------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def render(meshes, path, views):
    fig = plt.figure(figsize=(5.2 * len(views), 5.6))
    for i, (title, elev, azim) in enumerate(views, 1):
        ax = fig.add_subplot(1, len(views), i, projection="3d")
        for m, color in meshes:
            pc = Poly3DCollection(m.triangles, facecolor=color, edgecolor="k", linewidths=0.05, alpha=1.0)
            ax.add_collection3d(pc)
        mins, maxs = meshes[0][0].bounds
        for m, _ in meshes:
            mins = np.minimum(mins, m.bounds[0]); maxs = np.maximum(maxs, m.bounds[1])
        ax.set_xlim(mins[0], maxs[0]); ax.set_ylim(mins[1], maxs[1]); ax.set_zlim(mins[2], maxs[2])
        ax.set_box_aspect((maxs - mins).tolist())
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(title, fontsize=9)
        ax.set_axis_off()
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)


phone = bbox(-PHONE_L / 2, PHONE_L / 2, BACK + CLEAR, BACK + CLEAR + PHONE_T, BOT + CLEAR, BOT + CLEAR + PHONE_W)
render([(mesh, "#9fc3e8")], "/workspace/preview_ortho.png",
       [("Face (ecran)", 0, 90), ("Dos", 0, -90), ("Gauche = USB-C", 0, 180), ("Dessus", 90, 90)])
render([(mesh, "#9fc3e8"), (phone, "#e8c39f")], "/workspace/preview_iso.png",
       [("Iso face+gauche, tel insere", 18, -125), ("Iso dos", 25, 55)])
print("apercus ecrits")
