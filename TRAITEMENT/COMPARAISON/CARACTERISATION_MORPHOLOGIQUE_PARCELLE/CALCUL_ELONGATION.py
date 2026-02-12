from qgis.core import QgsField, QgsProject, QgsWkbTypes, edit
from PyQt5.QtCore import QVariant

# --- CONFIGURATION ---
# Nom de votre couche de parcelles
layer_name = 'PARCELLE_SIMPLIFIE' 

layers = QgsProject.instance().mapLayersByName(layer_name)

if not layers:
    print(f"❌ Erreur : La couche '{layer_name}' est introuvable.")
else:
    layer = layers[0]
    
    # 1. Ajout du champ ELONG (Double) s'il n'existe pas
    if layer.fields().indexFromName('ELONG') == -1:
        layer.dataProvider().addAttributes([QgsField('ELONG', QVariant.Double, 'Double', 10, 3)])
        layer.updateFields()
    
    idx_elong = layer.fields().indexFromName('ELONG')
    
    # 2. Calcul du rapport Longueur / Largeur
    layer.startEditing()
    
    for feature in layer.getFeatures():
        geom = feature.geometry()
        if geom.isEmpty():
            continue

        # On calcule le rectangle orienté minimal 
        # Cette méthode renvoie (Geometry, area, angle, width, height)
        obb_geom, obb_area, obb_angle, obb_width, obb_height = geom.orientedMinimumBoundingBox()
        
        # Le rapport longueur/largeur doit être >= 1
        # On divise la plus grande dimension par la plus petite
        if obb_width > 0 and obb_height > 0:
            longueur = max(obb_width, obb_height)
            largeur = min(obb_width, obb_height)
            elong_ratio = longueur / largeur
        else:
            elong_ratio = 1.0

        layer.changeAttributeValue(feature.id(), idx_elong, round(elong_ratio, 3))
    
    layer.commitChanges()
    layer.triggerRepaint()
    print(f"✅ Calcul de l'élongation terminé pour la couche '{layer_name}'.")