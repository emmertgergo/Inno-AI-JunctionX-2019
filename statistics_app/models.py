from django.db import models
from children_app.models import Child
from tale_app.models import Tale, Content


class Session(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    tale = models.ForeignKey(Tale, models.CASCADE)
    child = models.ForeignKey(Child, models.CASCADE)
    completed = models.BooleanField(db_column='completed', default=False)
    date = models.DateTimeField(db_column='date', auto_now=True)
    content_id = models.IntegerField()
    image_path = models.CharField(db_column='image_path', blank=True,max_length=255)

    def __str__(self):
        return 'ID: {} Child name: {} Tale: {}'.format(self.id, self.child.name, self.tale.name)


class Result(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    session = models.ForeignKey(Session, models.CASCADE)
    content = models.ForeignKey(Content, models.CASCADE)
    emotion_0 = models.FloatField(null=True)
    emotion_1 = models.FloatField(null=True)
    emotion_2 = models.FloatField(null=True)
    emotion_3 = models.FloatField(null=True)
    emotion_4 = models.FloatField(null=True)
    emotion_5 = models.FloatField(null=True)
    emotion_6 = models.FloatField(null=True)
    emotion_7 = models.FloatField(null=True)
    time = models.DateTimeField(db_column='time', auto_now=True)
    image = models.ImageField(db_column='image', upload_to='azure_app/pictures', blank=True)

    class Meta:
        db_table = 'result'
        unique_together = ('session', 'content')

    def __str__(self):
        return 'ID: {} Child name: {}'.format(self.id, self.session.child.name)
