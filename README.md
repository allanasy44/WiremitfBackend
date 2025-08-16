# Wiremit Forex Rate Aggregator

Backend service that aggregates forex rates from multiple public APIs, computes an average, applies a markup, and exposes secured endpoints.

## Tech

- Django 5, Django REST Framework
- JWT auth with `djangorestframework-simplejwt`
- Celery + Redis for async and hourly refresh (celery-beat)
- PostgreSQL for persistence
- drf-yasg (Swagger/Redoc) for API docs
- Gunicorn + Whitenoise for prod serving

## Why JWT?

Stateless, horizontally scalable, works well behind load balancers and with mobile/SPA clients. Refresh tokens let us rotate access securely.

## Endpoints

- `POST /signup` → create user, returns `{ 'access', 'refresh' }`
- `POST /login` → get tokens for existing user
- `GET /rates` → latest rate per pair (USD-GBP, USD-ZAR, ZAR-GBP) **auth required**
- `GET /rates/<currency>` where `<currency>` is one of `USD-GBP`, `USD-ZAR`, `ZAR-GBP` **auth required**
- `GET /historical/rates?pair=<pair>&page=<n>` → paginated history **auth required**
- `POST /admin/refresh` → admin-only, trigger async refresh now

## Aggregation Logic

We query 3 public APIs (configurable via env):

- `FX_API_1` default `https://api.exchangerate.host/latest?base=USD`
- `FX_API_2` default `https://open.er-api.com/v6/latest/USD`
- `FX_API_3` default `https://api.exchangerate-api.com/v4/latest/USD`

We normalize responses to USD→target. For each pair we compute:

```
average = mean(samples)
final = average * (1 + MARKUP)      # MARKUP default = 0.10
```

Cross rate:

```
ZAR-GBP = (USD-GBP) / (USD-ZAR)
```

We store each aggregated `final` into the `Rate` table with JSON of the samples.

## Hourly Refresh

Scheduled in `CELERY_BEAT_SCHEDULE` to call `rates.tasks.refresh_rates_task` every hour at minute 0.
You can also call `/admin/refresh` as a superuser to enqueue a refresh.

## Security

- Secrets via env vars, `.env.example` provided.
- Auth-required endpoints enforce `IsAuthenticated`.
- Admin endpoint uses `IsAdminUser`.
- Rate limits (per-user/per-anon) configured in DRF settings.
- DB creds come from env; do not commit real secrets.

## Run locally (Docker)

```bash
docker-compose build
docker-compose up
```

Then open:

- API: http://localhost:8000/

Create a user:

```bash
curl -X POST http://localhost:8000/signup -H "Content-Type: application/json" -d '{"username":"alice","password":"secretpass!"}'
```

Migrations/collectstatic happen automatically on container boot.

## Environment

See `.env.example`. Important vars:

```
DEBUG=1
DJANGO_SECRET_KEY=dev-secret
POSTGRES_DB=wiremit
POSTGRES_USER=wiremit
POSTGRES_PASSWORD=wiremit
MARKUP=0.10
REDIS_URL=redis://redis:6379/0
FX_API_1=...
FX_API_2=...
FX_API_3=...
```

## CI

Basic GitHub Actions workflow included at `.github/workflows/ci.yml` to lint and run tests (extend as needed).

## Design & Scale

- **Components**: API (Django), Worker (Celery), Scheduler (Beat), Cache/Broker (Redis), DB (Postgres).
- **Data Flow**: Celery fetches external rates → aggregates & stores → API reads latest/historical.
- **Scale**: Add more currencies by listing them in aggregator; add more worker replicas; shard reads via read replicas; cache latest rates in Redis if needed.


