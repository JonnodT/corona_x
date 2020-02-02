from django.db import models

# Create your models here.

class User(models.Model):
    class Meta:
        db_table = "user"

        verbose_name = "user"

        verbose_name_plural = "users"


class Symptom(models.Model):
    class Meta:
        db_table = "symptoms"
    # The id of the daystat entry that owns this symptom
    # owner = models.ManyToManyField(DayStat)
    s_id = models.IntegerField("s_id")
    name = models.CharField("symptom", max_length=100)


class DayStat(models.Model):
    class Meta:
        db_table = "day_stat"

        verbose_name = "day"

        verbose_name_plural = "days"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    day_idx = models.IntegerField('day_number')
    general_eval = models.IntegerField('general_self_evaluation(1-4)')
    body_temp = models.DecimalField('body_temperature', max_length=11, decimal_places=1, max_digits=20)
    sleep_time = models.DecimalField('sleep_time', max_length=11,decimal_places=1, max_digits=20)
    health_score = models.IntegerField('health_score', null=True)
    blog = models.TextField("description", null=True)
    symptoms = models.ManyToManyField(Symptom)

    # Also, symptoms, many to many field


