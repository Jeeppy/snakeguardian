from collections import Counter, OrderedDict
from django.db.models import Sum
from book.models import Achat, Repas


def proies_en_stock(utilisateur):
    achats = Achat.objects.order_by('-date')
    initial = {}
    for item in achats.filter(utilisateur=utilisateur).values('type').annotate(total=Sum('quantite')):
        item_type = item.get('type')
        item_total = int(item.get('total', 0))
        if item_type in initial:
            item_total += initial.get(item_type)
        initial[item_type] = item_total
    consomations = {}
    for item in Repas.objects.filter(specimen__utilisateur=utilisateur).values('type').annotate(total=Sum('quantite')):
        consomations[item.get('type')] = item.get('total')
    inventaire = Counter(initial) - Counter(consomations)
    return OrderedDict(sorted(inventaire.items()))
