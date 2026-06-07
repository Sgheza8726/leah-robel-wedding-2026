# Leah x Robel Wedding 2026

A shareable Flask wedding website project for Robel and Leah.

This repo contains a lightweight multi-page wedding site with a custom homepage, story page, RSVP page, schedule, travel details, accommodations, Q&A, and moments gallery.

## Overview

The site is built to be easy to customize without digging through a large codebase.

- Edit wedding content in `src/wedding_site.py`
- Edit page structure in `src/templates/index.html`
- Edit styling in `src/static/wedding.css`
- Run the app locally with Flask from `src/app.py`

## Project Structure

```text
src/
├── app.py              Flask app and route registration
├── wedding_site.py     Wedding content, page data, and route map
├── static/
│   └── wedding.css     Site styles
└── templates/
    └── index.html      Main Jinja template
```

## Local Development

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the site:

```bash
python -m src.app
```

Open:

```text
http://127.0.0.1:5000
```

If port `5000` is already in use on your machine, start Flask on another port:

```bash
PORT=43210 python -m src.app
```

## Customizing The Site

### Update text and images

Most editable content lives in `src/wedding_site.py`, including:

- couple name
- navigation labels
- hero and cover images
- welcome copy
- story timeline
- RSVP text
- schedule details
- travel and accommodations notes
- Q&A entries
- gallery images

### Update the design

Use `src/static/wedding.css` to change:

- colors
- spacing
- typography
- layout behavior
- mobile styling

Use `src/templates/index.html` if you want to change the HTML structure itself.

## Notes

- The project is intentionally simple and static-first.
- It now uses a mix of local static image assets and remote/public image sources.
- RSVP is handled directly in the Flask app and saved to a CSV file by default.

## Suggested Shareable Repo Name

If you want the GitHub repo name to feel a little cleaner publicly, a stronger option would be:

`leah-robel-wedding-2026`
