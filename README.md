# OCR-Translater
OCR-Translater is a local AI-based tool that translates scanned PDFs while preserving their formatting. 
It uses [PaddleOCR](https://github.com/PADDLEPADDLE/PADDLEOCR) for OCR and [translategemma](https://huggingface.co/mlx-community/translategemma-4b-it-4bit) for translation.

Currently, it only supports general horizontal text, as well as paragraphs and paragraph titles. 
The available languages are Japanese, English, and Chinese. (ja,en,zh)

> [!NOTE]
> This project is still under development, and some features may not work as expected.

# Features

- **Layout Preservation**: Translate scanned PDFs while preserving their original layout and formatting as much as possible.
- **Privacy-Friendly Local Processing**: Perform OCR and translation locally using AI models, reducing the need to send document contents to external services.
- **Runs on MacBooks**: Designed to run locally on MLX-compatible macOS devices, including MacBooks with Apple Silicon.

# Supported Environment

- Currently supports macOS environments where MLX is supported.
- Verified on a MacBook Air (M2) running macOS 26.4.1.
- Support for CUDA-enabled environments is under consideration for future development.

# Installation
```
$ git clone https://github.com/kouki-shito/ocr-translater.git
```
OCR-Translater uses [uv](https://docs.astral.sh/uv/) for package management. If you haven't installed it yet, please refer to [Installation](https://docs.astral.sh/uv/getting-started/installation/) to install it.

Navigate to the cloned project and run the following command.
```
$ uv sync
```

# Basic Usage
Run the script with the following command.
```
$ oc <pdf_file> <output_dir> <from_language> <to_language> [Options]
```
### Arguments

| Argument | Description |
|---|---|
| `pdf_file` | Path to the input PDF file. |
| `output_dir` | Path to the output directory. |
| `from_language` | Source language. Must be one of the supported languages. (ja,en,zh) |
| `to_language` | Target language. Must be one of the supported languages. (ja,en,zh) |
| `--font_regular` | *(Optional)* Path to the regular font file. |
| `--font_bold` | *(Optional)* Path to the bold font file. |

### Example
```
$ oc test.pdf ./output en ja
```
To specify custom fonts:
```
$ oc test.pdf ./output en ja \
    --font_regular /fonts/regular.ttf \
    --font_bold /fonts/bold.ttf
```
