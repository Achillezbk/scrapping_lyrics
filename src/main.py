import collections
import utils


def print_full_lyrics(top_word: int = 10) -> list[tuple]:
    """Permet d'obtenir un top des mots les plus utilisés par l'artiste.

    Args:
        top_word (int, optional): Taille souhaitée du top. Defaults to 10.

    Returns:
        list[tuple]: Contenant les mots les plus utilisés par l'artiste.
    """
    full_lyrics = utils.get_all_clean_lyrics()
    full_lyrics = collections.Counter(full_lyrics)
    full_lyrics = full_lyrics.most_common(top_word)
    return full_lyrics


top_lyrics = print_full_lyrics()
print(top_lyrics)
