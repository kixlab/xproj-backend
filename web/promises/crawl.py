import requests
from .models import BudgetProgram
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def seoul_api_url(service, *extra_args, **kwargs):
    if not settings.XPROJ_SEOUL_API_KEY:
        raise ImproperlyConfigured(
            "API key for Seoul open API is missing. "
            "Please provide set XPROJ_SEOUL_API_KEY in your environment "
            "before launching this command."
        )
    options = {
        "key": settings.XPROJ_SEOUL_API_KEY,
        "type": "json",
        "service": service
    }
    options.update(kwargs)
    url = "http://openapi.seoul.go.kr:8088/{key}/{type}/{service}/{low}/{high}/{fiscal_year}"
    formatted = url.format(**options)
    formatted += "/".join(extra_args)
    return formatted

def get_budget_programs(fiscal_year):
    """Imports all Budget programs in chunks"""
    print("Crawling budget programs for %d" % fiscal_year)
    chunk = 500
    total_number = 0
    service = "FiosTbmTecurramt"
    low = 1
    high = chunk
    count_updated = 0
    count_created = 0
    while True:
        try:
            print("Getting %s from %4d to %4d (total %d)..." % (service, low, high, total_number))
            url = seoul_api_url(service, low=low, high=high, fiscal_year=fiscal_year)
            data = requests.get(url, timeout=5).json()
        except requests.exceptions.ConnectionError:
            print("Request failed. Check network or try again later.")
            break    
        except requests.exceptions.Timeout:
            print("Request timed out. Check network or try again later.")
            break    
        except requests.exceptions.HTTPError:
            # Could not get url
            print("Error getting API.")
            break
        except ValueError:
            # Could not parse JSON
            print("Error parsing JSON.")
            break

        if service not in data:
            print("Error: %s" % data["RESULT"]["MESSAGE"])
            break

        for row in data[service]["row"]:
            values = {
                "name": row["DBIZ_NM"],
                "fiscal_year": row["FIS_YEAR"],
                "fiscal_category": row["FIS_FG_NM"],
                "category": row["FLD_NM"],
                "sub_category": row["SECT_NM"],
                "department": row["DEPT_NM"],
                "total_amount": row["SUB_SUM_CURR_AMT"],
                "expenditure_amount": row["EXPD_AMT"],
                "etc_amount": row["ETC_AMT"],
                "change_amount": row["CHNG_AMT"],
                "forward_amount": row["FORWD_AMT"],
                "allocated_amount": row["COMPO_AMT"],
                "national_amount": row["NATN_CURR_AMT"],
                "province_amount": row["SIDO_CURR_AMT"],
                "precinct_amount": row["SIGUNGU_CURR_AMT"],
                "balance_amount": row["BALANCE_AMT"],
            }
            _, created = BudgetProgram.objects.update_or_create(original_id=row['DBIZ_CD'], defaults=values)
            count_created += 1 if created else 0
            count_updated += 0 if created else 1

        # Continue paging until all records are downloaded.
        total_number = data[service]['list_total_count']
        if len(data[service]["row"]) >= chunk:
            low = high + 1
            high += chunk
            if high > total_number:
                high = total_number
        else:
            break
    print("Created %d, updated %d objects" % (count_created, count_updated))