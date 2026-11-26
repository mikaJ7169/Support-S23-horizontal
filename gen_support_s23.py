#!/usr/bin/env python3
"""
Support horizontal (paysage) pour Samsung Galaxy S23 -> STL (mm).  v4 (reprise a zero)

Design monolithique en L (style mini-ecran) :
  - embase plate arrondie au sol
  - panneau arriere incline de TILT degres vers l'arriere, solidaire du berceau
  - berceau en haut : le telephone est insere par le dessus, "anglobe"
    (fond + parois + baguette frontale de 3 mm) -> seul l'ecran est visible
  - bas du telephone a RAISE mm du sol ; le cable USB passe sous le support

Cotes officielles Galaxy S23 : 146.3 x 70.9 x 7.6 mm, ecran 6.1" 2340x1080
(19.5:9) = 140.7 x 64.9 mm, coins du chassis ~ r11 mm, coins d'ecran ~ r8 mm.
Layout : USB-C au centre du bord inferieur, boutons volume+power sur le bord
droit (partie haute), SIM + enceinte sur le bord inferieur, micro en haut,
capteurs photo en haut a gauche du dos.

Repere local (avant inclinaison) : X = longueur du tel (+X = GAUCHE vue de
l'ecran = cote USB-C), Y = epaisseur (ecran vers +Y), Z = largeur du tel,
le seuil (le tel repose dessus) est le plan Z=0.
"""

import numpy as np
import trimesh
from trimesh.creation import box as tbox, extrude_polygon
from trimesh.transformations import translation_matrix, rotation_matrix
from shapely.geometry import box as sbox

# ---------------- Telephone (mm) ----------------
PHONE_L, PHONE_W, PHONE_T = 146.3, 70.9, 7.6
R_PHONE = 11.0

# ---------------- Parametres (mm / deg) ----------------
CLEAR  = 0.5
WALL   = 4.0
BACK   = 5.0          # paroi de fond du berceau
LIP    = 3.0          # baguette frontale
RAISE  = 80.0         # bas du telephone au-dessus du sol
TILT   = 10.0         # inclinaison vers l'arriere
R_CAV  = R_PHONE + 1.5
R_WIN  = 9.0
R_BODY = 6.0
ZB     = -90.0        # base du panneau en local (coupee au sol ensuite)

cav_x = PHONE_L + 2 * CLEAR          # 147.3
cav_y = PHONE_T + 2 * CLEAR          # 8.6
body_x = cav_x + 2 * WALL            # 155.3
body_y = BACK + cav_y + 4.0          # 17.6 (baguette 4 mm)
body_z0, body_z1 = -8.0, 78.0        # paroi basse (seuil) + hauteur des parois
zc = (body_z0 + body_z1) / 2
win_x = cav_x - 2 * LIP              # 141.3


def rrect(w, h, r):
    r = min(r, w / 2, h / 2)
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


def rounded_box(sx, sy, sz, r, center):
    cx, cy, cz = center
    parts = [
        bbox(cx - sx / 2 + r, cx + sx / 2 - r, cy - sy / 2 + r, cy + sy / 2 - r, cz - sz / 2 + r, cz + sz / 2 - r),
        bbox(cx - sx / 2, cx + sx / 2, cy - sy / 2 + r, cy + sy / 2 - r, cz - sz / 2 + r, cz + sz / 2 - r),
        bbox(cx - sx / 2 + r, cx + sx / 2 - r, cy - sy / 2, cy + sy / 2, cz - sz / 2 + r, cz + sz / 2 - r),
        bbox(cx - sx / 2 + r, cx + sx / 2 - r, cy - sy / 2 + r, cy + sy / 2 - r, cz - sz / 2, cz + sz / 2),
    ]
    from trimesh.creation import cylinder, icosphere
    # aretes selon X
    for yy in (-1, 1):
        for zz in (-1, 1):
            c = cylinder(radius=r, height=sx - 2 * r, sections=64)
            c.apply_transform(rotation_matrix(np.pi / 2, [0, 1, 0]))
            c.apply_translation([cx, cy + yy * (sy / 2 - r), cz + zz * (sz / 2 - r)])
            parts.append(c)
    for xx in (-1, 1):
        for zz in (-1, 1):
            c = cylinder(radius=r, height=sy - 2 * r, sections=64)
            c.apply_translation([cx + xx * (sx / 2 - r), cy, cz + zz * (sz / 2 - r)])
            parts.append(c)
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


# ---------------- Partie haute (repere local, vertical) ----------------
body = rounded_box(body_x, body_y, body_z1 - body_z0, R_BODY, (0, body_y / 2, (body_z0 + body_z1) / 2))
panel = prism_xz(rrect(body_x, body_z1 - ZB, 8.0), -6.0, 0.5, zc=(body_z1 + ZB) / 2)  # panneau arriere
upper = trimesh.boolean.union([body, panel], engine="manifold")

cav_h = body_z1                      # cavite ouverte en haut : Z = 0..78
win_z0 = LIP                         # fenetre : Z = 3..79 (ouverte en haut)
cuts = [
    prism_xz(rrect(cav_x, cav_h, R_CAV), BACK, BACK + cav_y, zc=cav_h / 2),                    # cavite, coins arrondis comme le tel
    prism_xz(rrect(win_x, body_z1 + 1 - win_z0, R_WIN), body_y - 4.2, body_y + 1.0, zc=(win_z0 + body_z1 + 1) / 2),  # fenetre ecran (coupe la baguette frontale)
    prism_xz(rrect(7.0, 44.0, 3.2), -1.0, body_y + 1.0, xc=body_x / 2 - 3.25, zc=34.0),        # fente USB-C / SIM / enceinte, paroi +X (gauche vue de l'ecran)
    prism_xz(rrect(67.0, 10.0, 3.2), -1.0, body_y + 1.0, xc=-43.5, zc=body_z0 + 5.0),         # logement boutons volume/power, paroi basse cote -X
    prism_xz(rrect(7.0, 8.0, 3.0), -1.0, body_y + 1.0, xc=-body_x / 2 + 3.25, zc=36.0),        # micro du bord superieur, paroi -X
    bbox(-cav_x / 2, -40.0, BACK - 2.6, BACK + 0.2, 0.0, 16.0),                                 # poche capteurs photo, coin (-X, bas)
    prism_xz(rrect(116.0, 55.0, 12.0), -7.0, 1.0, xc=0.0, zc=-52.5),                            # fenetre d'alleegement du panneau arriere
]
upper = trimesh.boolean.difference([upper] + cuts, engine="manifold")

# ---------------- Inclinaison + hauteur ----------------
rot = rotation_matrix(np.radians(TILT), [1, 0, 0], point=[0, 0, ZB])
upper.apply_transform(rot)

phone_local = prism_xz(rrect(PHONE_L, PHONE_W, R_PHONE), BACK + CLEAR, BACK + CLEAR + PHONE_T, zc=CLEAR + PHONE_W / 2)
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
upper = trimesh.boolean.difference([upper, bbox(-300, 300, -300, 300, -100, 0.0)], engine="manifold")

# ---------------- Embase horizontale (monde) ----------------
plinth = prism_xy(rrect(160.0, 64.0, 10.0), 0.0, 6.0, xc=0.0, yc=-20.0)
mesh = trimesh.boolean.union([upper, plinth], engine="manifold")
mesh.merge_vertices()

# ---------------- Validation ----------------
print("watertight :", mesh.is_watertight)
print("winding ok :", mesh.is_winding_consistent)
print("corps      :", mesh.body_count)
print("volume     : %.1f cm3" % (mesh.volume / 1000.0))
print("dimensions : %.1f x %.1f x %.1f mm" % tuple(mesh.extents))
print("zmin       : %.2f mm" % mesh.bounds[0][2])
print("inclinaison: %.0f deg" % TILT)
print("bas du tel au sol : %.2f mm" % phone_w.bounds[0][2])

tests = {
    "telephone (coins r11)": phone_w,
    "boutons":   to_world(bbox(-72.0, -20.0, BACK + CLEAR, BACK + CLEAR + PHONE_T, -1.2, CLEAR)),
    "fiche USB": to_world(bbox(PHONE_L / 2 - 0.15, PHONE_L / 2 + 8.0, BACK + CLEAR, BACK + CLEAR + PHONE_T, 30.0, 42.0)),
    "cable sous le support": to_world(bbox(-20.0, 20.0, 6.0, 12.0, -40.0, -20.0)),
}
for name, t in tests.items():
    inter = trimesh.boolean.intersection([mesh, t], engine="manifold")
    print("collision %-22s : %.3f mm3 (attendu 0)" % (name, inter.volume if inter is not None else 0.0))

probes = {
    "fenetre (vide)":        ((0, 15.0, 36.0), (10, 2, 10), 0),
    "baguette (plein)":      ((0, 15.0, 1.5), (10, 2, 2), 40),
    "cavite (vide)":         ((0, 9.0, 36.0), (10, 2, 10), 0),
    "fond berceau (plein)":  ((0, 2.5, 36.0), (10, 2, 10), 200),
    "paroi +X au-dessus fente (plein)": ((body_x / 2 - 2.0, 9.0, 65.0), (2, 8, 6), 96),
    "fente USB (vide)":      ((body_x / 2 - 2.0, 9.0, 34.0), (2, 8, 20), 0),
    "logement boutons (vide)": ((-40.0, 9.0, -4.0), (10, 8, 4), 0),
    "seuil (plein)":         ((30.0, 9.0, -4.0), (10, 8, 4), 320),
    "panneau arriere (plein)": ((0, -3.0, -50.0), (10, 2, 10), 0),  # dans la fenetre d'alleegement -> vide
    "panneau bord (plein)":  ((70.0, -3.0, -50.0), (10, 2, 10), 200),
    "embase (plein)":        ((0, -20.0, 3.0), (10, 8, 4), 320),
    "sous le berceau (vide)": ((0, 9.0, -40.0), (10, 8, 20), 0),
    "poche capteurs (vide)": ((-60.0, 3.8, 8.0), (10, 1.5, 8), 0),
}
for name, (c, s, expect) in probes.items():
    t = to_world(bbox(c[0] - s[0] / 2, c[0] + s[0] / 2, c[1] - s[1] / 2, c[1] + s[1] / 2, c[2] - s[2] / 2, c[2] + s[2] / 2))
    inter = trimesh.boolean.intersection([mesh, t], engine="manifold")
    v = inter.volume if inter is not None else 0.0
    ok = "OK" if (v < 1e-6) == (expect == 0) else "ERREUR"
    print("sonde %-32s : %.1f mm3 (attendu %s) %s" % (name, v, expect, ok))

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
    fig = plt.figure(figsize=(5.0 * len(views), 6.0))
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
       [("Face ecran (USB a gauche)", 0, 90), ("Profil (inclinaison)", 0, 0), ("Fente USB 3/4", 10, -30), ("Dos", 0, -90), ("Dessus", 90, 90)])
render([(mesh, "#9fc3e8"), (phone_w, "#e8c39f")], "/workspace/preview_iso.png",
       [("Iso face+gauche, tel insere", 14, 55), ("Iso profil, tel insere", 3, 85), ("Iso dos", 20, 235)])
print("apercus ecrits")
