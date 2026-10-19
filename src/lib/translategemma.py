from mlx_lm import load, stream_generate
from pathlib import Path
import json
from natsort import natsorted


def translate(temp_path: Path, from_lang: str, to_lang: str):
    json_path = temp_path / "json"
    jsons = natsorted(json_path.glob("*.json"))
    if len(jsons) == 0:
        raise ValueError("can't find json files from directory")
    translated_path = temp_path / f"translated_{to_lang}"
    translated_path.mkdir(parents=True, exist_ok=True)
    model, tokenizer = load("mlx-community/translategemma-4b-it-4bit")
    for js in jsons:
        save_path = translated_path / js.name
        if save_path.exists():
            continue
        with open(js, 'r') as js_op:
            js_data = json.load(js_op)
            parse = js_data["parsing_res_list"]
            print(f"translating: {save_path}")
            for i, content in enumerate(parse):
                label = content["block_label"]
                text = content["block_content"]
                if label in ["table", "image", "header_image", "chart", "formula", "formula_number"] or "".join(text.split()) == "":
                    continue
                prompt = [{
                    "type": "text",
                    "source_lang_code": from_lang,
                    "target_lang_code": to_lang,
                    "text": text,
                }]
                translated_texts = []
                if tokenizer.chat_template is not None:
                    messages = [{"role": "user", "content": prompt}]
                    prompt = tokenizer.apply_chat_template(
                        messages, add_generation_prompt=True
                    )
                for response in stream_generate(model, tokenizer, prompt=prompt):
                    token_text = response.text
                    if "<end_of_turn>" in token_text or "<eos>" in token_text:
                        break
                    translated_texts.append(token_text)
                    parse[i]["block_content"] = "".join(translated_texts)
            with open(save_path, 'w') as f:
                save_json = js_data
                save_json["parsing_res_list"] = parse
                json.dump(save_json, f, indent=2, ensure_ascii=False)
