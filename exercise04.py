import re


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

    return xmas_count+samx_count


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


def shift_and_count(input_matrix, shift_amount):
    new_matrix = shift_matrix_rows(input_matrix, shift_amount)
    matrix_string = matrix_to_string(new_matrix)
    # print(f"\n{matrix_string}\n")
    count = extract_xmas_count(matrix_string)
    return count


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


print("-----------------------------\nPART 1")

file_path = f".\\inputs\\04\\test.txt"
sanitized_file_path = f".\\inputs\\04\\sanitized_input.txt"

file_content = read_file_to_string(file_path)
char_matrix = string_to_matrix(file_content)

sanitized_input = add_custom_border_to_text(file_content, 2)
save_string_to_file(sanitized_input, sanitized_file_path)

sanitized_input_char_matrix = string_to_matrix(sanitized_input)

total_count = 0

orig_count = shift_and_count(sanitized_input_char_matrix, 0)
total_count += orig_count

print(f"count: {orig_count}")
print(f"total count: {total_count}")

print("\n-----=> TRASPOSIZIONE <=-----")

transposed_char_matrix = transpose_matrix(char_matrix)
transposed_string = matrix_to_string(transposed_char_matrix)

sanitized_transposed = add_custom_border_to_text(transposed_string, 2)
save_string_to_file(sanitized_transposed, f".\\inputs\\04\\transposed.txt")

sanitized_transposed_char_matrix = string_to_matrix(sanitized_transposed)

transposed_count = shift_and_count(sanitized_transposed_char_matrix, 0)
total_count += transposed_count

print(f"count: {transposed_count}")
print(f"total count: {total_count}")

print("\n-------=> MATRIX +1 <=-------")

# matrix_plus1_count = shift_and_count(char_matrix, 1)
# total_count += matrix_plus1_count
#
# print(f"count: {matrix_plus1_count}")
# print(f"total count: {total_count}")

print("\n-------=> MATRIX -1 <=-------")

# matrix_minus1_count = shift_and_count(char_matrix, -1)
# total_count += matrix_minus1_count
#
# print(f"count: {matrix_minus1_count}")
# print(f"total count: {total_count}")

print("\n---=> TRANSP. MATRIX +1 <=---")

shifted_matrix_plus1 = shift_matrix_rows(char_matrix, 1)
transposed_matrix_plus1 = transpose_matrix(shifted_matrix_plus1)
transposed_matrix_plus1_str = matrix_to_string(transposed_matrix_plus1)

sanitized_transposed_matrix_plus1 = add_custom_border_to_text(transposed_matrix_plus1_str, 2)
save_string_to_file(sanitized_transposed_matrix_plus1, f".\\inputs\\04\\transposed_matrix_plus1.txt")

sanitized_transposed_matrix_plus1_char_matrix = string_to_matrix(sanitized_transposed_matrix_plus1)

transp_matrix_plus1_count = shift_and_count(sanitized_transposed_matrix_plus1_char_matrix, 0)
total_count += transp_matrix_plus1_count

print(f"count: {transp_matrix_plus1_count}")
print(f"total count: {total_count}")

print("\n---=> TRANSP. MATRIX -1 <=---")

shifted_matrix_minus1 = shift_matrix_rows(char_matrix, -1)
transposed_matrix_minus1 = transpose_matrix(shifted_matrix_minus1)
transposed_matrix_minus1_str = matrix_to_string(transposed_matrix_minus1)

sanitized_transposed_matrix_minus1 = add_custom_border_to_text(transposed_matrix_minus1_str, 2)
save_string_to_file(sanitized_transposed_matrix_minus1, f".\\inputs\\04\\transposed_matrix_minus1.txt")

sanitized_transposed_matrix_minus1_char_matrix = string_to_matrix(sanitized_transposed_matrix_minus1)

transp_matrix_minus1_count = shift_and_count(sanitized_transposed_matrix_minus1_char_matrix, 0)
total_count += transp_matrix_minus1_count

print(f"count: {transp_matrix_minus1_count}")
print(f"total count: {total_count}")
