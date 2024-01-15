# prompt: need flask showing the home page

from flask import Flask, render_template, request, redirect, url_for
import requests
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

import os

app = Flask(__name__, static_folder='tmp/static',)


def process_and_save_html(
    base_url, form_data, classes_to_remove, tag_list, output_filename
):
    encoded_data = urllib.parse.urlencode(form_data).encode("utf-8")
    request = urllib.request.Request(base_url, method="POST", data=encoded_data)
    response = urllib.request.urlopen(request)
    html = response.read()

    soup = BeautifulSoup(html, "html.parser")

    for class_to_remove in classes_to_remove:
        for element in soup.find_all(class_=class_to_remove):
            element.decompose()

    for tag in soup.find_all(tag_list):
        tag.decompose()
    enx_image_tags = soup.find_all("enx-image")
    for enx_image_tag in enx_image_tags:
        source_tags = enx_image_tag.find_all("source")
        for source_tag in source_tags:
            relative_path = source_tag.get("data-srcset")
            if relative_path:
                complete_url = urllib.parse.urljoin(
                    "https://www.prokerala.com/", relative_path
                )
                source_tag["data-srcset"] = complete_url
        img_tags = enx_image_tag.find_all("img")
        for img_tag in img_tags:
            relative_path = img_tag.get("src")
            if relative_path:
                complete_url = urllib.parse.urljoin(
                    "https://www.prokerala.com/", relative_path
                )
                img_tag["src"] = complete_url

    img_tags = soup.find_all("img")
    for img_tag in img_tags:
        relative_path = img_tag.get("src")
        if relative_path:
            complete_url = urllib.parse.urljoin(
                "https://www.prokerala.com/", relative_path
            )
            img_tag["src"] = complete_url

    # Specify the desired output directory (use a different directory, e.g., 'generated_files')
    output_directory = os.path.join("/tmp", "static")

    # Ensure that the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Specify the output filename
    output_filename = os.path.join(output_directory, output_filename.replace("#", ""))
    print('>>>>>>>>>>>',output_filename)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(str(soup))

def foo(formdata):
    formaction_paths = [
        "/astrology/kundli/#panchang-predictions",
        "/astrology/birth-chart/navamsa-chart.php",
        "/astrology/nakshatra-finder/",
        "/astrology/mangal-dosha/manglik.php",
        "/astrology/kundli/#dasha",
        "/astrology/kundli/#varga-chart",
        "/astrology/ashtakavarga.php",
        "/astrology/birth-chart/",
    ]

    s = {
        0: [
            "adm-unit clearfix",
            "wdgt-group-inner",
            "app-top-navigation-sticky",
            "full-width app-bottom-navigation",
            "shadow",
            "compact",
            "section-title",
            "adm-wrapper",
            "mt-3",
            "compact",
            "astrologer-list-slider",
            "astrology-related-reports",
        ],
        1: [
            "adm-unit clearfix",
            "wdgt-group-inner",
            "app-top-navigation-sticky",
            "full-width app-bottom-navigation",
            "shadow",
            "compact",
            "section-title",
            "adm-wrapper",
            "mt-3",
            "compact",
            "astrologer-list-slider",
            "astrology-related-reports",
            "list-wrapper",
        ],
        2: [
            "adm-unit clearfix",
            "wdgt-group-inner",
            "app-top-navigation-sticky",
            "app-bottom-navigation",
            "list-wrapper",
            "section-title",
            "adm-wrapper",
            "mt-3",
            "tc",
            "tab-content",
        ],
        3: [
            "adm-unit clearfix",
            "wdgt-group-inner",
            "full-width app-bottom-navigation",
            "list-wrapper",
            "section-title",
            "adm-wrapper",
            "mt-3",
            "compact",
            "pad-large",
            "app-top-navigation-sticky",
            "item-block",
        ],
        4: [
            "adm-unit clearfix",
            "wdgt-group-inner",
            "full-width app-bottom-navigation",
            "list-wrapper",
            "shadow",
            "section-title",
            "adm-wrapper",
            "mt-3",
            "compact",
            "pad-large",
            "tab-content",
            "app-top-navigation-sticky",
        ],
        5: [
            "adm-unit clearfix",
            "wdgt-group-inner",
            "full-width app-bottom-navigation",
            "section-title",
            "adm-wrapper",
            "mt-3",
            "compact",
            "pad-large",
            "shadow",
            "astrologer-list-slider",
            "astrology-related-reports",
            "t-small",
            "app-top-navigation-sticky",
        ],
        6: [
            "adm-unit clearfix",
            "wdgt-group-inner",
            "full-width app-bottom-navigation",
            "section-title",
            "adm-wrapper",
            "mt-3",
            "compact",
            "astrologer-list-slider",
            "astrology-related-reports",
            "t-small",
            "app-top-navigation-sticky",
        ],
        7: [
            "adm-unit clearfix",
            "wdgt-group-inner",
            "app-top-navigation-sticky",
            "full-width app-bottom-navigation",
            "shadow",
            "compact",
            "section-title",
            "adm-wrapper",
            "mt-3",
            "compact",
            "astrologer-list-slider",
            "astrology-related-reports",
            "list-wrapper",
        ],
    }

    t = {
        0: ["aside", "header", "footer", "dialog"],
        1: ["aside", "header", "footer", "dialog"],
        2: ["aside", "section", "header", "footer", "dialog", "ul", "enx-image"],
        3: ["aside", "section", "header", "footer", "dialog"],
        4: ["aside", "header", "footer", "dialog"],
        5: ["aside", "header", "footer", "dialog"],
        6: ["aside", "header", "footer", "dialog"],
        7: ["aside", "header", "footer", "dialog"],
    }

    for formaction_path in formaction_paths:
        url = "https://www.prokerala.com" + formaction_path
        if formaction_path.endswith("/"):
            output_filename = formaction_path.split("/")[-2] + ".html"
        else:
            output_filename = formaction_path.split("/")[-1] + ".html"

        if formaction_path == formaction_paths[0]:
            formdata["calculation"] = "panchang-predictions"
        elif formaction_path == formaction_paths[4]:
            formdata["calculation"] = "dasha"
        elif formaction_path == formaction_paths[5]:
            formdata["calculation"] = "varga-chart"

        classes_to_remove = s[formaction_paths.index(formaction_path)]
        tag_list = t[formaction_paths.index(formaction_path)]
        output_filename = output_filename.replace("#", "")
        process_and_save_html(
            url, formdata, classes_to_remove, tag_list, output_filename
        )
    print(f"URL: {url}")
    print(f"FormData: {formdata}")
    print(f"Classes to Remove: {classes_to_remove}")
    print(f"Tag List: {tag_list}")
    print(f"Output Filename: {output_filename}")

    return render_template("results.html")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/submit_form", methods=["POST"])
def submit_form():
    loc = request.form.get("place")
    name = request.form.get("name")
    gender = request.form.get("gender")
    day = request.form.get("day")
    month = request.form.get("month")
    year = request.form.get("year")
    hour = request.form.get("hour")
    minute = request.form.get("min")
    apm = request.form.get("apm")
    r = requests.get(
        "https://www.prokerala.com/astrology/search.php?index=0&q=" + str(loc)
    )
    print(r)
    soup = BeautifulSoup(r.content, "html.parser")
    g = soup.prettify()
    f = g.split(",")[0]
    s = f.split("|")[0]
    h = ""
    numbers = [c for c in s if c.isdigit()]
    geoID = "".join(numbers)

    result = {
        "loc": geoID,
        "location": loc,
        "name": name,
        "gender": gender,
        "day": day,
        "month": month,
        "year": year,
        "hour": hour,
        "min": minute,
        "apm": apm,
        "chart_format": "south-indian",
        "locale": "ta",
        "p": "1",
        "utm_source": "Birth_Chart",
        "utm_medium": "",
        "utm_campaign": "",
        "calculation": "",
    }
    print(result)
    return foo(result)


if __name__ == "__main__":
    app.run(debug=True)
