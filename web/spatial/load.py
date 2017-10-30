import os
from django.contrib.gis.utils import LayerMapping
from django.db.models import Count
from spatial.models import Area, VotingDistrict
from django.contrib.gis import geos

mapping = {
    'area_id' : 'ADM_DR_CD',
    'name' : 'ADM_DR_NM',
    'voting_district_name' : 'precinct_n',
    'province' : 'province',
    'precinct' : 'SGG_NM',
    'mpoly' : 'MULTIPOLYGON',
}

def run(shp_file, verbose=False):
    Area.objects.all().delete()
    VotingDistrict.objects.all().delete()

    spatial_data(shp_file, verbose)
    voting_districts()

def spatial_data(shp_file, verbose=True):
    lm = LayerMapping(
        Area, shp_file, mapping,
        encoding='utf-8',
        transform=False,
    )
    lm.save(strict=False, verbose=verbose)
    print("Imported %d areas" % Area.objects.all().count())

def voting_districts():
    voting_districts = Area.objects.values('voting_district_name').annotate(count=Count("id"))
    for district in voting_districts:
        name = district['voting_district_name']
        areas = Area.objects.filter(voting_district_name=name)
        # Union all areas
        union = areas[0].mpoly
        for area in areas[1:]:
            union = union.union(area.mpoly)
        if union and isinstance(union, geos.Polygon):
            union = geos.MultiPolygon(union)
        # Save district
        v, created = VotingDistrict.objects.update_or_create(
            name=name, 
            defaults={'mpoly': union},
        )
        v.areas = areas
        v.save()
        print("Imported %s with %d areas" % (name, district['count']))
