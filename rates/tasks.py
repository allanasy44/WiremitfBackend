from celery import shared_task
from .aggregator import fetch_pairs
from .models import Rate
@shared_task
def refresh_rates_task():
    pairs=fetch_pairs()
    for pair,data in pairs.items():
        if not data: continue
        Rate.objects.create(pair=pair, rate=data['final'], sources={'average':data['average'],'samples':data['sources']})
    return True
