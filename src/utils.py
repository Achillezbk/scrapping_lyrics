from collections import Counter
from bs4 import BeautifulSoup
import requests


BANAL_WORDS = ["", "que", "pas", "les", "des", "qui", "tout", "mais", "dans", "sur", "pour", "plus", "ans"]


def get_all_urls() -> list[str]:
    """Permet d'obtenir toutes les urls liées à un artiste.

    Returns:
        list[str]: _URLs renvoyant les paroles pour chaque chansons._
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


def extract_lyrics(url: str) -> str:
    """Extraction des paroles dans une variable contenant le texte brute.

    Args:
        url (str): URL ciblée.

    Returns:
        str: Chaîne de caractères vide si la requête o.k, chaîne de caractères si la requête k.o
    """
    print(f"Extracting lyrics {url}...")
    r = requests.get(url)
    if r.status_code != 200:
        print("Couldn't fetch page.")
        extract_lyrics(url)  # Appelle récursif de la fonction en cas d'échec de la requête.
        return ""
    else:
        soup = BeautifulSoup(r.content, "html.parser")  # r.content : contenu de la page en HTML.
        list_html_lyrics = soup.find_all("div", class_="Lyrics__Container-sc-1ynbvzw-1 kUgSbL")  # liste avec les div
        list_generator = [lyric.stripped_strings for lyric in list_html_lyrics]  # liste de generators 
        all_lyrics = [" ".join(generator) for generator in list_generator]
        all_lyrics = "\n".join(all_lyrics)
        print("Extraction success !")
        return all_lyrics


def get_clean_lyrics(raw_string: str, word_length: int = 2) -> list[str]:
    """Transformer les chaîne de caractères brutes en liste de mots

    Args:
        raw_string (str): Mots bruts.
        word_length (int): Taille minimum des mots traités. Defaults to 2.

    Returns:
        list[str]: Mots en miniscule, nettoyés.
    """
    list_words = raw_string.split()  # split sur l'espace
    clean_words = [word.strip(" ,?").lower() for word in list_words if len(word) > word_length]
    clean_words = [word for word in clean_words if "[" not in word and "(" not in word]
    return clean_words


def remove_words(original_word: list[str], word_to_remove: list[str]) -> list[str]:
    """Enlever les mots prédéfinis comme étant des mots banals.

    Args:
        original_word (list[str]): Liste de mots contenant tous les mots.
        word_to_remove (list[str]): Constante contenant les mots à enlever.

    Returns:
        list[str]: Liste de mots sans les mots définis comme banals
    """  
    clean_list = [word for word in original_word if word not in word_to_remove]
    return clean_list


def get_all_clean_lyrics() -> list[str]:
    """Obtenir tous les mots dans toutes les chansons.

    Returns:
        list[str]: Tous les mots de toutes les chansons.
    """
    urls = get_all_urls()
    all_clean_lyrics = []
    for url in urls[:20]:  # limite de 20 url pour tester le script.
        raw_lyrics = extract_lyrics(url)
        lyrics = get_clean_lyrics(raw_lyrics, 2)
        all_clean_lyrics.extend(lyrics)
        all_clean_lyrics = remove_words(all_clean_lyrics, BANAL_WORDS)
    return all_clean_lyrics