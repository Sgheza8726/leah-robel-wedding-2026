# Wedding Website

This project is now a standalone Flask wedding website.

## Structure

`src/app.py`
Flask app setup and route registration.

`src/wedding_site.py`
Editable wedding content and route definitions.

`src/templates/index.html`
Main Jinja template.

`src/static/wedding.css`
Site styling.

## Run locally

Create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the server:

```bash
python -m src.app
```

Then open:

```text
http://127.0.0.1:5000
```

## Editing content

Most text, photos, and page structure live in `src/wedding_site.py`.

## Editing design

Update layout and styles in `src/templates/index.html` and `src/static/wedding.css`.
