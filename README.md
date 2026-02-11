# Mise à jour de l’attribut occupation des sols de la base de données cadastrales

![Licence](https://img.shields.io/badge/Licence-MIT-yellow)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB)
![Plateforme](https://img.shields.io/badge/Visualisation-GitHub--Pages-blue)

---

## Présentation du projet
Ce dépôt regroupe les travaux relatifs à l'automatisation de la mise à jour de l'occupation des sols (OCS) au sein du cadastre français. L'étude propose un protocole de fusion multi-source intégrant des données de télédétection (IA) et des référentiels vectoriels institutionnels pour améliorer la précision de l'information géographique à l'échelle parcellaire.

## Contenu du dépôt
Le projet est structuré autour de quatre composantes principales :

| Composante | Description |
| :--- | :--- |
| **Scripts Python** | Codes sources documentés assurant la chaîne de traitement, du prétraitement à la production des indices de confiance. |
| **Géo-visualisation** | Interface interactive déployée permettant l'exploration spatiale des résultats. |
| **Résultats** | Sorties de données au format CSV et productions cartographiques (atlas et couches géographiques). |
| **Article scientifique** | Documentation complète détaillant le contexte, la méthodologie, l'analyse des résultats et les conclusions. |

---

## Méthodologie
Le processus repose sur l'harmonisation de nomenclatures hétérogènes et l'application de modèles d'arbitrage (scoring décisionnel et arbres de décision). 

> **Qualification de la donnée** : Un indice de confiance est calculé pour chaque unité foncière afin d'évaluer la robustesse de la classification finale.

---

## Accès aux ressources

### Interface de Géo-visualisation
L'interface interactive de consultation des résultats est accessible directement via le lien suivant :  
[**Accéder à la Géo-visualisation interactive**](https://lietheo.github.io/GEOLAB_GROUPE3_CADASTRE_OCCUPATION/)


---

## Licence
Ce projet est sous licence **MIT**. Consulter le fichier `LICENSE` pour les conditions de réutilisation.

---

## Auteurs
**S. Mercier, M. Uozumi, A. Sery, T. Liegeon.** *Master II Observation de la Terre et Géomatique (OTG), Université de Strasbourg (2025-2026).*
