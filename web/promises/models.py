from django.contrib.gis.db import models
from spatial.models import VotingDistrict
from django.contrib.postgres.fields import ArrayField

class Person(models.Model):
    name = models.CharField(max_length=100)
    mop_for_district = models.ForeignKey(VotingDistrict, related_name='mop', null=True)
    mayor_for_province = models.CharField(max_length=50, blank=True, null=True)
    mayor_for_district = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class Promise(models.Model):
    title = models.CharField(max_length=254)
    categories = ArrayField(models.CharField(max_length=50), blank=True)
    target_groups = ArrayField(models.CharField(max_length=50), blank=True)
    person = models.ForeignKey(Person, related_name='promises',
        on_delete=models.SET_NULL, blank=True, null=True)
    budget_programs = models.ManyToManyField('BudgetProgram', related_name='promises')

    def __str__(self):
        return self.title

class BudgetProgram(models.Model):
    name = models.CharField(max_length=254)  # DBIZ_NM 세부사업명
    original_id = models.CharField(max_length=254, null=True, blank=True, unique=True)  # DBIZ_CD 세부사업코드
    fiscal_year = models.PositiveSmallIntegerField(default=0)  # FIS_YEAR 회계연도
    fiscal_category = models.CharField(max_length=50)  # FIS_FG_NM 회계구분
    category = models.CharField(max_length=50)  # FLD_NM 회계구분
    sub_category = models.CharField(max_length=50)  # SECT_NM 부문명
    department = models.CharField(max_length=254)  # DEPT_NM 부서명
    total_amount = models.BigIntegerField   (default=0)  # SUB_SUM_CURR_AMT 소계
    expenditure_amount = models.BigIntegerField(default=0)  # EXPD_AMT 지출액
    etc_amount = models.BigIntegerField(default=0)  # ETC_AMT 수입대체경비
    change_amount = models.BigIntegerField(default=0)  # CHNG_AMT 변경금액
    forward_amount = models.BigIntegerField(default=0)  # FORWD_AMT 이월액
    allocated_amount = models.BigIntegerField(default=0)  # COMPO_AMT 편성액
    national_amount = models.BigIntegerField(default=0)  # NATN_CURR_AMT 국비
    province_amount = models.BigIntegerField(default=0)  # SIDO_CURR_AMT 도비
    precinct_amount = models.BigIntegerField(default=0)  # SIGUNGU_CURR_AMT 구비
    balance_amount = models.BigIntegerField(default=0)  # BALANCE_AMT 집행잔액

    def __str__(self):
        return self.name