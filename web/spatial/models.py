from django.contrib.gis.db import models

class Area(models.Model):
    """
    An area (district) in South Korea, e.g. 대전광역시, 유성구, 온천2동
    Mapped to its voting district
    Spatial information in mpoly. Can query location, distance etc.
    """
    area_id = models.CharField(max_length=10)  # ADM_DR_CD
    name = models.CharField(max_length=254)  # ADM_DR_NM
    precinct = models.CharField(max_length=254)  # precinct_n
    province = models.CharField(max_length=254)  # province
    voting_district_name = models.CharField(max_length=254)  # SGG_NM

    mpoly = models.MultiPolygonField(srid=3857)

    def __str__(self):
        return '%s, %s, %s' % (self.province, self.precinct, self.name)
