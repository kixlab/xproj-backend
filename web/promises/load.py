import os
from spatial.models import VotingDistrict
from promises.models import Person, Promise
import json
import re

def run(verbose=True):
    elected_members()
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

def promises():
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



