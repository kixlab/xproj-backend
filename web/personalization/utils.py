from prompt_responses.models import Response, Prompt
from django.db.models import Max
from django.contrib.auth import get_user_model

def get_promptset_prompt(prompt_set, object_id=None, user=None):
    # if object_id, find some statistic for object_id amont all prompts with the set
    print('stats')
    User = get_user_model()

    # Prepare queryset of responses for this prompt set
    qs = Response.objects.filter(
        prompt__promptset=prompt_set.pk,
        object_id=object_id
    ).exclude(
        rating__isnull=True,
        prompt__type=Prompt.TYPES.tagging
    )
    # Select most recent response for each user
    latest_ratings = qs.order_by().values('prompt', 'content_type', 'object_id', 'user_id').annotate(
        max_id=Max('id')
    ).values('max_id')
    qs = qs.filter(pk__in=latest_ratings)

    # Strategy 1: Find any user sharing some charachteristic with me rating this promise highly for any of the prompts
    qs_ = qs.filter(rating__gte=4)
    users = User.objects.filter(id__in=qs_.values('user__id')).all()
    found_user = None
    for user in users:
        # Find a user that shares something with me
        found_user = user
        break
    print('found %d users in these prompts' % len(users))
    print(found_user)
    
    return '<span class="emphasis-text">20대 대학원생</span>과 연관있는 공약입니다. 이 공약에 대해 어떻게 생각하시나요?'