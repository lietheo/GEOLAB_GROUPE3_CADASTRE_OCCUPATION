import math
from qgis.core import *
from PyQt5.QtCore import QVariant

def calculate_psi(feature):
    geom = feature.geometry()
    if geom.isEmpty():
        return 0.0
    
    # --- FONCTION INTERNE POUR CALCULER SUR UN POLYGONE SIMPLE ---
    def process_single_geom(g):
        # g doit être un objet QgsGeometry
        area = g.area()
        perimeter = g.length()
        
        # Récupération sécurisée des sommets (marche pour Polygon et MultiPolygon)
        vertices = [v for v in g.vertices()]
        n_vertices = len(vertices)
        
        if area <= 0 or n_vertices < 3:
            return 0.0
        
        # Compacité
        compactness = 4 * math.pi * area / (perimeter ** 2) if perimeter > 0 else 0
        
        # Rectangularité
        bbox = g.boundingBox()
        bbox_area = bbox.width() * bbox.height()
        rectangularity = area / bbox_area if bbox_area > 0 else 0
        
        # Longueur moyenne côtés
        side_lengths = []
        for i in range(len(vertices) - 1):
            side_lengths.append(vertices[i].distance(vertices[i+1]))
        
        mean_side = sum(side_lengths) / len(side_lengths) if side_lengths else 0
        var_side = math.sqrt(sum((x - mean_side)**2 for x in side_lengths) / len(side_lengths)) if len(side_lengths) > 1 else 0
        
        # Scores
        score_compact = min(1.0, max(0.0, compactness / 0.8))
        score_rectang = min(1.0, max(0.0, rectangularity / 0.9))
        score_vertices = min(1.0, max(0.0, 20.0 / max(n_vertices, 4)))
        score_sides = min(1.0, max(0.0, 1.0 - var_side / max(mean_side, 1e-6)))
        
        psi = 0.25 * score_compact + 0.20 * score_rectang + 0.20 * score_vertices + 0.20 * score_sides + 0.15 * 0.8
        return psi

    # --- TRAITEMENT SELON TYPE GÉOMÉTRIE ---
    # Si c'est un MultiPolygon (plusieurs parties)
    if geom.isMultipart():
        # On extrait chaque partie comme une géométrie QgsGeometry individuelle
        parts = [QgsGeometry.fromPolygonXY(p) for p in geom.asMultiPolygon()]
        if not parts:
            return 0.0
        # On cherche la géométrie qui a la plus grande aire
        largest_part_geom = max(parts, key=lambda p: p.area())
        return process_single_geom(largest_part_geom)
    else:
        # Polygone simple
        return process_single_geom(geom)

# --- EXECUTION ---
layer_name = "PARCELLE_SIMPLIFIE"
layers = QgsProject.instance().mapLayersByName(layer_name)

if not layers:
    print(f"❌ Couche '{layer_name}' non trouvée !")
else:
    layer = layers[0]
    
    # Ajout du champ s'il n'existe pas
    if layer.fields().indexFromName('PSI') == -1:
        layer.dataProvider().addAttributes([QgsField('PSI', QVariant.Double)])
        layer.updateFields()
    
    idx = layer.fields().indexFromName('PSI')
    layer.startEditing()
    
    for feat in layer.getFeatures():
        psi_value = calculate_psi(feat)
        layer.changeAttributeValue(feat.id(), idx, psi_value)
    
    layer.commitChanges()
    layer.triggerRepaint()
    print(f"✅ PSI calculé sur {layer.featureCount()} parcelles")