
import os, requests, statistics, logging
from django.conf import settings
logger = logging.getLogger(__name__)

def _fetch(api_url):
    try:
        r = requests.get(api_url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.warning("fetch failed %s %s", api_url, e)
        return None

def fetch_pairs():
    # Build API list from env with settings fallbacks
    apis = [
        os.environ.get('FX_API_1', getattr(settings, 'FX_API_1', 'https://api.exchangerate.host/latest?base=USD')),
        os.environ.get('FX_API_2', getattr(settings, 'FX_API_2', 'https://open.er-api.com/v6/latest/USD')),
        os.environ.get('FX_API_3', getattr(settings, 'FX_API_3', 'https://api.exchangerate-api.com/v4/latest/USD')),
    ]

    samples_usd_gbp = []
    samples_usd_zar = []

    for url in apis:
        data = _fetch(url)
        if not data:
            continue

        # Normalize common shapes
        rates = data.get('rates') or data.get('conversion_rates') or data.get('conversionRates') or {}
        base = data.get('base') or data.get('base_code') or data.get('baseCurrency') or 'USD'

        if not rates:
            continue

        # We want rates expressed as USD -> target (i.e., target per 1 USD)
        # If base is USD, we can read directly. If base is not USD, invert accordingly if possible.
        def to_usd_target(ticker):
            if base.upper() == 'USD':
                return rates.get(ticker)
            # rate is given as base -> target, so to get USD->target we need USD in 'rates'
            # If we have rate for ticker in terms of base, and also USD in terms of base,
            # USD->ticker = (base->ticker) / (base->USD)
            base_to_ticker = rates.get(ticker)
            base_to_usd = rates.get('USD')
            if base_to_ticker and base_to_usd:
                try:
                    return float(base_to_ticker) / float(base_to_usd)
                except Exception:
                    return None
            return None

        usd_gbp = to_usd_target('GBP')
        usd_zar = to_usd_target('ZAR')

        if usd_gbp: samples_usd_gbp.append(float(usd_gbp))
        if usd_zar: samples_usd_zar.append(float(usd_zar))

    markup = float(os.environ.get('MARKUP', getattr(settings, 'MARKUP', 0.10)))

    out = {}

    def compute(vals):
        if not vals:
            return None
        avg = float(statistics.mean(vals))
        final = avg * (1.0 + markup)
        return {'average': avg, 'final': final, 'count': len(vals), 'sources': vals}

    out['USD-GBP'] = compute(samples_usd_gbp)
    out['USD-ZAR'] = compute(samples_usd_zar)

    # Cross rate ZAR-GBP = (USD-GBP) / (USD-ZAR)
    cross_samples = []
    for i in range(min(len(samples_usd_gbp), len(samples_usd_zar))):
        try:
            cross_samples.append(samples_usd_gbp[i] / samples_usd_zar[i])
        except Exception:
            continue
    out['ZAR-GBP'] = compute(cross_samples)

    return out
