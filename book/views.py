from collections import Counter, OrderedDict
from datetime import datetime

import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.db.models import Sum
from django.shortcuts import render

from book.forms import TerrariumForm, SpecimenForm, RepasForm, MueForm, MesureForm, EmplacementForm, MaintenanceForm, \
    AchatForm, UploadFileForm
from book.models import Terrarium, Specimen, Achat, Repas, PROIE, Mue, Mesure, Emplacement, Maintenance, Photo, Document
from book.utils import proies_en_stock


@login_required
def index(request):
    """
    Page index
    """
    specimens = Specimen.objects.filter(utilisateur=request.user).order_by('nom')
    return render(
        request,
        'book/index.html',
        {
            'specimens': specimens,
        }
    )


@login_required
def liste_terrariums(request):
    """
    Page terrarium
    """

    data = Terrarium.objects.filter(utilisateur=request.user).order_by('nom')

    return render(request, 'book/liste_terrariums.html', {'terrariums': data})


@login_required
def ajouter_terrarium(request):
    """
    Ajouter un terrarium
    """
    form = TerrariumForm(request.POST or None)
    if form.is_valid():
        created = True
        form.save()
    else:
        created = False
    return render(request, 'book/ajouter_terrarium.html', {'form': form, 'created': created})


@login_required
def liste_specimens(request):
    """
    Spécimens
    """
    data = Specimen.objects.filter(utilisateur=request.user).order_by('nom')
    return render(request, 'book/liste_specimens.html', {'specimens': data})


@login_required
def ajouter_specimen(request):
    """
    Ajouter un spécimen
    """
    form = SpecimenForm(request.POST or None)
    if form.is_valid():
        created = True
        form.save()
    else:
        created = False
    return render(request, 'book/ajouter_specimen.html', {'form': form, 'created': created})


@login_required
def specimen(request, identifiant):
    """
    Spécimen
    """
    data = Specimen.objects.get(id=identifiant, utilisateur=request.user)
    repas = data.repas.order_by('-date')
    return render(request, 'book/specimen.html', {'specimen': data, 'repas': repas})


@login_required
def ajouter_repas(request, identifiant):
    """
    Ajouter un repas
    """
    instance_specimen = Specimen.objects.get(id=identifiant, utilisateur=request.user)
    form = RepasForm(request.POST or None, initial={'specimen': instance_specimen})
    proies = proies_en_stock(request.user)
    if form.is_valid():
        created = True
        form.save()
    else:
        created = False
    return render(
        request,
        'book/ajouter_repas.html',
        {'form': form, 'created': created, 'specimen': instance_specimen, 'proies': proies, 'now': datetime.now()}
    )


@login_required
def ajouter_mue(request, identifiant):
    """
    Ajouter une mue
    """
    instance_specimen = Specimen.objects.get(id=identifiant, utilisateur=request.user)
    form = MueForm(request.POST or None, initial={'specimen': instance_specimen})
    if form.is_valid():
        created = True
        form.save()
    else:
        created = False
    return render(
        request,
        'book/ajouter_mue.html',
        {'form': form, 'created': created, 'specimen': instance_specimen, 'now': datetime.now()}
    )


@login_required
def ajouter_mesure(request, identifiant):
    """
    Ajouter une mesure
    """
    instance_specimen = Specimen.objects.get(id=identifiant, utilisateur=request.user)
    form = MesureForm(request.POST or None, initial={'specimen': instance_specimen})
    if form.is_valid():
        created = True
        form.save()
    else:
        created = False
    return render(
        request,
        'book/ajouter_mesure.html',
        {'form': form, 'created': created, 'specimen': instance_specimen, 'now': datetime.now()}
    )


@login_required
def ajouter_emplacement(request, identifiant):
    """
    Ajouter un emplacement
    """
    instance_specimen = Specimen.objects.get(id=identifiant, utilisateur=request.user)
    form = EmplacementForm(request.POST or None, initial={'specimen': instance_specimen})
    terrariums = Terrarium.objects.all()
    if form.is_valid():
        created = True
        form.save()
    else:
        created = False
    return render(
        request,
        'book/ajouter_emplacement.html',
        {'form': form, 'created': created, 'specimen': instance_specimen, 'terrariums': terrariums, 'now': datetime.now()}
    )


@login_required
def terrarium(request, identifiant):
    """
    Terrarium
    """
    data = Terrarium.objects.get(id=identifiant, utilisateur=request.user)
    maintenances = data.maintenances.order_by('-date')
    return render(request, 'book/terrarium.html', {'terrarium': data, 'maintenances': maintenances})


@login_required
def ajouter_maintenance(request, identifiant):
    """
    Ajouter une maintenance
    """
    instance_terrarium = Terrarium.objects.get(id=identifiant, utilisateur=request.user)
    form = MaintenanceForm(request.POST or None, initial={'terrarium': instance_terrarium})
    if form.is_valid():
        created = True
        form.save()
    else:
        created = False
    return render(
        request,
        'book/ajouter_maintenance.html',
        {'form': form, 'created': created, 'terrarium': instance_terrarium, 'now': datetime.now()}
    )


@login_required
def stock(request):
    """
    Stock
    """
    achats = Achat.objects.filter(utilisateur=request.user).order_by('-date')
    initial = {}
    for item in achats.filter(utilisateur=request.user).values('type').annotate(total=Sum('quantite')):
        item_type = item.get('type')
        item_total = int(item.get('total', 0))
        if item_type in initial:
            item_total += initial.get(item_type)
        initial[item_type] = item_total
    consomations = {}
    for item in Repas.objects.filter(specimen__utilisateur=request.user).values('type').annotate(total=Sum('quantite')):
        consomations[item.get('type')] = item.get('total')
    inventaire = dict(Counter(initial) - Counter(consomations))
    repas = Repas.objects.filter(specimen__utilisateur=request.user).order_by('-date')
    return render(
        request,
        'book/stock.html',
        {'achats': achats, 'stock': OrderedDict(sorted(inventaire.items())), 'consomations': repas}
    )


@login_required
def ajouter_achat(request):
    """
    Ajouter un achat
    """
    form = AchatForm(request.POST or None)
    types = OrderedDict(PROIE)
    if form.is_valid():
        created = True
        form.save()
    else:
        created = False
    return render(
        request, 'book/ajouter_achat.html', {'form': form, 'created': created, 'types': types, 'now': datetime.now()}
    )


@login_required
def editer_specimen(request, identifiant):
    """
    Editer un spécimen
    """
    instance = Specimen.objects.get(id=identifiant, utilisateur=request.user)
    form = SpecimenForm(request.POST or None, instance=instance)
    if form.is_valid():
        modified = True
        form.save()
    else:
        modified = False
    return render(request, 'book/ajouter_specimen.html', {'specimen': instance, 'form': form, 'modified': modified})


@login_required
def editer_terrarium(request, identifiant):
    """
    Editer un terrarium
    """
    instance = Terrarium.objects.get(id=identifiant, utilisateur=request.user)
    form = TerrariumForm(request.POST or None, instance=instance)
    if form.is_valid():
        modified = True
        form.save()
    else:
        modified = False
    return render(request, 'book/ajouter_terrarium.html', {'terrarium': instance, 'form': form, 'modified': modified})


@login_required
def editer_repas(request, identifiant):
    """
    Editer un repas
    """
    instance = Repas.objects.get(id=identifiant, specimen__utilisateur=request.user)
    instance_specimen = instance.specimen
    form = RepasForm(request.POST or None, instance=instance)
    proies = proies_en_stock(request.user)
    if form.is_valid():
        modified = True
        form.save()
    else:
        modified = False
    return render(
        request,
        'book/ajouter_repas.html',
        {
            'repas': instance,
            'form': form,
            'modified': modified,
            'proies': proies,
            'specimen': instance_specimen,
        }
    )


@login_required
def editer_mue(request, identifiant):
    """
    Editer une mue
    """
    instance = Mue.objects.get(id=identifiant, specimen__utilisateur=request.user)
    instance_specimen = instance.specimen
    form = MueForm(request.POST or None, instance=instance)
    if form.is_valid():
        modified = True
        form.save()
    else:
        modified = False
    return render(
        request,
        'book/ajouter_mue.html',
        {'mue': instance,
         'form': form,
         'modified': modified,
         'specimen': instance_specimen}
    )


@login_required
def editer_mesure(request, identifiant):
    """
    Editer une mesure
    """
    instance = Mesure.objects.get(id=identifiant, specimen__utilisateur=request.user)
    instance_specimen = instance.specimen
    form = MesureForm(request.POST or None, instance=instance)
    if form.is_valid():
        modified = True
        form.save()
    else:
        modified = False
    return render(
        request,
        'book/ajouter_mesure.html',
        {'mesure': instance, 'form': form, 'modified': modified, 'specimen': instance_specimen}
    )


@login_required
def editer_emplacement(request, identifiant):
    """
    Editer un emplacement
    """
    instance = Emplacement.objects.get(id=identifiant, specimen__utilisateur=request.user)
    instance_specimen = instance.specimen
    terrariums = Terrarium.objects.all()
    form = EmplacementForm(request.POST or None, instance=instance)
    if form.is_valid():
        modified = True
        form.save()
    else:
        modified = False
    return render(
        request,
        'book/ajouter_emplacement.html',
        {
            'emplacement': instance,
            'form': form,
            'modified': modified,
            'terrariums': terrariums,
            'specimen': instance_specimen
        }
    )


@login_required
def editer_maintenance(request, identifiant):
    """
    Editer une maintenance
    """
    instance = Maintenance.objects.get(id=identifiant, terrarium__utilisateur=request.user)
    form = MaintenanceForm(request.POST or None, instance=instance)
    if form.is_valid():
        modified = True
        form.save()
    else:
        modified = False
    return render(
        request,
        'book/ajouter_maintenance.html',
        {'maintenance': instance, 'form': form, 'modified': modified, 'terrarium': instance.terrarium}
    )


@login_required
def editer_achat(request, identifiant):
    """
    Editer un achat
    """
    instance = Achat.objects.get(id=identifiant, utilisateur=request.user)
    form = AchatForm(request.POST or None, instance=instance)
    types = dict(PROIE)
    if form.is_valid():
        modified = True
        form.save()
    else:
        modified = False
    return render(
        request,
        'book/ajouter_achat.html',
        {'form': form, 'modified': modified, 'types': types, 'achat': instance}
    )


@login_required
def upload_photo(request, identifiant):
    instance_specimen = Specimen.objects.get(id=identifiant, utilisateur=request.user)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            save_path = os.path.join(settings.MEDIA_ROOT, 'photos', request.FILES['file']._name)
            path = default_storage.save(save_path, request.FILES['file'])
            default_storage.path(path)
            uploaded = True
            filename = path[path.rfind('/') + 1:len(path)]
            photo = Photo.objects.create(filename=filename, utilisateur=request.user)
            instance_specimen.photos.add(photo)
    else:
        form = UploadFileForm()
        uploaded = False
    return render(
        request,
        'book/ajouter_photo.html',
        {'form': form, 'uploaded': uploaded, 'specimen': instance_specimen}
    )


@login_required
def creer_carte(request, identifiant):
    instance = Specimen.objects.get(id=identifiant, utilisateur=request.user)
    url = "{domaine}/specimen/{id}/".format(domaine=request.get_host(), id=identifiant)
    return render(
        request,
        'book/card.html',
        {'specimen': instance, 'url': url}
    )


@login_required
def ajouter_document(request, identifiant):
    instance_specimen = Specimen.objects.get(id=identifiant, utilisateur=request.user)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            save_path = os.path.join(settings.MEDIA_ROOT, 'documents', request.FILES['file']._name)
            path = default_storage.save(save_path, request.FILES['file'])
            default_storage.path(path)
            uploaded = True
            filename = path[path.rfind('/') + 1:len(path)]
            document = Document.objects.create(filename=filename, utilisateur=request.user)
            instance_specimen.documents.add(document)
    else:
        form = UploadFileForm()
        uploaded = False
    return render(
        request,
        'book/ajouter_document.html',
        {'form': form, 'uploaded': uploaded, 'specimen': instance_specimen}
    )
