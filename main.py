from extraction.website import get_song_html
from process.lyrics import organize_song_lyrics, parse_chords_and_lyrics, analyze_stanzas, set_stanza_default
from process.make_file import make_pdf
from process.similarity import analyze_stanzas_similarity

url = "https://www.cifraclub.com.br/fernandinho/nada-alem-do-sangue/"

song_name = f"{url.split('/')[-2]}"

if __name__ == "__main__":
    song_html = get_song_html(url)
    song_lines = parse_chords_and_lyrics(song_html)

    formatted_lyrics = organize_song_lyrics(song_lines)

    individual_results, groups = analyze_stanzas_similarity(formatted_lyrics)
    if individual_results and groups:
        set_stanza_default(groups, formatted_lyrics)

    sequence, id_map = analyze_stanzas(formatted_lyrics)
    print(f"Ordem: {sequence}")

    for i, stanza in enumerate(formatted_lyrics):
        print(f"Stanza {i + 1}: {stanza}")

    make_pdf(song_name, sequence, id_map)
    # raw_pdf(song_lines, f"{song_name}.pdf")
