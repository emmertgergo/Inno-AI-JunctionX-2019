from django.db import models
from django.contrib.auth.models import User


class Child(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='Name', max_length=128, blank=True, null=True)
    image = models.ImageField(db_column='image', upload_to='children_app/pictures', blank=True)
    user = models.ForeignKey(User, models.CASCADE, db_column='userID')
    wholescore = models.IntegerField(blank=True, default=0)
    sessionscore = models.IntegerField(blank=True, default=0)
    emojitype = models.IntegerField(blank=True, default=1)


    class Meta:
        db_table = 'child'

    def __str__(self):
        return 'ID:{} Name:{}'.format(self.id, self.name)
