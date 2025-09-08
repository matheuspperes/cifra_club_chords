from bs4 import BeautifulSoup, Tag

from process.make_file import is_chord_line


def organize_song_lyrics(*lyrics_map) -> list[list]:
    """Filters a lyric's song into a structured list of stanzas.
    - Enclosed text in square brackets ([ ]) triggers a stanza break.
    - Empty lines are preserved as stanza separators.

    :param lyrics_map: tuple of each line
    :return: List of lists, which each sublist represents a stanza.
    """
    combined_stanzas = []
    current_stanza = []
    lyrics: list

    for lyrics in lyrics_map:
        for index, line in enumerate(lyrics):
            stripped_line = line.strip()

            if stripped_line and stripped_line[0] == '[' and stripped_line[-1] == ']':  # search for tags
                combined_stanzas.append([line.rstrip()])
                continue

            # Check for stanza break or empty line
            elif not stripped_line:
                if analyze_if_ignore_blank_line(lyrics[index - 1], lyrics[index + 1]):
                    continue
                if current_stanza:
                    combined_stanzas.append(current_stanza)
                    current_stanza = []
            else:
                current_stanza.append(line.rstrip())

            # if "parte" in stripped_line.lower():   # sometimes a phrase of tabs remains in the html ("Parte 1 de 3") TODO
            #     continue

        # Add any remaining lines after processing all songs
        if current_stanza:
            combined_stanzas.append(current_stanza)
            current_stanza = []

    return combined_stanzas


def parse_chords_and_lyrics(html: Tag) -> list:
    """Parse

    :param html: Chord tag from beautiful soup
    :return: chord with split lines
    """
    html = str(html)
    soup = BeautifulSoup(html, 'html.parser')
    lines = soup.get_text().splitlines()

    return [lines[index] for index in range(len(lines))  # remove the repeated blank lines
            if lines[index] or index == 0 or lines[index - 1]]


def analyze_stanzas(sublists: list) -> list:
    ids_stanzas = []
    current_id = 0
    id_map = {}  # To track stanza content and their IDs

    i: int = 0
    while i < len(sublists):
        sublist = sublists[i]

        # Check if sublist should be ignored (contains [text]) | e.g. [Primeira Parte]
        ignore = any(item[0] == '[' and item[-1] == ']' for item in sublist)
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


def analyze_if_ignore_blank_line(prev_line: str, post_line: str):
    """Analyze if a blank line corresponds to a new stanza, otherwise should be ignored

    :param prev_line: previous line
    :param post_line: posterior line
    :return: bool
    """
    check_line_1 = False
    check_line_2 = False

    if not is_chord_line(prev_line) and prev_line[0] != '[':
        check_line_1 = True
    if not is_chord_line(post_line) and post_line[0] != '[':
        check_line_2 = True

    return check_line_1 and check_line_2


def set_stanza_default(groups: list, lyrics: list):
    """Set which stanza will be default to change the others that are similar

    :param groups: similar stanzas
    :param lyrics: song lyrics
    """
    combo: dict

    for combo in groups:
        default_item = input(f"Qual estrofe será o padrão? Opções: {combo['indexes']}: ")
        if not default_item:
            return

        # set the default stanza changing the others
        [lyrics.__setitem__(index, lyrics[int(default_item)]) for index in combo['indexes']]
