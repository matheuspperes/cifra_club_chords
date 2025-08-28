from bs4 import BeautifulSoup, Tag


def organize_song_lyrics(*lyrics_map) -> list[list]:
    """
    Filters a lyric's song into a structured list of stanzas.
    - Enclosed text in square brackets ([ ]) triggers a stanza break.
    - Empty lines are preserved as stanza separators.

    Args:
        lyrics_map: tuple of each line

    Returns:
        List of lists, where each sublist represents a stanza.
    """
    combined_stanzas = []
    current_stanza = []
    lyrics: list

    for lyrics in lyrics_map:
        for index, line in enumerate(lyrics):
            line = line.rstrip()
            stripped_line = line.strip()

            # Check for stanza break (square brackets) or empty line
            if (stripped_line.startswith('[') and stripped_line.endswith(']')) or not stripped_line:
                if current_stanza:  # Flush current stanza if not empty
                    # finish stanza
                    combined_stanzas.append(current_stanza)
                    current_stanza = []
                elif not stripped_line:
                    continue

                else:  # Add the bracket line as its own stanza
                    combined_stanzas.append([line])

            # if "parte" in stripped_line.lower():   # sometimes a phrase of tabs remains in the html ("Parte 1 de 3") TODO
            #     continue

            else:
                current_stanza.append(line)

        # Add any remaining lines after processing all songs
        if current_stanza:
            combined_stanzas.append(current_stanza)
            current_stanza = []

    return combined_stanzas


def parse_chords_and_lyrics(html: Tag) -> list:
    html = str(html)
    soup = BeautifulSoup(html, 'html.parser')
    lines = soup.get_text().splitlines()

    return [lines[index] for index in range(len(lines))  # remove the repeated blank lines
            if lines[index] or index == 0 or lines[index - 1]]


def analyze_stanzas(sublists) -> list:
    ids_stanzas = []
    current_id = 0
    id_map = {}  # To track stanza content and their IDs

    i: int = 0
    while i < len(sublists):
        sublist = sublists[i]

        # Check if sublist should be ignored (contains [text]) | e.g. [Primeira Parte]
        ignore = any(item.startswith('[') and item.endswith(']') for item in sublist)
        if ignore:
            i += 1
            continue

        # Check if it has a parentheses
        is_parentheses = any(item.startswith('(') and item.endswith(')') for item in sublist)  # TODO

        # The current sublist is a stanza to analyze
        stanza_content = tuple(sublist)  # Using tuple for hashability

        if stanza_content in id_map:  # Repeated stanza
            original_id = id_map[stanza_content]
            ids_stanzas.append(original_id)
        else:  # New stanza
            # print(f"ID: {current_id} \nEstrofe:\n" + "\n".join(stanza_content) + "\n\n")
            if not id_map and "intro" not in sublist[0].lower():
                current_id += 1

            id_map[stanza_content] = current_id
            ids_stanzas.append(current_id)
            current_id += 1

        i += 1

    sequence_ids_stanzas = []
    prev = ids_stanzas[0]
    count = 1

    for curr in ids_stanzas[1:]:
        if curr == prev:
            count += 1
        else:
            sequence_ids_stanzas.append(f"{prev}({count}x)" if count > 1 else str(prev))
            prev = curr
            count = 1

    # Append the last group
    sequence_ids_stanzas.append(f"{prev}({count}x)" if count > 1 else str(prev))
    id_map = dict(zip(id_map.values(), id_map.keys()))  # switch keys to values
    return [sequence_ids_stanzas, id_map]
