"""
Flask web server for the wedding website.

Run: python -m src.app   (from project root, venv activated)
Then open: http://localhost:5000
"""
import os
from flask import Flask, render_template
from src.wedding_site import SITE, PAGE_ROUTES, get_page

app = Flask(__name__, template_folder="templates")


def render_wedding_page(slug):
    return render_template("index.html", site=SITE, page_slug=slug, page=get_page(slug))


def _register_wedding_routes():
    def page_view(slug):
        return lambda: render_wedding_page(slug)

    for slug, path in PAGE_ROUTES.items():
        app.add_url_rule(path, endpoint=f"wedding_{slug}", view_func=page_view(slug))


_register_wedding_routes()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
