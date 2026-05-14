# Tablora

Tablora is a lightweight web app for turning spreadsheets into clean, exportable charts — without writing a single line of code.

Upload a `.csv` or `.xlsx` file, pick your variables and chart type, and download the result as PNG, PDF, or SVG.

## Features

- Import CSV or Excel files (auto-detects decimal separator)
- Generate line, bar, scatter, and pie charts
- Export to PNG, PDF, or SVG
- User accounts with saved dashboards (Supabase)
- French-language UI

## Tech Stack

- **Frontend / App framework:** [Streamlit](https://streamlit.io/)
- **Data:** pandas, numpy, openpyxl
- **Charts:** matplotlib, plotly, seaborn
- **Auth & storage:** Supabase (Postgres + Auth)
- **Session:** cookie-based via `streamlit-cookies-controller`

## Project Structure

```
.
├── Accueil.py            # Landing page (home)
├── graph_generator.py    # File loading + chart generation
├── pages/                # Multi-page Streamlit routes
│   ├── 1_Login.py
│   ├── 2_Creer.py        # Chart creation flow
│   ├── 4_Dashboard.py
│   └── ...               # Legal pages (CGU, LPD, mentions légales)
├── utils/                # CSS loader, footer, cached helpers
├── styles/style.css
└── requirements.txt
```

## License

Open source — see repository for details.
