import re
from pathlib import Path

from fpdf import FPDF

from constants import CHORD_REGEX, DEFAULT_FONT, PDF_FOLDER

current_folder = Path(__file__).parent.parent


def check_folder():
    path = Path(current_folder) / PDF_FOLDER
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


def raw_pdf(text, output_filename):
    """Create a PDF with monospaced font preserving the formatting"""
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", style='B', size=15)
    pdf.cell(0, 2, "Nada alem do sangue", align="C")
    pdf.ln(10)

    # Split the text into lines and add each one
    for line in text:
        if re.findall(CHORD_REGEX, line):
            pdf.set_font("Helvetica", style='B', size=10)
            pdf.cell(0, 4, line, ln=True)
            continue

        pdf.set_font("Helvetica", size=10)
        pdf.cell(0, 4, line, ln=True)

    pdf.output(output_filename)
    return True


def is_chord_line(line: str) -> bool:
    tokens = line.replace("(", "").replace(")", "").split()
    if not tokens:
        return False
    chord_count = sum(bool(re.match(CHORD_REGEX, t)) for t in tokens)
    return chord_count > 0 and chord_count / len(tokens) >= 0.5


def make_pdf(song_name: str, sequence: list, id_map_stanzas: dict, song_key: str):
    name_file = song_name.replace(" ", "").replace("/", "_") + f'({song_key})' + ".pdf"

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font(DEFAULT_FONT, style='B', size=20)
    pdf.cell(0, 15, song_name, align="C", ln=True)

    pdf.set_font(DEFAULT_FONT, style='B', size=14)
    pdf.cell(0, 2, f"Ordem: {' '.join(sequence)}", ln=True)
    pdf.ln(3)

    if id_map_stanzas.get(0):
        pdf.set_text_color(255, 0, 0)
        pdf.set_font(DEFAULT_FONT, style='B', size=12)
        pdf.cell(0, 8, f"{'  |  '.join(map(str.strip, id_map_stanzas.pop(0)))}", ln=True)

    for index, stanza in id_map_stanzas.items():
        pdf.ln(2)

        pdf.set_text_color(255, 0, 0)
        pdf.set_font(DEFAULT_FONT, style='B', size=15)
        pdf.cell(5, 5, f"{index}. ", ln=0)

        for line in stanza:
            if is_chord_line(line):
                pdf.set_text_color(255, 0, 0)
                pdf.set_font(DEFAULT_FONT, style='B', size=12)
                pdf.set_x(20)
                pdf.cell(0, 5, line, ln=1)

            else:
                pdf.set_text_color(0, 0, 0)
                pdf.set_font(DEFAULT_FONT, size=12)
                pdf.set_x(20)
                pdf.cell(0, 5, line, ln=1)

    check_folder()
    path_to_save = str(current_folder / PDF_FOLDER / name_file)
    pdf.output(path_to_save)
    return True
