from collections import Counter
from bs4 import BeautifulSoup
import requests

BANAL_WORDS = ["", "que", "pas", "les", "des", "qui", "tout", "mais", "dans", "sur", "pour", "plus", "ans"]


def get_all_urls():
    """Description: Permet d'obtenir toutes les urls liées à un artiste.

    Returns: (list) URLs renvoyant les paroles pour chaque chansons.

    """
    page_number = 1
    links = []
    next_page = 1
    while next_page:
        r = requests.get(f"https://genius.com/api/artists/29743/songs?page={page_number}&sort=popularity")
        if r.status_code == 200:
            response = r.json().get("response", {})  # dictionnaire vide si "response" n'est pas trouvé.
            next_page = response.get("next_page")
            songs = response.get("songs")
            links.extend([url.get("url") for url in songs])  # on récupère l'url pour url dans "songs"
            print(f"Fetching page {page_number}.")
            page_number += 1

    return links


def extract_lyrics(url):
    """Description: premet d'extraire les paroles

    Args:
        url: (str) URL ciblée.

    Returns: (str) Paroles brutes.

    """
    print(f"Extracting lyrics {url}...")
    r = requests.get(url)
    if r.status_code != 200:
        print("Couldn't fetch page.")
        return []
    else:
        soup = BeautifulSoup(r.content, "html.parser")  # r.content : contenu de la page en HTML.
        list_html_lyrics = soup.find_all("div", class_="Lyrics__Container-sc-1ynbvzw-1 kUgSbL")  # liste avec les div
        list_generator = [lyric.stripped_strings for lyric in list_html_lyrics]  # liste avec les generators (listes)
        all_lyrics = [" ".join(generator) for generator in list_generator]
        all_lyrics = "\n".join(all_lyrics)
        return all_lyrics


def get_clean_lyrics(list_words, word_length=2):
    """Description: Transformer les str brutes en liste de mots

    Args:
        list_words: (str) Mots brutes.
        word_length: (int) Taille minimum des mots traités.

    Returns: (list) Mots en miniscule, nettoyés.

    """
    list_words = list_words.split()  # split sur l'espace
    clean_words = [word.strip(" ,?").lower() for word in list_words if len(word) > word_length]
    clean_words = [word for word in clean_words if "[" not in word and "(" not in word]
    return clean_words


def remove_words(original_word, word_to_remove):
    """Description: Enlever les mots banals.

    Args:
        original_word: (list) Liste de mots contenant tous les mots.
        word_to_remove: (list) Constante contenant les mots à enlever.

    Returns: (list) Liste de mots sans les mots dits banals.

    """
    clean_list = [word for word in original_word if word not in word_to_remove]
    return clean_list


def get_all_clean_lyrics():
    """Description: Obtenir tous les mots dans toutes les chansons.

    Returns: (list) Tous les mots de toutes les chansons.

    """
    urls = get_all_urls()
    all_clean_lyrics = []
    for url in urls[:]:  # utiliser les slices pour tester avec un nombre limiter d'url.
        lyrics = extract_lyrics(url)
        lyrics = get_clean_lyrics(lyrics, 2)
        all_clean_lyrics.extend(lyrics)
        all_clean_lyrics = remove_words(all_clean_lyrics, BANAL_WORDS)
    return all_clean_lyrics


def print_full_lyrics(top_word=10):
    """Description: Obtenir un top des mots les plus utilisés par l'artiste.

    Args:
        top_word: (int) Taille souhaitée du top.

    Returns:

    """
    full_lyrics = get_all_clean_lyrics()
    full_lyrics = Counter(full_lyrics)
    full_lyrics = full_lyrics.most_common(top_word)
    print(full_lyrics)


print_full_lyrics()
