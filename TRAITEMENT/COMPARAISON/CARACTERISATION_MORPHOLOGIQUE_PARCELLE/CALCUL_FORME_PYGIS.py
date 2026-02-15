from qgis.core import QgsField, QgsProject, QgsWkbTypes, edit
from PyQt5.QtCore import QVariant
import math

# --- CONFIGURATION ---
# Remplacez 'MA_COUCHE_PARCELLES' par le nom exact de votre couche
nom_de_votre_couche = 'PARCELLE_SIMPLIFIE' 

# 1. Récupération de la couche par son nom
layers = QgsProject.instance().mapLayersByName(nom_de_votre_couche)

if not layers:
    print(f"ERREUR : La couche '{nom_de_votre_couche}' est introuvable dans le projet.")
else:
    layer = layers[0]
    
    if layer.geometryType() != QgsWkbTypes.PolygonGeometry:
        print(f"ERREUR : La couche '{nom_de_votre_couche}' n'est pas une couche de polygones.")
    else:
        # 2. Préparation des nouveaux champs
        new_fields = [
            QgsField("SURFACE", QVariant.Double,"Double", 20, 5 ),
            QgsField("PERIMETRE", QVariant.Double, "Double", 15, 2),
            QgsField("Nseg", QVariant.Int),
            QgsField("N50", QVariant.Int),
        ]
        
        # Ajout des champs s'ils n'existent pas
        layer.startEditing()
        for field in new_fields:
            if layer.fields().indexFromName(field.name()) == -1:
                layer.addAttribute(field)
        layer.commitChanges() 
        
        # Récupération des index
        f = layer.fields()
        idxs = {field.name(): f.indexFromName(field.name()) for field in new_fields}

        # 3. Calcul des indicateurs
        try:
            with edit(layer):
                for feature in layer.getFeatures():
                    geom = feature.geometry()
                    if geom.isEmpty():
                        continue

                    # --- Géométrie de base ---
                    area_m2 = geom.area()
                    area_ha = area_m2 / 10000.0
                    
                    # Extraction des segments
                    vertices = [v for v in geom.vertices()]
                    lengths = []
                    for i in range(len(vertices) - 1):
                        d = vertices[i].distance(vertices[i+1])
                        if d > 0.0001:
                            lengths.append(d)
                    
                    total_perim = sum(lengths)
                    if total_perim <= 0 or area_m2 <= 0:
                        continue
                        
                    # --- Indicateurs ---
                    n_seg = len(lengths)
                    
                    # N50
                    sorted_segs = sorted(lengths, reverse=True)
                    cumul, n_50, target = 0, 0, total_perim / 2.0
                    for s in sorted_segs:
                        cumul += s
                        n_50 += 1
                        if cumul >= target:
                            break

                    # Mise à jour
                    layer.changeAttributeValues(feature.id(), {
                        idxs["Nseg"]: n_seg,
                        idxs["N50"]: n_50,
                        idxs["SURFACE"]: round(area_ha, 5),
                        idxs["PERIMETRE"]: round(total_perim, 2),
                    })
            print(f"Traitement de la couche '{nom_de_votre_couche}' terminé avec succès.")
            
        except Exception as e:
            print(f"Erreur lors de l'édition : {e}")
            layer.rollBack()