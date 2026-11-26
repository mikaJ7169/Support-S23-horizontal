#!/usr/bin/env python3
"""
Support horizontal (paysage) pour Samsung Galaxy S23 -> STL (mm).  v3

Cotes officielles Galaxy S23 : 146.3 x 70.9 x 7.6 mm, ecran 6.1" 2340x1080
(19.5:9), coins du chassis ~ r11 mm (design identique au S22).
Layout : USB-C au centre du bord inferieur, boutons volume + power sur le bord
droit (partie haute), tiroir SIM + enceinte sur le bord inferieur, micro sur le
bord superieur, capteurs photo en haut a gauche du dos.

v3 :
  - en regardant l'ECRAN, le port USB-C est a GAUCHE du support (+X)
  - le berceau est incline de 10 deg vers l'arriere -> le telephone repose
    contre le fond et ne peut pas tomber vers l'avant
  - le bas du telephone est a 80 mm du sol, le cable USB peut passer SOUS
  - la cavite a des coins arrondis (r12.5) qui suivent la courbe du telephone
  - insertion du telephone par le dessus (ouverture superieure)
  - corps/colonnes/embase entierement arrondis (aucun coin saillant)

Repere local avant inclinaison : X = longueur du tel, Y = epaisseur (ecran
vers +Y), Z = largeur du tel. +X = cote USB-C = GAUCHE vue de l'ecran.
"""

import numpy as np
import trimesh
from trimesh.creation import box as tbox, cylinder, icosphere, extrude_polygon
from trimesh.transformations import translation_matrix, rotation_matrix
from shapely.geometry import box as sbox

# ---------------- Telephone (mm) ----------------
PHONE_L = 146.3
PHONE_W = 70.9
PHONE_T = 7.6
R_PHONE = 11.0     # rayon des coins du chassis

# ---------------- Parametres (mm / deg) ----------------
CLEAR  = 0.5
WALL   = 4.0
BACK   = 5.0
LIP_T  = 4.0
LIP    = 3.0
BOT    = 6.0       # epaisseur du seuil
RAISE  = 80.0      # hauteur du bas du telephone au-dessus du sol
TILT   = 10.0      # inclinaison vers l'arriere
FOOT_D = 34.0
COL_W  = 20.0
ZB     = -90.0    # base des colonnes en repere local (sera coupee au niveau du sol)
R_BODY = 6.0
R_CAV  = R_PHONE + 1.5   # 12.5 : suit la courbe des coins du tel
R_WIN  = 9.0             # coins de la fenetre (coins de l'ecran ~ r8)

cav_x = PHONE_L + 2 * CLEAR            # 147.3
cav_y = PHONE_T + 2 * CLEAR            # 8.6
cav_z = PHONE_W + 2 * CLEAR            # 71.9
body_x = cav_x + 2 * WALL              # 155.3
body_y = BACK + cav_y + LIP_T          # 17.6
body_z = BOT + cav_z + WALL            # 81.9
zc = BOT + cav_z / 2                   # 41.95 centre de la cavite
win_x = cav_x - 2 * LIP                # 141.3


def rrect(w, h, r):
    return sbox(-w / 2, -h / 2, w / 2, h / 2).buffer(r, join_style=1).buffer(-r, join_style=1)


def prism_xz(poly, y0, y1, xc=0.0, zc=0.0):
    m = extrude_polygon(poly, y1 - y0)
    m.apply_transform(rotation_matrix(-np.pi / 2, [1, 0, 0]))
    m.apply_translation([xc, y0, zc])
    return m


def prism_xy(poly, z0, z1, xc=0.0, yc=0.0):
    m = extrude_polygon(poly, z1 - z0)
    m.apply_translation([xc, yc, z0])
    return m


def bbox(x0, x1, y0, y1, z0, z1):
    c = [(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]
    return tbox(extents=[x1 - x0, y1 - y0, z1 - z0], transform=translation_matrix(c))


def cyl_x(r, length, y, z):
    c = cylinder(radius=r, height=length, sections=64)
    c.apply_transform(rotation_matrix(np.pi / 2, [0, 1, 0]))
    c.apply_translation([0, y, z])
    return c


def cyl_y(r, length, x, z, yc=0.0):
    c = cylinder(radius=r, height=length, sections=64)
    c.apply_transform(rotation_matrix(np.pi / 2, [1, 0, 0]))
    c.apply_translation([x, yc, z])
    return c


def rounded_box(sx, sy, sz, r, center):
    cx, cy, cz = center
    parts = [
        bbox(cx - sx / 2 + r, cx + sx / 2 - r, cy - sy / 2 + r, cy + sy / 2 - r, cz - sz / 2 + r, cz + sz / 2 - r),
        bbox(cx - sx / 2, cx + sx / 2, cy - sy / 2 + r, cy + sy / 2 - r, cz - sz / 2 + r, cz + sz / 2 - r),
        bbox(cx - sx / 2 + r, cx + sx / 2 - r, cy - sy / 2, cy + sy / 2, cz - sz / 2 + r, cz + sz / 2 - r),
        bbox(cx - sx / 2 + r, cx + sx / 2 - r, cy - sy / 2 + r, cy + sy / 2 - r, cz - sz / 2, cz + sz / 2),
    ]
    for yy in (-1, 1):
        for zz in (-1, 1):
            parts.append(cyl_x(r, sx - 2 * r, cy + yy * (sy / 2 - r), cz + zz * (sz / 2 - r)))
    for xx in (-1, 1):
        for zz in (-1, 1):
            parts.append(cyl_y(r, sy - 2 * r, cx + xx * (sx / 2 - r), cz + zz * (sz / 2 - r), yc=cy))
    for xx in (-1, 1):
        for yy in (-1, 1):
            c = cylinder(radius=r, height=sz - 2 * r, sections=64)
            c.apply_translation([cx + xx * (sx / 2 - r), cy + yy * (sy / 2 - r), cz])
            parts.append(c)
    for xx in (-1, 1):
        for yy in (-1, 1):
            for zz in (-1, 1):
                parts.append(icosphere(subdivisions=2, radius=r).apply_translation(
                    [cx + xx * (sx / 2 - r), cy + yy * (sy / 2 - r), cz + zz * (sz / 2 - r)]))
    return trimesh.boolean.union(parts, engine="manifold")


# ---------------- Berceau (repere local, vertical) ----------------
body = rounded_box(body_x, body_y, body_z, R_BODY, (0, body_y / 2, body_z / 2))
col_xc = body_x / 2 - COL_W / 2
cols = [prism_xy(rrect(COL_W, body_y, 4.0), ZB, body_z, xc=s * col_xc, yc=body_y / 2) for s in (-1, 1)]
upper = trimesh.boolean.union([body] + cols, engine="manifold")

cav_h = body_z + 1.0 - BOT                     # cavite ouverte en haut : Z = BOT..body_z+1
win_h = body_z + 1.0 - (BOT + LIP)             # fenetre ouverte en haut : Z = BOT+LIP..body_z+1
cuts = [
    prism_xz(rrect(cav_x, cav_h, R_CAV), BACK, BACK + cav_y, zc=BOT + cav_h / 2),                      # cavite, coins arrondis comme le tel
    prism_xz(rrect(win_x, win_h, R_WIN), BACK + cav_y - 0.2, body_y + 1.0, zc=BOT + LIP + win_h / 2),   # fenetre ecran
    bbox(body_x / 2 - 5.0, body_x / 2 + 1.0, -1.0, body_y + 1.0, BOT, BOT + 48.0),                      # ouverture USB-C, paroi +X (gauche vue de l'ecran)
    bbox(55.0, body_x / 2, -1.0, body_y + 1.0, -1.0, BOT + 1.0),                                        # canal pour le cable sous le telephone
    bbox(-body_x / 2 + 1.0, -10.0, -1.0, body_y + 1.0, -1.0, BOT + 0.2),                                # logement boutons volume/power (paroi basse, cote -X)
    bbox(-body_x / 2 - 1.0, -body_x / 2 + 5.0, -1.0, body_y + 1.0, zc - 4.0, zc + 4.0),                 # micro du bord superieur (paroi -X)
    bbox(-cav_x / 2, -40.0, BACK - 2.6, BACK + 0.2, BOT, BOT + 16.0),                                   # poche capteurs photo, coin (-X, bas) du fond
]
upper = trimesh.boolean.difference([upper] + cuts, engine="manifold")

# ---------------- Inclinaison + mise a hauteur ----------------
rot = rotation_matrix(np.radians(TILT), [1, 0, 0], point=[0, 0, ZB])  # pivot a la base : le haut bascule vers l'arriere, la base reste au sol
upper.apply_transform(rot)

phone_local = prism_xz(rrect(PHONE_L, PHONE_W, R_PHONE), BACK + CLEAR, BACK + CLEAR + PHONE_T, zc=BOT + CLEAR + PHONE_W / 2)  # coins arrondis dans le plan de l'ecran
phone_r = phone_local.copy()
phone_r.apply_transform(rot)
Tz = RAISE - phone_r.bounds[0][2]
upper.apply_translation([0, 0, Tz])


def to_world(m):
    m2 = m.copy()
    m2.apply_transform(rot)
    m2.apply_translation([0, 0, Tz])
    return m2


phone_w = to_world(phone_local)

# decoupe au niveau du sol (les colonnes atteignent le plateau a plat)
upper = trimesh.boolean.difference([upper, bbox(-300, 300, -300, 300, -100, 0.0)], engine="manifold")

# ---------------- Embase horizontale ----------------
foot = prism_xy(rrect(body_x, FOOT_D + BACK + 1.0, 8.0), 0.0, BOT, xc=0.0, yc=(BACK + 1.0 - FOOT_D) / 2)
foot_f = [
    cyl_x(3.0, 2 * (body_x / 2 - 8.0), -FOOT_D + 3.0, BOT - 3.0),
    cyl_y(3.0, FOOT_D - 8.0, -(body_x / 2 - 3.0), BOT - 3.0, yc=-(FOOT_D - 8.0) / 2),
    cyl_y(3.0, FOOT_D - 8.0, +(body_x / 2 - 3.0), BOT - 3.0, yc=-(FOOT_D - 8.0) / 2),
]

mesh = trimesh.boolean.union([upper, foot] + foot_f, engine="manifold")
mesh.merge_vertices()

# ---------------- Validation ----------------
print("watertight :", mesh.is_watertight)
print("winding ok :", mesh.is_winding_consistent)
print("corps      :", mesh.body_count)
print("volume     : %.1f cm3" % (mesh.volume / 1000.0))
print("dimensions : %.1f x %.1f x %.1f mm" % tuple(mesh.extents))
print("inclinaison: %.0f deg vers l'arriere" % TILT)
print("bas du tel au sol : %.2f mm" % phone_w.bounds[0][2])

tests = {
    "telephone (coins r11)": phone_w,
    "boutons":  to_world(bbox(-72.0, -20.0, BACK + CLEAR, BACK + CLEAR + PHONE_T, BOT - 1.2, BOT + CLEAR)),
    "fiche USB": to_world(bbox(PHONE_L / 2 - 0.15, PHONE_L / 2 + 8.0, BACK + CLEAR, BACK + CLEAR + PHONE_T, zc - 6.0, zc + 6.0)),
    "cable sous tel": to_world(bbox(58.0, 73.0, BACK + CLEAR, BACK + CLEAR + PHONE_T, 0.5, BOT - 0.5)),
}
for name, t in tests.items():
    inter = trimesh.boolean.intersection([mesh, t], engine="manifold")
    print("collision %-20s : %.3f mm3 (attendu 0)" % (name, inter.volume if inter is not None else 0.0))

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
    fig = plt.figure(figsize=(5.2 * len(views), 6.0))
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


render([(mesh, "#9fc3e8")], "/workspace/preview_ortho.png",
       [("Face ecran (USB a gauche)", 0, 90), ("Profil (inclinaison)", 0, 0), ("Paroi USB 3/4", 8, -30), ("Dos", 0, -90), ("Dessus", 90, 90)])
render([(mesh, "#9fc3e8"), (phone_w, "#e8c39f")], "/workspace/preview_iso.png",
       [("Iso face+USB, tel insere", 14, 55), ("Iso profil, tel insere", 4, 80), ("Iso dos", 20, 235)])
print("apercus ecrits")
