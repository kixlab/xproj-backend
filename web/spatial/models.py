from django.contrib.gis.db import models


class VotingDistrict(models.Model):
    name = models.CharField(max_length=254)
    mpoly = models.MultiPolygonField(srid=3857)

    def __str__(self):
        return self.name


class Area(models.Model):
    """
    An area (district) in South Korea, e.g. 대전광역시, 유성구, 온천2동
    Mapped to its voting district
    Spatial information in mpoly. Can query location, distance etc.
    """
    area_id = models.CharField(max_length=10)
    name = models.CharField(max_length=254)
    precinct = models.CharField(max_length=254)
    province = models.CharField(max_length=254)
    voting_district_name = models.CharField(max_length=254)
    voting_distict_id = models.ForeignKey(VotingDistrict,
                                          on_delete=models.SET_NULL,
                                          blank=True,
                                          null=True,
                                          related_name='areas')

    mpoly = models.MultiPolygonField(srid=3857)

    def __str__(self):
        return '%s, %s, %s' % (self.province, self.precinct, self.name)
