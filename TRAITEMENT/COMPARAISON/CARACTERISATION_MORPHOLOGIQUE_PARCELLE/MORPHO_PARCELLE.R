# Installation et chargement des packages
if(!require(FactoMineR)) install.packages("FactoMineR")
if(!require(factoextra)) install.packages("factoextra") 
library(FactoMineR)
library(factoextra)
library(dplyr)       

# Chargement des données 
df <- read.csv("PARCELLE_SIMPLIFIE.csv", header=TRUE, sep=";")

# Sélection des variables quantitatives uniquement pour l'ACP
# (Nseg, N50, P2, SURF_HA, PERIM_M, PSI,)
data_pca <- df[, c("Nseg", "N50", "ELONG", "SURFACE", "PERIMETRE", "PSI")]

# Réalisation de l'ACP Normée
res.pca <- PCA(data_pca, scale.unit = TRUE, graph = FALSE)

# Visualisation du cercle des corrélations
fviz_pca_var(res.pca, col.var = "contrib", 
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE) # Évite le chevauchement du texte

# Contribution des variables aux axes principaux
fviz_contrib(res.pca, choice = "var", axes = 1) # top 10 variables sur axe 1
fviz_contrib(res.pca, choice = "var", axes = 2)
fviz_contrib(res.pca, choice = "var", axes = 3)

fviz_eig(res.pca, addlabels = TRUE) +
  geom_hline(yintercept = (1/ncol(data_pca))*100, linetype = "dashed", color = "red") +
  labs(title = "Éboulis des valeurs propres", subtitle = "La ligne rouge indique le seuil moyen (Inertie = 1)")

# 1. On récupère les valeurs propres
eigenvalues <- res.pca$eig[, 1]

# 2. On compte combien d'axes ont une valeur > 1
nb_axes_gardes <- sum(eigenvalues > 1)
print(paste("Nombre d'axes avec inertie > 1 :", nb_axes_gardes))

# 3. On extrait les coordonnées uniquement pour ces axes
coords_finales <- as.data.frame(res.pca$ind$coord[, 1:nb_axes_gardes])

# Extraction des coordonnées des 6 792 polygones sur les axes principaux
coords_polygones <- as.data.frame(res.pca$ind$coord)

# Fusion avec le jeu de données initial (pour garder les identifiants)
# On ajoute une colonne ID basée sur les noms de lignes pour la fusion
coords_finales$ID_JOIN <- row.names(coords_finales)
df$ID_JOIN <- row.names(df)

# jointure SQL sur la base de "ID_JOIN"
df_final <- merge(df, coords_finales, by = "ID_JOIN")

### CAH
data_for_clustering <- df_final[, c("Dim.1", "Dim.2", "Dim.3")]

# 4. Calcul de la matrice des distances (Euclidienne)
d <- dist(data_for_clustering, method = "euclidean")

# 5. Application de la méthode de Ward (Ward.D2 est la version standardisée)
res.cah <- hclust(d, method = "ward.D2")

# 6. Visualisation du dendrogramme pour choisir le nombre de clusters
plot(res.cah, labels = FALSE, main = "Dendrogramme de la morphologie")
# Pour voir les sauts d'inertie (les hauteurs des branches) :
plot(rev(res.cah$height)[1:10], type="b", main="Sauts d'inertie")

# On définit le nombre de groupes souhaité (ex: 4)
nb_clusters <- 6

# On récupère le numéro de cluster pour chaque polygone
clusters <- cutree(res.cah, k = nb_clusters)

# On ajoute cette information dans votre dataframe principal
df_final$CLUSTER <- as.factor(clusters)

# Calcul des moyennes des variables initiales par cluster
profil_clusters <- df_final %>%
  group_by(CLUSTER) %>%
  summarise(
    Moy_perimetre = mean(PERIMETRE),
    Moy_Surface = mean(SURFACE),
    Moy_PSI = mean(PSI),
    Moy_Nseg = mean(Nseg),
    Moy_N50 = mean(N50),
    Moy_ELONG = mean(ELONG),
    Effectif = n()
  )

# Sauvegarde en CSV
write.csv(df_final, "typologie_morphologique_finale_2.csv", row.names = TRUE)

