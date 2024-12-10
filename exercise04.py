import re
from colorama import Fore, Style, init


# Inizializza Colorama per colori cross-platform
init(autoreset=True)


def export_regex_matches_with_groups(pattern, text):
    """
    Esporta tutti i match di una regex da un input, includendo i gruppi catturati.

    Args:
        pattern (str): La regex da utilizzare per il matching.
        text (str): Il testo su cui cercare i match.

    Returns:
        list: Una lista di tuple, ciascuna contenente i gruppi del match.
              Se non ci sono gruppi, restituisce i match completi.
    """
    try:
        matches = re.findall(pattern, text)
        # Verifica se la regex cattura gruppi
        if matches and isinstance(matches[0], tuple):
            return [list(match) for match in matches]  # Converte ogni tuple in lista
        else:
            return matches  # Restituisce i match semplici se non ci sono gruppi
    except re.error as e:
        print(f"Errore nella regex: {e}")
        return []


def read_file_to_string(file_path):
    """
    Legge un intero file e restituisce il contenuto come stringa.

    Args:
        file_path (str): Il percorso del file da leggere.

    Returns:
        str: Il contenuto del file come stringa.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Errore: Il file '{file_path}' non esiste.")
        return ""
    except IOError as e:
        print(f"Errore durante la lettura del file: {e}")
        return ""


def string_to_matrix(input_string):
    """
    Converte una stringa in una matrice XY di caratteri.
    Ogni riga è separata da un carattere di a capo '\n'.

    Args:
        input_string (str): La stringa da convertire.

    Returns:
        list: Matrice XY (lista di liste) di caratteri.
    """
    return [list(line) for line in input_string.splitlines()]


def transpose_matrix(matrix):
    """
    Traspone una matrice qualsiasi.

    Args:
        matrix (list): Matrice originale (lista di liste).

    Returns:
        list: Matrice trasposta.
    """
    return [list(row) for row in zip(*matrix)]


def matrix_to_string(matrix):
    """
    Converte una matrice XY di caratteri in una stringa.
    Ogni riga della matrice corrisponde a una riga della stringa separata da '\n'.

    Args:
        matrix (list): Matrice XY (lista di liste) di caratteri.

    Returns:
        str: Stringa risultante.
    """
    return '\n'.join(''.join(row) for row in matrix)


def extract_xmas_count(input_text):
    regex_xmas = r"XMAS"
    xmas_matches = export_regex_matches_with_groups(regex_xmas, input_text)
    xmas_count = len(xmas_matches)
    print(f"xmas_matches: {xmas_matches}  =>  {xmas_count}")

    regex_samx = r"SAMX"
    samx_matches = export_regex_matches_with_groups(regex_samx, input_text)
    samx_count = len(samx_matches)
    print(f"samx_matches: {samx_matches}  =>  {samx_count}")

    return xmas_count, samx_count, xmas_count + samx_count


def shift_matrix_rows(matrix, step):
    """
    Sposta ogni riga di una matrice di caratteri di un numero di caratteri proporzionale
    al proprio numero di riga (step * numero di riga).

    Args:
        matrix (list): Matrice XY (lista di liste) di caratteri.
        step (int): Numero di caratteri da spostare per riga, moltiplicato per il numero di riga.

    Returns:
        list: Matrice con le righe spostate.
    """
    shifted_matrix = []
    for row_index, row in enumerate(matrix):
        shift_amount = step * row_index
        # Effettua lo spostamento usando slicing e concatenazione circolare
        shifted_row = row[-shift_amount:] + row[:-shift_amount]
        shifted_matrix.append(shifted_row)
    return shifted_matrix


def shift_matrix_rows_with_dots(matrix, step):
    """
    Sposta ogni riga di una matrice di caratteri di un numero di caratteri proporzionale
    al proprio numero di riga (step * numero di riga), rimpiazzando i caratteri che "escono"
    con un punto ".".

    Args:
        matrix (list): Matrice XY (lista di liste) di caratteri.
        step (int): Numero di caratteri da spostare per riga, moltiplicato per il numero di riga.

    Returns:
        list: Matrice con le righe spostate.
    """
    shifted_matrix = []
    for row_index, row in enumerate(matrix):
        shift_amount = step * row_index

        if shift_amount > 0:
            # Rimpiazza i caratteri "spostati a sinistra" con "."
            shifted_row = ["." for _ in range(shift_amount)] + row[:-shift_amount]
        elif shift_amount < 0:
            # Rimpiazza i caratteri "spostati a destra" con "."
            shift_amount = abs(shift_amount)
            shifted_row = row[shift_amount:] + ["." for _ in range(shift_amount)]
        else:
            # Nessuno spostamento, la riga rimane invariata
            shifted_row = row

        shifted_matrix.append(shifted_row)

    return shifted_matrix


def shift_matrix_with_diagonal(matrix, direction="right"):
    """
    Crea una diagonale nella matrice spostando i caratteri verso una direzione specificata
    (destra o sinistra) e riempiendo i vuoti con punti (".").

    Args:
        matrix (list): Matrice XY (lista di liste) di caratteri.
        direction (str): Direzione della diagonale: "right" (destra) o "left" (sinistra).

    Returns:
        list: Matrice trasformata con la diagonale.
    """
    max_width = len(matrix[0]) + len(matrix)  # Larghezza massima con shift
    transformed_matrix = []

    for row_index, row in enumerate(matrix):
        if direction == "right":
            # Numero di punti da aggiungere prima e dopo per la diagonale verso destra
            leading_dots = "." * row_index
            trailing_dots = "." * (max_width - len(leading_dots) - len(row))
        elif direction == "left":
            # Numero di punti da aggiungere prima e dopo per la diagonale verso sinistra
            trailing_dots = "." * row_index
            leading_dots = "." * (max_width - len(trailing_dots) - len(row))
        else:
            raise ValueError("Direzione non valida. Usa 'right' o 'left'.")

        # Costruzione della riga trasformata
        transformed_row = leading_dots + "".join(row) + trailing_dots
        transformed_matrix.append(transformed_row)

    # Aggiungi una cornice di punti sopra e sotto
    border = "." * max_width
    transformed_matrix = [border] + transformed_matrix + [border]

    return transformed_matrix


def shift_and_count(input_matrix, shift_amount):
    new_matrix = shift_matrix_rows_with_dots(input_matrix, shift_amount)
    matrix_string = matrix_to_string(new_matrix)
    # print(f"\n{matrix_string}\n")
    xmas_count, samx_count, count = extract_xmas_count(matrix_string)
    return xmas_count, samx_count, count


def add_custom_border_to_text(input_string, num_points):
    """
    Aggiunge un bordo personalizzato di punti a una stringa multilinea:
    - num_points righe di soli punti all'inizio e alla fine.
    - num_points punti come prefisso e suffisso a ogni riga esistente.

    Args:
        input_string (str): La stringa multilinea da modificare.
        num_points (int): Il numero di punti da aggiungere come prefisso, suffisso,
                          e righe di bordo.

    Returns:
        str: La stringa modificata con il bordo aggiunto.
    """
    if num_points <= 0:
        raise ValueError("Il numero di punti deve essere maggiore di 0.")

    # Suddividi la stringa in righe
    lines = input_string.splitlines()

    # Calcola la lunghezza della prima riga
    if not lines:
        return ""  # Se la stringa è vuota, restituisci una stringa vuota
    line_length = len(lines[0])

    # Genera il bordo di soli punti
    border_line = "." * (line_length + 2 * num_points)

    # Aggiungi i prefissi e i suffissi di punti alle righe esistenti
    prefix_suffix = "." * num_points
    bordered_lines = [f"{prefix_suffix}{line}{prefix_suffix}" for line in lines]

    # Aggiungi il numero di righe di bordo superiore e inferiore
    border_block = [border_line] * num_points
    result = "\n".join(border_block + bordered_lines + border_block)
    return result


def save_string_to_file(content, file_path):
    """
    Salva una stringa in un file.

    Args:
        content (str): La stringa da salvare.
        file_path (str): Il percorso del file in cui salvare la stringa.

    Returns:
        None
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except IOError as e:
        print(f"Errore durante il salvataggio del file: {e}")


def count_words_from_position(matrix, start_row, start_col, words):
    """
    Conta quante volte le parole richieste esistono partendo da una posizione specifica
    nella matrice, considerando tutte le direzioni (destra, sinistra, alto, basso, diagonali).

    Args:
        matrix (list of list): Matrice di caratteri.
        start_row (int): Riga di partenza.
        start_col (int): Colonna di partenza.
        words (list): Lista di parole da cercare.

    Returns:
        dict: Dizionario con le posizioni e direzioni per ciascuna parola.
              Formato: { parola: [(start_row, start_col, direction_name), ...] }
    """
    def search_in_direction(matrix, word, start_row, start_col, direction):
        """
        Cerca una parola partendo da una posizione in una direzione specifica.

        Args:
            matrix (list): Matrice di caratteri.
            word (str): Parola da cercare.
            start_row (int): Riga iniziale.
            start_col (int): Colonna iniziale.
            direction (tuple): Direzione come (row_delta, col_delta).

        Returns:
            bool: True se la parola è trovata, False altrimenti.
        """
        rows, cols = len(matrix), len(matrix[0])
        for i in range(len(word)):
            r, c = start_row + i * direction[0], start_col + i * direction[1]
            if r < 0 or c < 0 or r >= rows or c >= cols or matrix[r][c] != word[i]:
                return False
        return True

    # Definisci tutte le direzioni con nomi
    directions = {
        "right": (0, 1),
        "left": (0, -1),
        "down": (1, 0),
        "up": (-1, 0),
        "diagonal_down_right": (1, 1),
        "diagonal_down_left": (1, -1),
        "diagonal_up_right": (-1, 1),
        "diagonal_up_left": (-1, -1),
    }

    # Risultati della ricerca
    word_results = {word: [] for word in words}

    # Cerca ogni parola in ogni direzione
    for word in words:
        for direction_name, direction_delta in directions.items():
            if search_in_direction(matrix, word, start_row, start_col, direction_delta):
                word_results[word].append((start_row, start_col, direction_name))

    return word_results


def get_matrix_dimensions(matrix):
    """
    Ottiene il numero di righe e colonne di una matrice.

    Args:
        matrix (list of list): Matrice rappresentata come una lista di liste.

    Returns:
        tuple: Numero di righe e numero di colonne (rows, cols).
    """
    rows = len(matrix)
    cols = len(matrix[0]) if matrix else 0  # Verifica che la matrice non sia vuota
    return rows, cols


def merge_results(all_results):
    """
    Unifica i risultati di più ricerche in un unico dizionario.

    Args:
        all_results (list): Lista di dizionari con i risultati delle ricerche.

    Returns:
        dict: Dizionario unificato con tutte le parole e le loro posizioni.
    """
    unified_results = {}
    for result in all_results:
        for word, occurrences in result.items():
            if word not in unified_results:
                unified_results[word] = []
            unified_results[word].extend(occurrences)
    return unified_results


def highlight_words_in_matrix(matrix, results, words):
    """
    Evidenzia i caratteri della matrice basati sui risultati della ricerca.

    Args:
        matrix (list of list): Matrice di caratteri.
        results (dict): Dizionario con parole trovate e posizioni.
                        Formato: { parola: [(start_row, start_col, direction), ...] }
        words (list): Lista di parole cercate.

    Returns:
        None: Stampa la matrice colorata nel terminale.
    """
    # Copia della matrice per la colorazione
    colored_matrix = [[char for char in row] for row in matrix]

    # Colori disponibili per le parole trovate
    colors = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA]

    # Direzioni come (row_delta, col_delta)
    directions_map = {
        "right": (0, 1),
        "left": (0, -1),
        "down": (1, 0),
        "up": (-1, 0),
        "diagonal_down_right": (1, 1),
        "diagonal_down_left": (1, -1),
        "diagonal_up_right": (-1, 1),
        "diagonal_up_left": (-1, -1),
    }

    # Funzione per applicare un colore a un carattere
    def apply_color(char, color):
        return f"{color}{char}{Style.RESET_ALL}"

    # Colora le parole trovate
    for word_index, word in enumerate(words):
        word_color = colors[word_index % len(colors)]  # Colore ciclico per ogni parola
        if word in results:
            for (row, col, direction_name) in results[word]:
                dr, dc = directions_map[direction_name]
                for i in range(len(word)):
                    r, c = row + i * dr, col + i * dc
                    if 0 <= r < len(matrix) and 0 <= c < len(matrix[0]):
                        colored_matrix[r][c] = apply_color(colored_matrix[r][c], word_color)

    # Stampa la matrice colorata
    for row in colored_matrix:
        print("".join(row))


file_path = f"./inputs/04/input.txt"

# region PART 1
print("-----------------------------\nPART 1")

sanitized_file_path = f"./inputs/04/sanitized_input.txt"

file_content = read_file_to_string(file_path)
char_matrix = string_to_matrix(file_content)

sanitized_content = add_custom_border_to_text(file_content, 8)
sanitized_char_matrix = string_to_matrix(sanitized_content)

save_string_to_file(sanitized_content, sanitized_file_path)

total_count = 0


def star_search():
    total_count = 0
    rows, cols = get_matrix_dimensions(char_matrix)
    all_results = []
    for row in range(0, rows):
        for col in range(0, cols):
            # print(f"searching from [{row},{col}]")
            results = count_words_from_position(char_matrix, row, col, ["XMAS"])
            # print(f" > results: {results}")
            if results:
                # print(f" > XMAS: {results["XMAS"]}")
                if results["XMAS"]:
                    total_count += len(results["XMAS"])
                    all_results.append(results)
    combined_results = merge_results(all_results)
    highlight_words_in_matrix(char_matrix, combined_results, ["XMAS"])
    return total_count

def matrix_search():
    total_count = 0
    # region PART 1
    print("-----------------------------\nPART 1")
    xmas_count, samx_count, orig_count = shift_and_count(char_matrix, 0)
    total_count += orig_count
    print(f"count: {xmas_count}+{samx_count} = {orig_count}")
    print(f"total count: {total_count}")
    # endregion
    # region PART 2
    print("\n-----=> TRASPOSIZIONE <=-----")
    transposed_char_matrix = transpose_matrix(char_matrix)
    transposed_string = matrix_to_string(transposed_char_matrix)
    save_string_to_file(transposed_string, f"./inputs/04/transposed.txt")
    xmas_count, samx_count, transposed_count = shift_and_count(transposed_char_matrix, 0)
    total_count += transposed_count
    print(f"count: {xmas_count}+{samx_count} = {transposed_count}")
    print(f"total count: {total_count}")
    # endregion
    # region TRANSP MATRIX +1
    print("\n---=> TRANSP. MATRIX +1 <=---")
    shifted_matrix_plus1 = shift_matrix_with_diagonal(char_matrix, "right")
    shifted_plus1_str = matrix_to_string(shifted_matrix_plus1)
    save_string_to_file(shifted_plus1_str, f"./inputs/04/shifted_plus1.txt")
    # xmas_count, samx_count, shifted_plus1_count = shift_and_count(shifted_matrix_plus1, 0)
    # total_count += shifted_plus1_count
    #
    # print(f"count: {xmas_count}+{samx_count} = {shifted_plus1_count}")
    # print(f"total count: {total_count}")
    transposed_shifted_plus1 = transpose_matrix(shifted_matrix_plus1)
    transposed_shifted_plus1_str = matrix_to_string(transposed_shifted_plus1)
    save_string_to_file(transposed_shifted_plus1_str, f"./inputs/04/transposed_shifted_plus1.txt")
    xmas_count, samx_count, transposed_shifted_plus1_count = shift_and_count(transposed_shifted_plus1, 0)
    total_count += transposed_shifted_plus1_count
    print(f"count: {xmas_count}+{samx_count} = {transposed_shifted_plus1_count}")
    print(f"total count: {total_count}")
    # endregion
    # region TRANSP MATRIX -1
    print("\n---=> TRANSP. MATRIX -1 <=---")
    shifted_matrix_minus1 = shift_matrix_with_diagonal(char_matrix, "left")
    shifted_minus1_str = matrix_to_string(shifted_matrix_minus1)
    save_string_to_file(shifted_minus1_str, f"./inputs/04/shifted_minus1.txt")
    # xmas_count, samx_count, shifted_minus1_count = shift_and_count(shifted_matrix_minus1, 0)
    # total_count += shifted_minus1_count
    #
    # print(f"count: {xmas_count}+{samx_count} = {shifted_minus1_count}")
    # print(f"total count: {total_count}")
    transposed_shifted_minus1 = transpose_matrix(shifted_matrix_minus1)
    transposed_shifted_minus1_str = matrix_to_string(transposed_shifted_minus1)
    save_string_to_file(transposed_shifted_minus1_str, f"./inputs/04/transposed_shifted_minus1.txt")
    xmas_count, samx_count, transposed_shifted_minus1_count = shift_and_count(transposed_shifted_minus1, 0)
    total_count += transposed_shifted_minus1_count
    print(f"count: {xmas_count}+{samx_count} = {transposed_shifted_minus1_count}")
    print(f"total count: {total_count}")
    # endregion
    return total_count


# STAR SEARCH
total_count = star_search()

# MATRIX SEARCH
#total_count = matrix_search()

print(f"\nSOLUTION --------------------\n")
print(f"total_count: {total_count}")

# endregion


word = "MAS"


def generate_patterns(word):
    """
    Genera i 4 pattern per una parola di lunghezza 3, come specificato:

    Pattern 1:
    w0 . w0
    . w1 .
    w2 . w2

    Pattern 2:
    w0 . w2
    . w1 .
    w0 . w2

    Pattern 3:
    w2 . w2
    . w1 .
    w0 . w0

    Pattern 4:
    w2 . w0
    . w1 .
    w2 . w0

    Args:
        word (str): Parola di lunghezza 3.

    Returns:
        list: Lista dei 4 pattern generati (ognuno è una lista di liste di caratteri).
    """
    if len(word) != 3:
        raise ValueError("La parola deve avere lunghezza 3.")

    w0, w1, w2 = word[0], word[1], word[2]

    # Pattern 1
    pattern1 = [
        [w0, '.', w0],
        ['.', w1, '.'],
        [w2, '.', w2]
    ]

    # Pattern 2
    pattern2 = [
        [w0, '.', w2],
        ['.', w1, '.'],
        [w0, '.', w2]
    ]

    # Pattern 3
    pattern3 = [
        [w2, '.', w2],
        ['.', w1, '.'],
        [w0, '.', w0]
    ]

    # Pattern 4
    pattern4 = [
        [w2, '.', w0],
        ['.', w1, '.'],
        [w2, '.', w0]
    ]

    return [pattern1, pattern2, pattern3, pattern4]


def star_search2(patterns):
    total_count = 0
    rows, cols = get_matrix_dimensions(char_matrix)
    all_results = []
    for row in range(0, rows - len(word) + 1):
        for col in range(0, cols - len(word) + 1):
            print(f"searching from [{row},{col}]")

            for pattern in patterns:
                print(f" > searching pattern:\n{matrix_to_string(pattern)}\n")
                matches = 0
                for int_row in range(0, len(word)):
                    for int_col in range(0, len(word)):
                        grid_char = char_matrix[row + int_row][col + int_col]
                        pattern_char = pattern[int_row][int_col]
                        print(f"  > grid[{row + int_row},{col + int_col}]<->pattern[{int_row},{int_col}]: {grid_char}<->{pattern_char}")
                        if pattern_char == '.':
                            matches += 1
                            continue
                        if grid_char == pattern_char:
                            matches += 1
                            continue
                if matches == 9:
                    total_count += 1
                    print(f" >>> pattern FOUND!")
                else:
                    print(f" >>> NOT FOUND [best: {matches}]")

    return total_count

print("-----------------------------\nPART 2")
total_count = 0

patterns = generate_patterns(word)

total_count = star_search2(patterns)

print(f"\nSOLUTION --------------------\n")
print(f"total_count: {total_count}")