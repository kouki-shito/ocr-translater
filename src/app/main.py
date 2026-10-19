from lib.pdf import make_pdf
from lib.ocr import ocr
from lib.image import delete_text
from lib.translategemma import translate
from lib.fonts import Fonts
from pathlib import Path
import argparse


def main():
    choice_langs = Fonts._member_names_
    parser = argparse.ArgumentParser()
    parser.add_argument('arg1', type=Path, help="pdf file path")
    parser.add_argument('arg2', type=Path, help="output file path")
    parser.add_argument(
        'arg3', choices=choice_langs, help="from language")
    parser.add_argument('arg4', choices=choice_langs, help="to language")
    parser.add_argument('--font_regular', type=Path, help="regular font file")
    parser.add_argument('--font_bold', type=Path, help="bold font file")
    args = parser.parse_args()
    pdf_path = args.arg1
    out_dir = args.arg2
    from_lang = args.arg3
    to_lang = args.arg4
    font_path_re = args.font_regular if args.font_regular is not None else Fonts[
        to_lang].value[0]
    font_path_bd = args.font_bold if args.font_bold is not None else Fonts[
        to_lang].value[1]
    if not (pdf_path.exists() and pdf_path.is_file() and pdf_path.suffix == ".pdf"):
        raise FileNotFoundError("指定したPDFパスが不正です")
    out_dir.mkdir(parents=True, exist_ok=True)
    ocr(out_dir, pdf_path)
    delete_text(out_dir)
    translate(out_dir, from_lang, to_lang)
    make_pdf(out_dir, to_lang, font_path_re, font_path_bd)
