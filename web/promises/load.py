import os
from spatial.models import VotingDistrict
from promises.models import Person, Promise
import json
import re

def run(verbose=True):
    mayors()
    #elected_members()
    promises()

def elected_members():
    f = open("/data/voting-districts/results.txt")
    results = dict([line.split() for line in f])
    for v in VotingDistrict.objects.all():
        if v.name not in results:
            print("Missing result for %s" % v.name)
            continue
        member, created = Person.objects.update_or_create(
            name=results.get(v.name),
            defaults={'mop_for_district': v}
        )

def mayors():
    with open('/data/voting-districts/mayors.json') as data_file:    
        data = json.load(data_file)

    for province in data:
        print(province)
        province_name = province['province']
        mayor = province['mayor']
        submayors = province.get('sub', {})

        member, created = Person.objects.update_or_create(
            name=mayor,
            defaults={'mayor_for_province': province_name}
        )

        for district, name in submayors.items():
            member, created = Person.objects.update_or_create(
                name=name,
                defaults={'mayor_for_district': district}
            )    

provinces_eng_to_kor = {
    "seoul": "서울특별시",
    "daegu": "대구광역시",
    "gwangju": "광주광역시",
    "daejeon": "대전광역시",
    "ulsan": "울산광역시",
    "sejong": "세종특별자치시",
    "gyeonggi": "경기도",
    "gangwon": "강원도",
    "chungbuk": "충청북도",
    "chungnam": "충청남도",
    "jeonbuk": "전라북도",
    "jeonnam": "전라남도",
    "gyeongbuk": "경상북도",
    "gyeongnam": "경상남도",
    "jeju": "제주특별자치도",
    "busan": "부산광역시",
    "incheon": "인천광역시"
}

def promises():
    with open('/data/promises/jisa_tagged.json') as data_file:    
        data = json.load(data_file)
        for voting_district in data:
            province_name_eng = voting_district['city']
            if province_name_eng == '':
                continue
            province_name = provinces_eng_to_kor[province_name_eng]

            try:
                person = Person.objects.get(mayor_for_province=province_name)
            except Person.DoesNotExist:
                print("Could not find person for province %s" % province_name)
                continue
            promises = voting_district['promises']
            print(person.name, person.mayor_for_province, len(promises))

            for p in promises:
                promise = Promise(title=p['title'], categories=p['category'], target_groups=p['target'])
                promise.person = person
                promise.save()

    return

    with open('/data/promises/cong_tagged.json') as data_file:    
        data = json.load(data_file)
        for voting_district in data:
            name = voting_district['name']
            m = re.match('.*\(\s?(.*?)\s?\)', name)
            if not m:
                print("Could not match person name in %s" % name)
                continue
            person_name = m.group(1)
            try:
                person = Person.objects.get(name=person_name)
            except Person.DoesNotExist:
                print("Could not find person with name %s" % person_name)
                continue
            promises = voting_district['promises']
            print(person.name, person.mop_for_district, len(promises))

            for p in promises:
                promise = Promise(title=p['title'], categories=p['category'], target_groups=p['target'])
                promise.person = person
                promise.save()



