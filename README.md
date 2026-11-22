# Jhelum Mess Roti Counter

The project includes a Python frontend built with Streamlit and the original static HTML frontend.

## Run the Python app

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

The Python app loads the starter observations from `roti_observations_template.csv`. New observations are saved to `data.csv` in the project folder and remain available on later runs. The Records page can export the observations as a CSV file.

The existing static frontend can still be opened by serving this folder, for example with `python3 -m http.server 4173`.

## Run the data-helper tests

```bash
python3 -m unittest
```
