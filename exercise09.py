import re


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


def split_string_into_key_value_pairs(input_string):
    """
    Scompone una stringa di cifre in coppie chiave-valore.

    Args:
        input_string (str): Una stringa composta da sole cifre.

    Returns:
        list: Lista di tuple (chiave, valore).

    Raises:
        ValueError: Se la stringa contiene caratteri non numerici.
    """
    # Ripulisci la stringa: rimuovi caratteri non numerici
    clean_string = input_string.replace('\n', '').replace(' ', '').strip()

    if not clean_string.isdigit():
        raise ValueError("La stringa deve essere composta solo da cifre.")

    result = []
    for i in range(0, len(clean_string), 2):
        key = int(clean_string[i])
        # Se esiste un valore successivo, lo assegna come valore, altrimenti usa 0
        value = int(clean_string[i + 1]) if i + 1 < len(clean_string) else 0
        result.append((key, value))

    return result


def string_to_char_list(input_string):
    """
    Trasforma una stringa in una lista di caratteri.

    Args:
        input_string (str): La stringa di input.

    Returns:
        list: Lista di caratteri.
    """
    return list(input_string)


def char_list_to_string(char_list):
    """
    Trasforma una lista di caratteri in una stringa.

    Args:
        char_list (list): La lista di caratteri.

    Returns:
        str: La stringa risultante.
    """
    return ''.join(char_list)


def swap_positions(lst, pos1, pos2):
    """
    Scambia gli elementi di due posizioni in una lista.

    Args:
        lst (list): La lista in cui effettuare lo swap.
        pos1 (int): Indice del primo elemento.
        pos2 (int): Indice del secondo elemento.

    Returns:
        None: La lista viene modificata inline.
    """
    if pos1 < 0 or pos2 < 0 or pos1 >= len(lst) or pos2 >= len(lst):
        raise IndexError("Posizioni fuori dai limiti della lista.")

    lst[pos1], lst[pos2] = lst[pos2], lst[pos1]


def swap_positions_with_digits(lst, pos1, pos2):
    """
    Scambia gli elementi di due posizioni in una lista, gestendo numeri a più cifre.
    Se a pos2 c'è un numero con più cifre, le cifre vengono spostate in pos1, e pos2 viene riempita con punti.

    Args:
        lst (list): La lista in cui effettuare lo swap.
        pos1 (int): Indice della posizione iniziale della sequenza di destinazione.
        pos2 (int): Indice della posizione del numero.

    Returns:
        None: La lista viene modificata inline.

    Raises:
        ValueError: Se pos1 non ha abbastanza spazio per le cifre di pos2.
    """
    if pos1 < 0 or pos2 < 0 or pos1 >= len(lst) or pos2 >= len(lst):
        raise IndexError("Posizioni fuori dai limiti della lista.")

    # Determina il valore a pos2 e le sue cifre
    value_at_pos2 = int(lst[pos2])
    if not isinstance(value_at_pos2, int):
        raise ValueError(f"L'elemento in pos2 ({pos2}) deve essere un numero intero.")

    digits = list(str(value_at_pos2))  # Dividi il numero in cifre
    num_digits = len(digits)

    # Verifica se ci sono abbastanza spazi a pos1 per inserire le cifre
    if pos1 + num_digits > len(lst):
        raise ValueError(f"Non ci sono abbastanza spazi in pos1 ({pos1}) per contenere {num_digits} cifre.")

    # Sostituisci i punti a pos2 con tante cifre quante quelle del numero
    lst[pos2:pos2 + 1] = ['.'] * num_digits

    # Inserisci le cifre a partire da pos1
    lst[pos1:pos1 + num_digits] = digits


# def swap_positions(lst, pos1, pos2):
#     """
#     Scambia un numero in pos2 con una sequenza di punti '.' in pos1,
#     dove il numero di punti in pos1 deve essere uguale alle cifre del numero in pos2.
#
#     Args:
#         lst (list): La lista in cui effettuare lo swap.
#         pos1 (int): Indice della posizione iniziale della sequenza di punti.
#         pos2 (int): Indice della posizione del numero.
#
#     Returns:
#         None: La lista viene modificata inline.
#
#     Raises:
#         ValueError: Se la sequenza di punti in pos1 non è sufficiente o valida.
#         IndexError: Se pos1 o pos2 sono fuori dai limiti della lista.
#     """
#     if pos1 < 0 or pos2 < 0 or pos1 >= len(lst) or pos2 >= len(lst):
#         raise IndexError("Posizioni fuori dai limiti della lista.")
#
#     # Determina il numero in pos2 e calcola il numero di cifre
#     value_at_pos2 = lst[pos2]
#     if not isinstance(value_at_pos2, int):
#         raise ValueError(f"L'elemento in pos2 ({pos2}) deve essere un numero.")
#
#     num_digits = len(str(value_at_pos2))
#
#     # Verifica se ci sono abbastanza punti consecutivi in pos1
#     if lst[pos1:pos1 + num_digits] != ['.'] * num_digits:
#         raise ValueError(
#             f"Non ci sono abbastanza punti '.' consecutivi in pos1 ({pos1}) per scambiare con {value_at_pos2}.")
#
#     # Effettua lo swap
#     lst[pos1:pos1 + num_digits] = [value_at_pos2]  # Sostituisci i punti con il numero
#     lst[pos2] = '.' * num_digits  # Sostituisci il numero con punti


def find_element(lst, elem, reverse=False):
    """
    Cerca un elemento o una sottolista in una lista partendo dall'inizio o dal fondo.

    Args:
        lst (list): La lista in cui cercare.
        elem: L'elemento o la sottolista da cercare.
        reverse (bool): Se True, cerca partendo dal fondo; altrimenti dall'inizio.

    Returns:
        int: L'indice della prima occorrenza dell'elemento o sottolista trovato.
        -1: Se l'elemento o la sottolista non viene trovato.
    """
    if reverse:
        # Cerca partendo dalla fine
        for i in range(len(lst) - 1, -1, -1):
            if isinstance(elem, list):  # Se stiamo cercando una sottolista
                if lst[i:i + len(elem)] == elem:
                    return i
            else:  # Caso singolo elemento
                if lst[i] == str(elem):
                    return i
    else:
        # Cerca partendo dall'inizio
        for i in range(len(lst)):
            if isinstance(elem, list):  # Se stiamo cercando una sottolista
                if lst[i:i + len(elem)] == elem:
                    return i
            else:  # Caso singolo elemento
                if lst[i] == str(elem):
                    return i

    return -1  # Elemento o sottolista non trovato


def get_first_half(lst):
    """
    Restituisce la prima metà di una lista.

    Args:
        lst (list): La lista di input.

    Returns:
        list: La prima metà della lista. Se la lunghezza è dispari,
              include l'elemento centrale.
    """
    mid_index = (len(lst) + 1) // 2  # Calcola l'indice della metà (includendo l'elemento centrale se dispari)
    return lst[:mid_index]


def split_string_by_pattern(input_string, pattern):
    """
    Divide una stringa in base a un pattern specifico, con una o più ripetizioni,
    e considera solo ciò che è compreso nei match del pattern.

    Args:
        input_string (str): La stringa di input.
        pattern (str): Il pattern da cercare.

    Returns:
        list: Una lista contenente i match del pattern trovati.
    """
    # Compila il pattern per una o più ripetizioni
    regex = re.compile(f"({re.escape(pattern)})+")

    result = []

    # Cerca tutti i match nella stringa
    for match in regex.finditer(input_string):
        start, end = match.span()

        # Aggiungi i pattern trovati come blocchi separati
        repetitions = (end - start) // len(pattern)
        result.extend([pattern] * repetitions)

    return result


def split_numbers_and_dots(input_string):
    """
    Divide la stringa in sottostringhe alternate di numeri e punti,
    trasformando ciascuna sottostringa in una lista di singoli caratteri.

    Args:
        input_string (str): La stringa di input.

    Returns:
        list: Una lista composta da singoli numeri e punti.
    """
    import re

    # Divide la stringa in blocchi alternati di numeri e punti
    segments = re.findall(r'[0-9]+|[.]+', input_string)
    output = []
    idx = 0
    current_num = 0

    while idx < len(segments):
        # Elabora il blocco di numeri
        if idx < len(segments):
            current_num_str = str(segments[idx]).__contains__(str(current_num))
            next_num_str = str(segments[idx]).__contains__(str(current_num+1))

            while current_num_str and next_num_str:
                output.extend(split_string_by_pattern(str(segments[idx]), str(current_num)))
                current_num += 1
                current_num_str = str(segments[idx]).__contains__(str(current_num))
                next_num_str = str(segments[idx]).__contains__(str(current_num+1))

            if current_num_str and not next_num_str:
                output.extend(split_string_by_pattern(str(segments[idx]), str(current_num)))

        # Elabora il blocco di punti
        if idx + 1 < len(segments):
            dots = list(segments[idx + 1])  # Converte i punti in una lista di caratteri
            output.extend(dots)

        # Incrementa l'indice di 2 (passa ai prossimi blocchi numeri e punti)
        current_num += 1
        idx += 2

        try:
            while not str(segments[idx]).__contains__(str(current_num)):
                current_num += 1
        except:
            pass

    return output


print("-----------------------------\nPART 1")

file_path = f"./inputs/09/input.txt"
file_content = read_file_to_string(file_path)

input_data = split_string_into_key_value_pairs(file_content)
print(f"input_data: {input_data}")

output_data_string = ""
last_file_id = len(input_data)-1
tot_points = 0

file_id = 0
for file in input_data:
    output_data_string += str(file_id) * file[0]
    output_data_string += "." * file[1]
    tot_points += file[1]
    file_id += 1

print(f"output_data_string: {output_data_string}")
print(f"expected points: {tot_points}")

output_data_lst = split_numbers_and_dots(output_data_string)
output_final_string = ""

output_data_lst_orig = output_data_lst.copy()

dots_to_find = len(str(last_file_id))
dots_pos = find_element(output_data_lst, elem=['.']*dots_to_find, reverse=False)

print(f"starting with {last_file_id}")
swapped = 0
# cerco il primo punto nella lista di caratteri
while dots_pos:
    # a questo punto cerco l'ultimo file_id che esiste
    last_file_pos = find_element(output_data_lst, elem=last_file_id, reverse=True)
    dots_to_find = len(str(last_file_id))

    # if dots_pos > last_file_pos:
    #     print(f" > middle_solution: {output_final_string}")
    #     print(f" > END!")
    #     break

    if last_file_pos >= 0:
        print(f" > swapping {dots_pos}<->{last_file_pos}")
        swap_positions_with_digits(output_data_lst, dots_pos, last_file_pos)
        swapped += 1

    dots_pos = find_element(output_data_lst, elem=['.']*dots_to_find, reverse=False)
    output_final_string = char_list_to_string(output_data_lst)

    if output_final_string.endswith("." * tot_points) or last_file_id == 0 or dots_pos > last_file_pos:
        print(f" > middle_solution: {output_final_string}")
        print(f" > END!")
        break

    if swapped == output_data_lst_orig.count(str(last_file_id)):
        print(f" > end for char {last_file_id}... proceed with next")
        last_file_id -= 1
        swapped = 0

checksum_list = [int(char) for char in string_to_char_list(output_final_string) if char != '.']

print(f"\nSOLUTION --------------------\n")

idx = 0
sum = 0
for item in checksum_list:
    #print(f"{item} * {idx} = {item * idx}")
    sum += item * idx
    idx += 1

print(f"solution: {sum}\n")

print("-----------------------------\nPART 2")

print(f"\nSOLUTION --------------------\n")

print(f"solution:\n")
