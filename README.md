# MonsterBox v1

This repository contains a small example of a slot game monitoring service with a Flask backend and minimal frontend.

## Structure

- `slot-monitor-site/app.py` - Main Flask application
- `slot-monitor-site/models.py` - SQLAlchemy models
- `slot-monitor-site/auth.py` - Registration and login routes producing JWTs
- `slot-monitor-site/api_client.py` - Wrapper for third party API calls
- `slot-monitor-site/routes/game.py` - Blueprint with balance/bet/win endpoints
- `slot-monitor-site/routes/admin.py` - Admin endpoints protected by JWT
- `slot-monitor-site/routes/user.py` - Recharge and transaction history APIs
- `slot-monitor-site/templates/index.html` - Web page showing jackpot logs
- `slot-monitor-site/static/style.css` - Shared styling
- `slot-monitor-site/static/login.css` - Login page styling
- `slot-monitor-site/slot_jackpot_log.txt` - Example log file

## Running

Install dependencies and start the server:

```bash
pip install flask flask_sqlalchemy pyjwt requests werkzeug
python slot-monitor-site/app.py
```

Then open `http://localhost:5000` in a browser to view the logs.

Visit `http://localhost:5000/login` to sign in. A valid JWT token will be stored
in the browser and used to access the admin dashboard at
`http://localhost:5000/admin`. The dashboard includes basic charts powered by
Chart.js and a paginated user table.
The interface supports basic English/Chinese translations and can be branded via
environment variables `BRAND_NAME` and `DEFAULT_LANGUAGE` defined in
`config.py`.

Use `/auth/register` and `/auth/login` to obtain a JWT. Include the token in an
`Authorization: Bearer <token>` header when calling `/api/admin/*` endpoints.
You can simulate deposits via `POST /api/user/recharge` and view history with
`GET /api/user/transactions?user_id=<id>`.
