from flask import Flask, render_template, request, session, redirect, url_for
import json

from helpers import (
    city_has_content,
    country_city_count,
    food_items,
    localized_name,
    tip_downloads,
    tip_text,
)
import helpers
from i18n import t

app = Flask(__name__)
app.secret_key = "rejseguide-dev-key"

with open("data.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

COUNTRY_CODES = {
    "thailand": "TH",
    "vietnam": "VN",
    "bali": "ID",
    "australia": "AU",
}


def get_lang():
    lang = session.get("lang", "da")
    return lang if lang in ("da", "en") else "da"


@app.context_processor
def inject_globals():
    lang = get_lang()
    return {
        "lang": lang,
        "t": lambda key: t(key, lang),
        "other_lang": "en" if lang == "da" else "da",
    }


@app.template_global()
def localized(value):
    return helpers.localized(value, get_lang())


@app.before_request
def set_language():
    requested = request.args.get("lang")
    if requested in ("da", "en"):
        session["lang"] = requested


@app.route("/set-lang/<lang_code>")
def set_lang(lang_code):
    if lang_code in ("da", "en"):
        session["lang"] = lang_code
    return redirect(request.referrer or url_for("index"))


@app.route("/")
def index():
    lang = get_lang()
    destinations = []
    for slug, country in DATA.items():
        city_count = country_city_count(country)
        destinations.append(
            {
                "slug": slug,
                "name": localized_name(country.get("name"), lang),
                "code": COUNTRY_CODES.get(slug, slug[:2].upper()),
                "city_count": city_count,
                "has_content": city_count > 0,
            }
        )
    return render_template("index.html", destinations=destinations)


@app.route("/destination/<country_slug>")
def country(country_slug):
    lang = get_lang()
    country_data = DATA.get(country_slug)
    if not country_data:
        return redirect(url_for("index"))

    cities = []
    for city_slug, city in (country_data.get("cities") or {}).items():
        cities.append(
            {
                "slug": city_slug,
                "name": localized_name(city.get("name"), lang) or city_slug.replace("-", " ").title(),
                "has_content": city_has_content(city, lang),
            }
        )

    tips = []
    for tip in country_data.get("tips") or []:
        text = tip_text(tip, lang)
        if not text:
            continue
        tips.append({"text": text, "downloads": tip_downloads(tip)})

    return render_template(
        "country.html",
        country_slug=country_slug,
        country=country_data,
        country_name=localized_name(country_data.get("name"), lang),
        country_code=COUNTRY_CODES.get(country_slug, country_slug[:2].upper()),
        cities=cities,
        tips=tips,
        food=food_items(country_data.get("food"), lang),
        drinks=food_items(country_data.get("drinks"), lang),
    )


@app.route("/destination/<country_slug>/<city_slug>")
def city(country_slug, city_slug):
    lang = get_lang()
    country_data = DATA.get(country_slug)
    if not country_data:
        return redirect(url_for("index"))

    city_data = (country_data.get("cities") or {}).get(city_slug)
    if not city_data:
        return redirect(url_for("country", country_slug=country_slug))

    other_cities = []
    for slug, item in (country_data.get("cities") or {}).items():
        if slug == city_slug:
            continue
        if city_has_content(item, lang):
            other_cities.append(
                {
                    "slug": slug,
                    "name": localized_name(item.get("name"), lang) or slug.replace("-", " ").title(),
                }
            )

    city_tips = []
    for tip in city_data.get("tips") or []:
        text = tip_text(tip, lang)
        if text:
            city_tips.append(text)

    return render_template(
        "city.html",
        country_slug=country_slug,
        city_slug=city_slug,
        country_name=localized_name(country_data.get("name"), lang),
        country_code=COUNTRY_CODES.get(country_slug, country_slug[:2].upper()),
        city=city_data,
        city_name=localized_name(city_data.get("name"), lang) or city_slug.replace("-", " ").title(),
        city_tips=city_tips,
        other_cities=other_cities[:4],
    )


if __name__ == "__main__":
    app.run(debug=True)
