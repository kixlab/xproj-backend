import os
from spatial.models import VotingDistrict
from promises.models import Person, Promise, BudgetProgram
import json
import csv
import re

def run(verbose=True):
    mayors()
    elected_members()
    promises()
    # links()

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


def goal_texts():
    with open('/data/promise-goals/goals.csv') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            pk = (idx+1)
            promise = Promise.objects.get(id=pk)
            promise.goals = row['goal']
            promise.save()
            print("%d - %s - %s" % (pk, row['promise'], promise.title))

from itertools import islice
import numpy as np
from operator import itemgetter 
from collections import defaultdict
import string

def links():
    # Read promise-budget scoring table csv
    with open('/data/linkscores_name.csv', 'rb') as f:
        # Grab promise titles from first row
        promises = list(np.genfromtxt(islice(f, 0, 1), delimiter=",", dtype=None))
        # Grab service titles from second column
        services = np.genfromtxt(f, delimiter=",", dtype=None, skip_header=1, filling_values=0, invalid_raise=False, usecols=(1,))
        f.seek(0)
        # Grab budgets and scores from the table
        data = np.genfromtxt(f, delimiter=",", dtype="float", skip_header=1, filling_values=0, invalid_raise=False)
        budgets = data[:, 2]
        scores = data[:, 3:]
        # Find top services for each promise
        top_service_indices = np.argsort(-scores, axis=0)
        # Filter services scoring higher than threshold
        threshold = 0.8
        top_score_indices_m = np.transpose(np.nonzero(np.transpose(scores>threshold)))
        # Convert (x, y) tuples into dict of {x: [y1, y2, y3... ]}
        top_services_per_promise = defaultdict(list)
        for (promise_idx, service_idx) in top_score_indices_m:
            top_services_per_promise[promise_idx].append(service_idx)

    # Clean titles for better matching
    remove_quotes_map = dict([(ord(x), None) for x in ".,‘’´“”–-() "]) 
    promises_clean = list(map(lambda s: s.decode().translate(remove_quotes_map), promises))
    found = 0
    # Go through all promises in database
    for promise in Promise.objects.all():
        try:
            # Get index of promise
            title = promise.title.translate(remove_quotes_map)
            promise_idx = promises_clean.index(title)
        except ValueError:
            # print("Error at %s, could not find promise with this title (%s) in data." % (promise.title, title))
            continue
        found = found + 1
        # Take the top 4 services and all that have high enough score
        top_n_indices = top_service_indices[promise_idx, 0:4]
        top_score_indices = top_services_per_promise[promise_idx]
        linked_service_indices = set(list(top_n_indices) + list(top_score_indices))
        print("Linking %s with %d budget programs" % (promise.title, len(linked_service_indices)))
        for idx in linked_service_indices:
            title = services[idx].decode()
            budget = int(budgets[idx])
            budget_program, _ = BudgetProgram.objects.get_or_create(title=title, defaults={'amount': budget})
            promise.budget_programs.add(budget_program)
            promise.save()

    print("Found %d promises" % found)
    # find number of occurences:
    # from collections import Counter
    # Counter(top_promise_indices[:, 0])
    # find number of matched promises:
    # len(Counter(top_promise_indices[:, 0]).keys())
    # To find threshold, I did
    # np.sort(np.sum(scores > 0.8, axis=0))[::-1] and change threshold until
    # Get index of promise promises.index("사장직속안전전담기구신설".encode())


