
def split_string_by_separator(input_string, separator):
    """
    Divide una stringa in una lista basandosi su un separatore specificato.

    Args:
        input_string (str): La stringa da dividere.
        separator (str): Il separatore da utilizzare.

    Returns:
        list: Una lista di sottostringhe separate dal separatore.
    """
    if not separator:
        raise ValueError("Il separatore non può essere una stringa vuota.")

    return input_string.split(separator)

def string_to_char_list(input_string):
    """
    Trasforma una stringa in una lista di caratteri.

    Args:
        input_string (str): La stringa di input.

    Returns:
        list: Lista di caratteri.
    """
    return list(input_string)