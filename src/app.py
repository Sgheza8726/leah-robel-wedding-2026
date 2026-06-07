"""
Flask web server for the wedding website.

Run: python -m src.app   (from project root, venv activated)
Then open: http://localhost:5000
"""
import csv
import os
from datetime import datetime, UTC
from pathlib import Path
from flask import Flask, redirect, render_template, request, url_for
from src.wedding_site import SITE, PAGE_ROUTES, get_page

app = Flask(__name__, template_folder="templates")
RSVP_STORAGE_PATH = Path(os.environ.get("RSVP_STORAGE_PATH", "data/rsvps.csv"))
RSVP_FIELDS = [
    "submitted_at",
    "guest_name",
    "email",
    "phone",
    "attending",
    "guest_count",
    "guest_names",
    "dietary_notes",
]


def _empty_rsvp_form():
    return {
        "guest_name": "",
        "email": "",
        "phone": "",
        "attending": "yes",
        "guest_count": "1",
        "guest_names": "",
        "dietary_notes": "",
    }


def _store_rsvp(form_data):
    RSVP_STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_exists = RSVP_STORAGE_PATH.exists()
    with RSVP_STORAGE_PATH.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=RSVP_FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "submitted_at": datetime.now(UTC).isoformat(),
                "guest_name": form_data["guest_name"],
                "email": form_data["email"],
                "phone": form_data["phone"],
                "attending": form_data["attending"],
                "guest_count": form_data["guest_count"],
                "guest_names": form_data["guest_names"],
                "dietary_notes": form_data["dietary_notes"],
            }
        )


def _get_rsvp_context():
    return {
        "success": request.args.get("submitted") == "1",
        "error": request.args.get("error"),
        "form_data": _empty_rsvp_form(),
    }


def render_wedding_page(slug, **extra_context):
    context = {"site": SITE, "page_slug": slug, "page": get_page(slug)}
    context.update(extra_context)
    return render_template("index.html", **context)


@app.post("/rsvp")
def submit_rsvp():
    form_data = {
        "guest_name": request.form.get("guest_name", "").strip(),
        "email": request.form.get("email", "").strip(),
        "phone": request.form.get("phone", "").strip(),
        "attending": request.form.get("attending", "yes").strip() or "yes",
        "guest_count": request.form.get("guest_count", "1").strip() or "1",
        "guest_names": request.form.get("guest_names", "").strip(),
        "dietary_notes": request.form.get("dietary_notes", "").strip(),
    }

    if not form_data["guest_name"] or not form_data["email"]:
        return render_wedding_page(
            "rsvp",
            rsvp={"success": False, "error": "Please fill in your name and email.", "form_data": form_data},
        ), 400

    _store_rsvp(form_data)
    return redirect(url_for("wedding_rsvp", submitted="1"))


def _register_wedding_routes():
    def page_view(slug):
        def view():
            extra_context = {"rsvp": _get_rsvp_context()} if slug == "rsvp" else {}
            return render_wedding_page(slug, **extra_context)

        return view

    for slug, path in PAGE_ROUTES.items():
        app.add_url_rule(path, endpoint=f"wedding_{slug}", view_func=page_view(slug))


_register_wedding_routes()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
