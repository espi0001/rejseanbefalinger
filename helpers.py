"""Helpers for reading localized content from travel data."""


# Gør en værdi (string, liste eller None) om til en ren liste af ikke-tomme strenge
def normalize_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if item and str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


# Henter den sprog-specifikke udgave af et felt (fx {"da": ..., "en": ...}),
# falder tilbage til dansk hvis det ønskede sprog mangler
def localized(value, lang, fallback="da"):
    if value is None:
        return []

    if isinstance(value, dict):
        if lang in value:
            return normalize_list(value[lang])
        if fallback in value:
            return normalize_list(value[fallback])
        return []

    return normalize_list(value)


# Som localized(), men returnerer kun det første element (til fx navne)
def localized_name(value, lang, fallback="da"):
    items = localized(value, lang, fallback)
    return items[0] if items else ""


def has_content(value, lang):
    return bool(localized(value, lang))


# Tjekker om en by har noget vist indhold på det aktuelle sprog,
# så tomme byer kan vises som "coming soon" i stedet for et tomt link
def city_has_content(city, lang):
    sections = ("tips", "activities", "byen", "restaurants", "accommodation")
    for section in sections:
        items = city.get(section) or []
        if section == "tips":
            for tip in items:
                if isinstance(tip, dict):
                    if has_content(tip.get("text"), lang):
                        return True
                    if has_content(tip, lang):
                        return True
                elif str(tip).strip():
                    return True
            continue

        for item in items:
            if not isinstance(item, dict):
                if str(item).strip():
                    return True
                continue
            if item.get("name") and str(item["name"]).strip():
                if section == "accommodation":
                    return True
                if has_content(item.get("description"), lang):
                    return True
                if section == "accommodation" and (
                    has_content(item.get("pros"), lang)
                    or has_content(item.get("cons"), lang)
                ):
                    return True
    return False


def country_city_count(country):
    return len(country.get("cities") or {})


# Tip-teksten kan ligge direkte, under "text", eller som {"da": ..., "en": ...}
def tip_text(tip, lang):
    if isinstance(tip, dict):
        if "text" in tip:
            return localized(tip.get("text"), lang)
        if "da" in tip or "en" in tip:
            return localized(tip, lang)
    return normalize_list(tip)


# App-anbefalinger tilknyttet et tip (kun dem der faktisk har en URL)
def tip_downloads(tip):
    if not isinstance(tip, dict):
        return []
    return [item for item in (tip.get("download") or []) if item.get("url")]


# Mad/drikke-items som rigtige kort (samme facon som activities/restaurants),
# så de kan vises og linkes til på samme måde. Bevarer 1:1 rækkefølge med den
# rå liste i data.json, så index'et matcher det country_item-routen bruger.
def food_items(items, lang="da"):
    result = []
    for entry in items or []:
        if isinstance(entry, dict):
            result.append(
                {
                    "name": localized_name(entry.get("name"), lang),
                    "link": entry.get("link", ""),
                    "description": entry.get("description"),
                    "images": entry.get("images") or [],
                }
            )
        else:
            result.append({"name": str(entry), "link": "", "description": None, "images": []})
    return result


# Slår et item op på dens plads i en sektion (activities/byen/restaurants/
# accommodation/food/drinks). Bruges af single-page-routen; returnerer None
# hvis index er ugyldigt, så routen kan sende brugeren tilbage
def get_section_item(items, index):
    items = items or []
    if 0 <= index < len(items) and isinstance(items[index], dict):
        return items[index]
    return None
