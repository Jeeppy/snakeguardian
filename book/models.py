import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


SOURIS_ROSE = 'SO1'
SOURIS_BLANCHON = 'SO2'
SOURIS_SAUTEUSE = 'SO3'
SOURIS_ADULTE = 'SO4'
RAT_ROSE = 'RA1'
RAT_BLANCHON = 'RA2'
RAT_JEUNE = 'RA3'
RAT_ADULTE = 'RA4'
PROIE = (
    (RAT_ROSE, "Rat - Rosé"),
    (RAT_BLANCHON, "Rat - Blanchon"),
    (RAT_JEUNE, "Rat - Jeune"),
    (RAT_ADULTE, "Rat - Adulte"),
    (SOURIS_ROSE, "Souris - Rosé"),
    (SOURIS_BLANCHON, "Souris - Blanchon"),
    (SOURIS_SAUTEUSE, "Souris - Sauteuse"),
    (SOURIS_ADULTE, "Souris - Adulte"),
)


class Fichier(models.Model):
    """
    Photo
    """
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="utilisateur"
    )
    date = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=200, verbose_name="fichier")

    class Meta:
        abstract = True


class Photo(Fichier):
    class Meta:
        verbose_name = "photo"
        verbose_name_plural = "photo"


class Document(Fichier):
    class Meta:
        verbose_name = "document"
        verbose_name_plural = "documents"


class Specimen(models.Model):
    """
    Spécimen
    """
    MALE = 1
    FEMELLE = 2
    INDETERMINE = 3
    SEXE = (
        (MALE, "mâle"),
        (FEMELLE, "femelle"),
        (INDETERMINE, "indéterminé"),
    )
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="utilisateur"
    )
    nom = models.CharField(
        max_length=50,
        verbose_name="nom"
    )
    classe = models.CharField(
        max_length=50,
        verbose_name="classe"
    )
    espece = models.CharField(
        max_length=50,
        verbose_name="espèce"
    )
    sous_espece = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="sous-espèce"
    )
    phase = models.CharField(
        max_length=50,
        verbose_name="phase"
    )
    sexe = models.IntegerField(
        choices=SEXE,
        verbose_name="sexe",
        default=INDETERMINE
    )
    date_naissance = models.DateField(
        blank=True,
        null=True,
        verbose_name="date de naissance"
    )
    date_entree = models.DateField(
        verbose_name="date d'entrée"
    )
    origine = models.CharField(
        blank=True,
        null=True,
        max_length=50,
        verbose_name="origine"
    )
    derniere_activite = models.DateTimeField(
        auto_now=True,
        verbose_name="dernière activité"
    )
    prix = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="prix"
    )
    alerte_repas = models.IntegerField(
        default=0,
        verbose_name="alerte repas après"
    )
    photos = models.ManyToManyField(
        Photo,
        verbose_name="photo"
    )
    documents = models.ManyToManyField(
        Document,
        verbose_name="documents"
    )

    @property
    def alerter(self):
        dernier_repas = self.repas.order_by('-date').first()
        if not dernier_repas:
            return True if self.alerte_repas else False
        aujourdhui = datetime.datetime.now()
        return bool((aujourdhui - datetime.timedelta(days=self.alerte_repas)).date() > dernier_repas.date and
                    self.alerte_repas)

    def __str__(self):
        return "{nom}".format(nom=self.nom)

    class Meta:
        verbose_name = "spécimen"
        verbose_name_plural = "spécimens"
        index_together = (('id', 'utilisateur'),)


class Entretien(models.Model):
    """
    Entretien
    """
    date = models.DateField(
        verbose_name="date"
    )

    class Meta:
        abstract = True


class Repas(Entretien):
    """
    Repas
    """
    specimen = models.ForeignKey(
        Specimen,
        on_delete=models.CASCADE,
        related_name='repas',
        verbose_name="spécimen"
    )
    type = models.CharField(
        max_length=3,
        choices=PROIE,
        verbose_name="proie",
    )
    quantite = models.IntegerField(
        verbose_name="quantité"
    )
    origine = models.CharField(
        max_length=50,
        verbose_name="origine"
    )
    remarque = models.TextField(
        blank=True,
        null=True,
        verbose_name="remarque"
    )

    def __str__(self):
        return "{} | {} | {} | {}".format(self.date, self.specimen.nom, self.get_type_display(), self.quantite)

    class Meta:
        verbose_name = "repas"
        verbose_name_plural = "repas"


class Mue(Entretien):
    """
    Mue
    """
    specimen = models.ForeignKey(
        Specimen,
        on_delete=models.CASCADE,
        related_name='mues',
        verbose_name="spécimen"
    )
    remarque = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="remarque"
    )

    def __str__(self):
        return "{} | {}".format(self.date, self.specimen.nom)

    class Meta:
        verbose_name = "mue"
        verbose_name_plural = "mues"


class Mesure(Entretien):
    """
    Mesure
    """
    specimen = models.ForeignKey(
        Specimen,
        on_delete=models.CASCADE,
        related_name='mesures',
        verbose_name="spécimen"
    )
    taille = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="taille"
    )
    poids = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="poids"
    )

    def clean(self):
        if not self.taille and not self.poids:
            raise ValidationError("Le poids ou la taille est obligatoire.")
        super().clean()

    def __str__(self):
        return "{} | {} | {}  | {}".format(
            self.date,
            self.specimen.nom,
            self.taille,
            self.poids
        )

    class Meta:
        verbose_name = "mesure"
        verbose_name_plural = "mesures"


class Terrarium(models.Model):
    """
    Terrarium
    """
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="utilisateur"
    )
    nom = models.CharField(
        max_length=50,
        verbose_name="nom"
    )
    longueur = models.IntegerField(
        verbose_name="longueur"
    )
    largeur = models.IntegerField(
        verbose_name="largeur"
    )
    hauteur = models.IntegerField(
        verbose_name="hauteur"
    )
    substrat = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="substrat"
    )
    temperature_point_chaud = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="température point chaud"
    )
    puissance_eclairage = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="puissance d'éclairage"
    )
    puissance_chauffage = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="puissance de chauffage"
    )
    duree_eclairage = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="durée d'éclairage"
    )
    alerte_bac_eau = models.IntegerField(
        default=0,
        verbose_name="alerte nettoyage bac à eau après"
    )
    alerte_substrat = models.IntegerField(
        default=0,
        verbose_name="alerte changement de substrat après"
    )
    alerte_desinfection = models.IntegerField(
        default=0,
        verbose_name="alerte désincfection après"
    )

    @property
    def alerter_bac_eau(self):
        dernier = self.maintenances.filter(type=Maintenance.NETTOYAGE_EAU).order_by('-date').first()
        complet = self.maintenances.filter(type=Maintenance.COMPLET).order_by('-date').first()
        if not dernier and not complet:
            return True if self.alerte_bac_eau else False
        aujourdhui = datetime.datetime.now()
        est_eau_propre = (aujourdhui - datetime.timedelta(days=self.alerte_bac_eau)).date() > dernier.date \
            if dernier else False
        est_nettoyer = (aujourdhui - datetime.timedelta(days=self.alerte_desinfection)).date() > complet.date \
            if complet else False
        return (est_eau_propre or est_nettoyer) and self.alerte_bac_eau

    @property
    def alerter_substrat(self):
        dernier = self.maintenances.filter(type=Maintenance.SUBSTRAT).order_by('-date').first()
        complet = self.maintenances.filter(type=Maintenance.COMPLET).order_by('-date').first()
        if not dernier and not complet:
            return True if self.alerte_substrat else False
        aujourdhui = datetime.datetime.now()
        est_substrat = (aujourdhui - datetime.timedelta(days=self.alerte_substrat)).date() > dernier.date \
            if dernier else False
        est_nettoyer = (aujourdhui - datetime.timedelta(days=self.alerte_desinfection)).date() > complet.date \
            if complet else False
        return (est_substrat or est_nettoyer) and self.alerte_substrat

    @property
    def alerter_desinfection(self):
        dernier = self.maintenances.filter(type=Maintenance.DESINFECTION).order_by('-date').first()
        complet = self.maintenances.filter(type=Maintenance.COMPLET).order_by('-date').first()
        if not dernier and not complet:
            return True if self.alerte_desinfection else False
        aujourdhui = datetime.datetime.now()
        est_desinfecter = (aujourdhui - datetime.timedelta(days=self.alerte_desinfection)).date() > dernier.date \
            if dernier else False
        est_nettoyer = (aujourdhui - datetime.timedelta(days=self.alerte_desinfection)).date() > complet.date \
            if complet else False
        return (est_desinfecter or est_nettoyer) and self.alerte_desinfection

    @property
    def occupants_actuels(self):
        return [
            emplacement.specimen for emplacement in self.occupants.filter(
                Q(date_sortie__isnull=True) | Q(date_sortie__gt=datetime.datetime.now()))]

    def __str__(self):
        return "{nom}".format(nom=self.nom)

    class Meta:
        verbose_name = "terrarium"
        verbose_name_plural = "terrariums"


class Emplacement(models.Model):
    """
    Emplacement d'un spécimen
    """
    date_entree = models.DateField(
        verbose_name="date d'entrée"
    )
    date_sortie = models.DateField(
        blank=True,
        null=True,
        verbose_name="date de sortie"
    )
    specimen = models.ForeignKey(
        Specimen,
        on_delete=models.CASCADE,
        related_name='emplacements',
        verbose_name="spécimen"
    )
    terrarium = models.ForeignKey(
        Terrarium,
        on_delete=models.CASCADE,
        related_name='occupants',
        verbose_name="terrarium"
    )

    def __str__(self):
        return "{} | {} | {}".format(self.date_entree, self.specimen.nom, self.terrarium.nom)

    class Meta:
        verbose_name = "emplacement d'un spécimen"
        verbose_name_plural = "emplacements des spécimens"


class Maintenance(Entretien):
    """
    Entretien
    """
    NETTOYAGE_EAU = 1
    SUBSTRAT = 2
    RETRAIT = 3
    DESINFECTION = 4
    COMPLET = 5
    NETTOYAGE_VITRE = 6
    TYPE = (
        (NETTOYAGE_EAU, "nettoyage du bac à eau"),
        (NETTOYAGE_VITRE, "nettoyage des vitres"),
        (SUBSTRAT, "changement du substrat"),
        (RETRAIT, "retrait mues/excréments/salissures"),
        (DESINFECTION, "désinfection"),
        (COMPLET, "nettoyage complet"),
    )

    terrarium = models.ForeignKey(
        Terrarium,
        on_delete=models.CASCADE,
        related_name='maintenances',
        verbose_name="terrarium"
    )
    type = models.IntegerField(
        choices=TYPE,
        verbose_name="Type"
    )
    remarque = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="remarque"
    )

    def __str__(self):
        return "{} | {} | {}".format(self.date, self.terrarium, self.get_type_display().capitalize())


class Achat(models.Model):
    """
    Achat
    """
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="utilisateur"
    )
    date = models.DateField(
        verbose_name="date d'achat"
    )
    lieu = models.CharField(
        max_length=50,
        verbose_name="lieu d'achat"
    )
    type = models.CharField(
        max_length=3,
        choices=PROIE,
        verbose_name="type"
    )
    quantite = models.IntegerField(
        verbose_name="quantité"
    )
    prix = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        verbose_name="prix d'achat"
    )

    def __str__(self):
        return "{} | {} | {} €".format(self.date, self.get_type_display(), self.prix)

    @property
    def prix_unitaire(self):
        return self.prix / self.quantite

    class Meta:
        verbose_name = "achat"
        verbose_name_plural = "achats"


class Hivernation(models.Model):
    """
    Hivernation
    """
    specimen = models.ForeignKey(
        Specimen,
        on_delete=models.CASCADE,
        related_name='hivernation',
        verbose_name="spécimen"
    )
    date_debut = models.DateField(
        verbose_name="date de debut"
    )
    date_fin = models.DateField(
        verbose_name="date de fin",
        blank=True,
        null=True
    )

    @property
    def duree(self):
        if not self.date_fin:
            return None
        return (self.date_fin - self.date_debut).days
