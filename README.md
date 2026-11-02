# Cost Observation Frontend

Standalone Streamlit frontend repository for a separate FastAPI cost-observation backend.

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501. The backend must be running at `http://localhost:8000` and expose `GET /cost-analysis`. To change the backend address, set the `API_URL` environment variable before starting Streamlit (the `.env.example` is illustrative; it is not loaded automatically).

## Expected API JSON

```json
{
  "previous_month_total": 2900,
  "current_month_total": 3320,
  "estimated_savings": 180,
  "categories": [
    {"category": "Food", "previous": 500, "current": 550, "reason": "Possible grocery price increase"},
    {"category": "Utilities", "previous": 300, "current": 420, "reason": "Possible higher electricity usage"},
    {"category": "Shopping", "previous": 400, "current": 700, "reason": "Possible additional purchases"},
    {"category": "Rent", "previous": 1500, "current": 1500, "reason": "No change"},
    {"category": "Transport", "previous": 200, "current": 150, "reason": "Reduced travel"}
  ],
  "anomalies": [{"category": "Shopping", "message": "Unusual increase detected"}],
  "recommendations": [{"category": "Shopping", "recommendation": "Review non-essential purchases", "estimated_savings": 180}]
}
```

The frontend displays ML results returned by the backend; it does not train a model itself. Reasons and savings are estimates unless independently supported by data.
