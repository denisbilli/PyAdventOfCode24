def read_file_into_nested_lists(file_path):
    nested_lists = []

    # Apre il file e legge il contenuto
    with open(file_path, 'r') as file:
        for line in file:
            # Rimuove spazi superflui e splitta la riga in una lista
            nested_lists.append(line.strip().split())

    return nested_lists


# Esempio di utilizzo
file_path = f".\\inputs\\02\\input.txt"
levels = read_file_into_nested_lists(file_path)

print(f"input: {levels}")
print(f"tot levels: {len(levels)}")

def check(curr, prev):
    if abs(prev - curr) > 3:
        reason = f"{curr} {prev} is a difference of {abs(prev - curr)}"
        return False, reason
    elif increasing and curr < prev:
        reason = f"was increasing but {prev} {curr} is decreasing"
        return False, reason
    elif not increasing and curr > prev:
        reason = f"was decreasing but {prev} {curr} is increasing"
        return False, reason
    elif prev == curr:
        reason = f"{curr} {prev} is neither an increase or a decrease"
        return False, reason

    return True, ""

unsafe_levels = []

count = 0
for level in levels:
    good = True
    increasing = int(level[1]) - int(level[0]) > 0
    reason = ""

    for idx in range(1, len(level)):
        prev = int(level[idx - 1])
        curr = int(level[idx])
        good, reason = check(curr, prev)

        if not good:
            break

    increase_str = "increasing" if increasing else "decreasing"
    # if not good:
    #     print(f"level: {level}\t UNSAFE because {reason}")
    # else:
    #     print(f"level: {level}\t SAFE because all levels are {increase_str} by 1, 2, or 3")

    if good:
        count += 1
    else:
        unsafe_levels.append(level)

print(f"safe count: {count}")


# --------------------


old_count = count
count = 0

for level in unsafe_levels:
    good = False

    print(f"Trying level: {level}")

    for rem_idx in range(0, len(level)):
        level_copy = level.copy()
        level_copy.pop(rem_idx)
        idx_good = False

        #print(f"sub-level {rem_idx} {level_copy}")

        increasing = int(level_copy[1]) - int(level_copy[0]) > 0

        reason = ""

        for idx in range(1, len(level_copy)):
            prev = int(level_copy[idx - 1])
            curr = int(level_copy[idx])
            idx_good, reason = check(curr, prev)

            if not idx_good:
                print(f"sub-level {rem_idx} {level_copy}: UNSAFE because {reason}")
                break

        if idx_good:
            print(f"sub-level {rem_idx} {level_copy}: SAFE")

        good = good or idx_good

        if good:
            break

    if good:
        count += 1

print(f"safe count: {old_count}")
print(f"safe count with tolerance: {count}")
print(f"total safe: {old_count+count}")
