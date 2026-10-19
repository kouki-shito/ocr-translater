from paddleocr import PaddleOCRVL
import pymupdf
from pathlib import Path
import subprocess


def ocr(temp_path: Path, pdf_path: Path):
    doc = pymupdf.open(pdf_path)
    img_dir = temp_path / "image"
    img_dir.mkdir(parents=True, exist_ok=True)
    for page in doc:
        if (img_dir / f"{page.number}.png").exists():
            continue
        pix = page.get_pixmap()
        pix.save(img_dir / f"{page.number}.png")
    server = subprocess.Popen(
        ["uv", "run", "mlx_vlm.server", "--port", "8111"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ocr = PaddleOCRVL(vl_rec_backend="mlx-vlm-server", vl_rec_server_url="http://localhost:8111/",
                      vl_rec_api_model_name="PaddlePaddle/PaddleOCR-VL-1.6")
    image_paths = sorted(map(str, temp_path.glob(
        "image/*.png")), key=lambda x: int(Path(x).stem))
    if len(image_paths) == 0:
        raise ValueError("PDF Images Not Found")
    json_dir = temp_path / "json"
    json_dir.mkdir(parents=True, exist_ok=True)
    for i in image_paths:
        if (json_dir / f"{Path(i).stem}_res.json").exists():
            continue
        result = ocr.predict(i)
        for res in result:
            res.print()
            res.save_to_json(json_dir)
        print(f"finish {i}")
    server.terminate()
    print(f"Saved temp json to {json_dir}")
