import sys
from pathlib import Path
import webbrowser

import PySimpleGUI as sg
import requests
from readabilipy import simple_json_from_html_string
from weasyprint import CSS, HTML

# Bckground, Foreground
COLORS = {
    "dark-blue": ["#2b2d37", "#c5cdd9"],
    "atom-light": ["#f8f8f8", "#a3a3a6"],
    "gruvbox-dark": ["#282828", "#ebdbb2"],
    "gruvbox-light": ["#fbf1c7", "#3c3836"],
    "dracula": ["#282a36", "#f8f8f2"],
}


def url_to_pdf(url, background_color, font_color):
    response = requests.get(url)

    try:
        doc = simple_json_from_html_string(response.text, use_readability=True)
    except Exception:
        print("Error while parsing article...")
        sys.exit(1)

    doc_title = doc["title"]
    doc_byline = doc["byline"]
    doc_content = doc["content"]

    if doc_title is None and doc_byline is None and doc_content is None:
        print("Could not parse article...")
        sys.exit(1)

    html_out = ""

    if doc_title is not None:
        print("Title: ", doc_title)
        html_out += f"<h1>{doc_title}</h1>"

    if doc_byline is not None:
        print("By Line: ", doc_byline)

    if doc_content is not None:
        html_out += doc_content

    page_css = CSS(
        string="""
        @page {
            background-color: """ + background_color + """;
        }

        body {
            color: """ + font_color + """;
        }

        img{
            width: 100%;
        }
    """
    )

    HTML(string=html_out).write_pdf("output.pdf", stylesheets=[page_css])

    out_filepath = Path.cwd() / "output.pdf"
    webbrowser.open(out_filepath.as_uri())


def main():
    layout = [
        [sg.Text("Book Downloader")],
        [sg.Text("URL: "), sg.InputText()],
        [sg.Text("Theme: "), sg.Combo(list(COLORS.keys()))],
        [sg.Button("Download"), sg.Button("Close")],
    ]

    window = sg.Window("Web Page to Book", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Close":
            break
        elif event == "Download":
            print("You entered", values[0])
            url_to_pdf(values[0], COLORS[values[1]][0], COLORS[values[1]][1])
    window.close()


if __name__ == "__main__":
    main()
