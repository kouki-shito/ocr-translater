import cv2
import json
import numpy as np
from pathlib import Path
from natsort import natsorted
import shutil


def delete_text(temp_path: Path):
    json_path = temp_path / "json"
    jsons = natsorted(json_path.glob("*.json"))
    if len(jsons) == 0:
        raise ValueError("can't find json files from directory")
    processed_path = temp_path/"processed_image"
    if processed_path.exists():
        shutil.rmtree(processed_path)
    processed_path.mkdir(parents=True, exist_ok=True)
    for js in jsons:
        with open(js, 'r') as js_op:
            js_data = json.load(js_op)
            im_path = js_data["input_path"]
            parse = js_data["parsing_res_list"]
            img = cv2.imread(im_path)
            for content in parse:
                label = content["block_label"]
                text = content["block_content"]
                box = np.array(content["block_polygon_points"], dtype=np.int32)
                if label in ["table", "image", "header_image", "chart", "formula", "formula_number"] or "".join(text.split()) == "":
                    continue
                cv2.fillPoly(img, [box], (255, 255, 255))
            cv2.imwrite(processed_path / f"{Path(im_path).name}.png", img)
