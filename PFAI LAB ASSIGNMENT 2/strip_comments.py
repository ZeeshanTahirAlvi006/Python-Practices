import sys

with open('neon_wumpus.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

result = []
for line in lines:
    stripped = line.lstrip()
    # Skip pure comment lines
    if stripped.startswith('#'):
        continue

    new_line = line.rstrip('\n')

    # Find inline comment position (not inside string)
    in_single = False
    in_double = False
    comment_pos = -1
    i = 0
    while i < len(new_line):
        ch = new_line[i]
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == '#' and not in_single and not in_double:
            if i > 0 and new_line[i-1] in ' \t':
                comment_pos = i
                break
            elif i == 0:
                comment_pos = 0
                break
        i += 1

    if comment_pos > 0:
        new_line = new_line[:comment_pos].rstrip()
    elif comment_pos == 0:
        continue

    result.append(new_line + '\n')

# Remove excessive blank lines (more than 2 consecutive)
final = []
blank_count = 0
for line in result:
    if line.strip() == '':
        blank_count += 1
        if blank_count <= 2:
            final.append(line)
    else:
        blank_count = 0
        final.append(line)

with open('neon_wumpus.py', 'w', encoding='utf-8') as f:
    f.writelines(final)

print(f'Done. {len(lines)} lines -> {len(final)} lines')
