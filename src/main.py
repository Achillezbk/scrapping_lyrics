import collections
import utils


def print_full_lyrics(top_word: int = 10) -> list[tuple]:
    """Description: Obtenir un top des mots les plus utilisés par l'artiste.

    Args:
        top_word: (int) Taille souhaitée du top.

    Returns: (list[tuple]) Contenant les mots les plus utilisés par l'artiste.

    """
    full_lyrics = utils.get_all_clean_lyrics()
    full_lyrics = collections.Counter(full_lyrics)
    full_lyrics = full_lyrics.most_common(top_word)
    return full_lyrics


print(print_full_lyrics())
