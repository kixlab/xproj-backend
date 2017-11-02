from django.contrib.gis.db import models

class VotingDistrict(models.Model):
    """
    One Voting district (선거구) cover multiple Areas.
    The mpoly shape is a union of all the included areas.
    """
    name = models.CharField(max_length=254)
    mpoly = models.MultiPolygonField(srid=3857)

    def current_mop(self):
        try:
            return self.mop.all()[0]
        except IndexError:
            return None

    def __str__(self):
        return self.name


class Area(models.Model):
    """
    An area (district) in South Korea,
    e.g. 대전광역시 (province), 유성구 (precinct), 온천2동 (area)
    Mapped to its voting district
    Spatial information in mpoly. Can query location, distance etc.
    """
    area_id = models.CharField(max_length=10)
    name = models.CharField('Name of area (동)', max_length=254)
    precinct = models.CharField('Precinct (구)', max_length=254)
    province = models.CharField('Province (도)',max_length=254)
    voting_district_name = models.CharField(max_length=254)
    voting_district = models.ForeignKey(VotingDistrict,
                                          on_delete=models.SET_NULL,
                                          blank=True,
                                          null=True,
                                          related_name='areas')

    mpoly = models.MultiPolygonField(srid=3857)

    def __str__(self):
        return '%s, %s, %s' % (self.province, self.precinct, self.name)

    @property
    def display_name(self):
        return '%s %s %s' % (self.province, self.precinct, self.name)
