# scrapping_lyrics

# Analyseur de Paroles
Ce script Python est conçu pour analyser les paroles des chansons d'un artiste spécifique. Il récupère les paroles depuis un site web, les nettoie et produit une liste des mots les plus fréquemment utilisés par l'artiste. Ici, l'artiste ciblé est Patrick Bruel, son numéro dans l'api genius est 29743. Il suffit de changer le numéro de l'artiste pour utiliser le script sur l'artiste que l'on souhaite.

## Fonctions

### 'get_all_urls()' Cette fonction récupère toutes les URLs des chansons d'un artiste depuis l'API Genius. Elle retourne une liste d'URLs pointant vers les paroles de chaque chanson.

### 'extract_lyrics(url)' Prend en entrée une URL de chanson et extrait les paroles brutes du site web. Elle retourne les paroles sous forme de chaîne de caractères.

### 'get_clean_lyrics(list_words, word_length=2)' Transforme les paroles brutes en une liste de mots nettoyés. Elle prend en compte la longueur des mots et exclut les mots trop courts ou non pertinents.

### 'remove_words(original_word, word_to_remove)' Supprime les mots banals et non significatifs de la liste des mots. Elle utilise une liste prédéfinie de mots à exclure.

### 'get_all_clean_lyrics()' Combine les fonctions précédentes pour obtenir une liste nettoyée de tous les mots utilisés dans les paroles de toutes les chansons de l'artiste.

### 'print_full_lyrics(top_word=10)' Affiche les mots les plus fréquemment utilisés par l'artiste. Le nombre de mots affichés peut être ajusté.

## Pour utiliser ce script, exécutez simplement la commande suivante dans votre terminal :
python3 main.py
