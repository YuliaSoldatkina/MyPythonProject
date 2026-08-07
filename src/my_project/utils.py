"""РЈС‚РёР»РёС‚С‹ РґР»СЏ РѕР±СЂР°Р±РѕС‚РєРё С‚СЂР°РЅР·Р°РєС†РёР№."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

# РќР°СЃС‚СЂРѕР№РєР° Р»РѕРіРіРµСЂР°
LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "utils.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# РћР±СЂР°Р±РѕС‚С‡РёРє С„Р°Р№Р»Р° (РїРµСЂРµР·Р°РїРёСЃС‹РІР°РµС‚СЃСЏ РїСЂРё РєР°Р¶РґРѕРј Р·Р°РїСѓСЃРєРµ)
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Р¤РѕСЂРјР°С‚: РІСЂРµРјСЏ, РјРѕРґСѓР»СЊ, СѓСЂРѕРІРµРЅСЊ, СЃРѕРѕР±С‰РµРЅРёРµ
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def load_transactions(filepath: str) -> List[Dict[str, Any]]:
    """
    Р—Р°РіСЂСѓР¶Р°РµС‚ СЃРїРёСЃРѕРє С„РёРЅР°РЅСЃРѕРІС‹С… С‚СЂР°РЅР·Р°РєС†РёР№ РёР· JSON-С„Р°Р№Р»Р°.

    Р•СЃР»Рё С„Р°Р№Р» РЅРµ РЅР°Р№РґРµРЅ, РїСѓСЃС‚РѕР№, РёР»Рё РІ РЅС‘Рј РЅРµ СЃРїРёСЃРѕРє,
    РІРѕР·РІСЂР°С‰Р°РµС‚ РїСѓСЃС‚РѕР№ СЃРїРёСЃРѕРє.
    """
    logger.info("Р—Р°РіСЂСѓР·РєР° С‚СЂР°РЅР·Р°РєС†РёР№ РёР· %s", filepath)
    path = Path(filepath)

    if not path.exists():
        logger.warning("Р¤Р°Р№Р» РЅРµ РЅР°Р№РґРµРЅ: %s", filepath)
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.error("РћС€РёР±РєР° РїСЂРё С‡С‚РµРЅРёРё С„Р°Р№Р»Р°: %s", e)
        return []

    if not isinstance(data, list):
        logger.warning("Р¤Р°Р№Р» СЃРѕРґРµСЂР¶РёС‚ РЅРµ СЃРїРёСЃРѕРє")
        return []

    logger.info("Р—Р°РіСЂСѓР¶РµРЅРѕ %d С‚СЂР°РЅР·Р°РєС†РёР№", len(data))
    return data
