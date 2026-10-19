import pymupdf
import cv2
import json
import numpy as np
from pathlib import Path
from natsort import natsorted


def _searchFontSize(text: str, text_rect: pymupdf.Rect, page_rect: pymupdf.Rect, font_path: Path, min_size=1, max_size=300) -> int:
    pdf = pymupdf.open()
    page = pdf.new_page(width=page_rect.width, height=page_rect.height)
    page.insert_font(fontname="myfont", fontfile=font_path)
    low = min_size
    high = max_size
    best = min_size
    while low <= high:
        mid = (low + high) // 2
        result = page.insert_textbox(
            text_rect, text, fontname="myfont", fontsize=mid)
        if result >= 0:
            best = mid
            low = mid + 1
        else:
            high = mid - 1
    pdf.close()
    return best


def make_pdf(temp_path: Path, to_lang: str, regular_font_path: Path, bold_font_path: Path):
    translated_json_path = temp_path / f"translated_{to_lang}"
    jsons = natsorted(translated_json_path.glob("*.json"))
    if len(jsons) == 0:
        raise ValueError("can't find translated json files from directory")
    pdf = pymupdf.open()
    for js in jsons:
        with open(js, "r") as js_op:
            js_data = json.load(js_op)
            im_path = js_data["input_path"]
            parse = js_data["parsing_res_list"]
            img = cv2.imread(im_path)
            text_blocks = []
            for content in parse:
                label = content["block_label"]
                text = content["block_content"]
                box = np.array(content["block_polygon_points"], dtype=np.int32)
                if label in ["table", "image", "header_image", "chart", "formula", "formula_number"] or "".join(text.split()) == "":
                    continue
                cv2.fillPoly(img, [box], (255, 255, 255))
                text_blocks.append({
                    "label": label,
                    "text": text,
                    "box": box
                })
            _, img_bytes = cv2.imencode(".png", img)
            pixmap = pymupdf.Pixmap(im_path)
            page = pdf.new_page(
                width=pixmap.width,
                height=pixmap.height
            )
            page.insert_font(fontname="regular", fontfile=regular_font_path)
            page.insert_font(fontname="bold", fontfile=bold_font_path)
            page.insert_image(page.rect, stream=img_bytes.tobytes())
            for block in text_blocks:
                label = block["label"]
                text = block["text"]
                box = block["box"]
                fnt_path = regular_font_path
                fnt_name = "regular"
                if label in ["paragraph_title"]:
                    fnt_path = bold_font_path
                    fnt_name = "bold"
                text_rect = pymupdf.Rect(
                    x0=box[0][0], y0=box[0][1], x1=box[2][0], y1=box[2][1]).normalize()
                font_size = _searchFontSize(
                    text, text_rect, page.rect, fnt_path)
                page.insert_textbox(text_rect, text,
                                    fontname=fnt_name, fontsize=font_size)
    pdf.save(temp_path / f"translated_{to_lang}.pdf")
    print(f"saved translated_{to_lang}.pdf")
