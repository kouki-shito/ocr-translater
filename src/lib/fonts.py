from enum import Enum
from config.paths import PROJECT_ROOT

f_path = PROJECT_ROOT / "fonts"


class Fonts(Enum):
    ja = (f_path / "NotoSansJP-Regular.ttf", f_path / "NotoSansJP-Bold.ttf")
    en = (f_path / "OpenSans-Regular.ttf", f_path / "OpenSans-Bold.ttf")
    zh = (f_path / "NotoSansSC-Regular.ttf", f_path / "NotoSansSC-Bold.ttf")
