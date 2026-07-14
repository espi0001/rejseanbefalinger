"""Helpers for reading localized content from travel data."""


def normalize_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if item and str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


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


def localized_name(value, lang, fallback="da"):
    items = localized(value, lang, fallback)
    return items[0] if items else ""


def has_content(value, lang):
    return bool(localized(value, lang))


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


def tip_text(tip, lang):
    if isinstance(tip, dict):
        if "text" in tip:
            return localized(tip.get("text"), lang)
        if "da" in tip or "en" in tip:
            return localized(tip, lang)
    return normalize_list(tip)


def tip_downloads(tip):
    if not isinstance(tip, dict):
        return []
    return [item for item in (tip.get("download") or []) if item.get("url")]


def food_items(food, lang="da"):
    if not food:
        return []
    if isinstance(food, dict) and ("da" in food or "en" in food):
        return localized(food, lang)
    items = []
    for entry in food:
        if isinstance(entry, dict):
            names = entry.get("name")
            if isinstance(names, list):
                items.extend(names)
            elif isinstance(names, str) and names.strip():
                items.append(names.strip())
        elif isinstance(entry, str) and entry.strip():
            items.append(entry.strip())
    return items
