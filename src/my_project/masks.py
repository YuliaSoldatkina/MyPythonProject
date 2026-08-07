import logging
from pathlib import Path

# РќР°СЃС‚СЂРѕР№РєР° Р»РѕРіРіРµСЂР°
LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "masks.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# РћР±СЂР°Р±РѕС‚С‡РёРє С„Р°Р№Р»Р° (РїРµСЂРµР·Р°РїРёСЃС‹РІР°РµС‚СЃСЏ РїСЂРё РєР°Р¶РґРѕРј Р·Р°РїСѓСЃРєРµ)
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Р¤РѕСЂРјР°С‚: РІСЂРµРјСЏ, РјРѕРґСѓР»СЊ, СѓСЂРѕРІРµРЅСЊ, СЃРѕРѕР±С‰РµРЅРёРµ
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    РњР°СЃРєРёСЂСѓРµС‚ РЅРѕРјРµСЂ Р±Р°РЅРєРѕРІСЃРєРѕР№ РєР°СЂС‚С‹.

    Р¤РѕСЂРјР°С‚:
        XXXX XX** **** XXXX

    РџСЂРёРјРµСЂ:
        '7000792289606361' -> '7000 79** **** 6361'
    """
    digits_only = card_number.replace(" ", "")
    # РћР¶РёРґР°РµРј, С‡С‚Рѕ РґР»РёРЅР° РєР°СЂС‚С‹ >= 10, РёРЅР°С‡Рµ РїСЂРѕСЃС‚Рѕ РІРµСЂРЅРµРј РєР°Рє РµСЃС‚СЊ
    if len(digits_only) < 10:
        return card_number

    # РџРµСЂРІС‹Рµ 6 Рё РїРѕСЃР»РµРґРЅРёРµ 4 С†РёС„СЂС‹
    first_4 = digits_only[:4]  # XXXX
    next_2 = digits_only[4:6]  # XX
    last_4 = digits_only[-4:]  # XXXX

    # Р¤РѕСЂРјР°С‚ СЃС‚СЂРѕРіРѕ РїРѕ Р·Р°РґР°РЅРёСЋ: XXXX XX** **** XXXX
    return f"{first_4} {next_2}** **** {last_4}"


def get_mask_account(account_number: str) -> str:
    """
    РњР°СЃРєРёСЂСѓРµС‚ РЅРѕРјРµСЂ Р±Р°РЅРєРѕРІСЃРєРѕРіРѕ СЃС‡РµС‚Р°.

    Р¤РѕСЂРјР°С‚:
        **XXXX

    РџСЂРёРјРµСЂ:
        '73654108430135874305' -> '**4305'
    """
    digits_only = account_number.replace(" ", "")
    if len(digits_only) <= 4:
        return account_number

    last_4 = digits_only[-4:]
    return f"**{last_4}"
