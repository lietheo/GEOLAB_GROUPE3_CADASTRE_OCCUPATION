# Mise à jour de l’attribut occupation des sols de la base de données cadastrales

## Présentation du projet
Ce dépôt regroupe les travaux relatifs à l'automatisation de la mise à jour de l'occupation des sols (OCS) au sein du cadastre français. L'étude propose un protocole de fusion multi-source intégrant des données de télédétection (IA) et des référentiels vectoriels institutionnels pour améliorer la précision de l'information géographique à l'échelle parcellaire.

## Contenu du dépôt
Le projet est structuré autour de quatre composantes principales :

* **Scripts Python :** Codes sources documentés et commentés assurant l'intégralité de la chaîne de traitement, du prétraitement des données à la production des indices de confiance.
* **Géo-visualisation :** Interface interactive permettant l'exploration spatiale des résultats et la confrontation des différentes méthodes de classification.
* **Résultats :** Sorties de données au format CSV et productions cartographiques synthétisant les classifications obtenues et les indicateurs de fiabilité.
* **Article scientifique :** Documentation complète détaillant le contexte, la méthodologie de recherche, l'analyse des résultats et les conclusions de l'étude.

## Méthodologie
Le processus repose sur l'harmonisation de nomenclatures hétérogènes et l'application de modèles d'arbitrage (scoring décisionnel et arbres de décision). Un indice de confiance est calculé pour chaque unité foncière afin de qualifier la robustesse de la classification finale.

## Accès à la Géo-visualisation
L'interface de visualisation est accessible via le lien suivant :
[Consulter la GeoViz](https://github.com/lietheo/GEOLAB_GROUPE3_CADASTRE_OCCUPATION)

## Auteurs
S. Mercier, M. Uozumi, A. Sery, T. Liegeon.
Master II Observation de la Terre et Géomatique (OTG), Université de Strasbourg (2026).
