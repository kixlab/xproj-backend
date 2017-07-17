import os
from django.contrib.gis.utils import LayerMapping
from .models import Area

mapping = {
    'area_id' : 'ADM_DR_CD',
    'name' : 'ADM_DR_NM',
    'voting_district_name' : 'precinct_n',
    'province' : 'province',
    'precinct' : 'SGG_NM',
    'mpoly' : 'MULTIPOLYGON',
}

shp_file = '/data/voting-districts/제20대국회의원선거구_속성_통계청행정동.shp'

def run(verbose=True):
    Area.objects.all().delete()
    lm = LayerMapping(
        Area, shp_file, mapping,
        encoding='utf-8',
        transform=False,
    )
    lm.save(strict=True, verbose=verbose)
