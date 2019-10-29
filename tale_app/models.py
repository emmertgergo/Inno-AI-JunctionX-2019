from django.db import models


class Tale(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=128, blank=True, null=True)
    image = models.ImageField(db_column='image', upload_to='tale_app/pictures', blank=True)
    level = models.IntegerField(db_column='level', null=False)

    class Meta:
        db_table = 'tale'

    def __str__(self):
        return 'ID:{} Name:{}'.format(self.id, self.name)


class Content(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    taleid = models.ForeignKey(Tale, models.CASCADE, db_column='taleid')
    mp4 = models.FileField(db_column='mp4', upload_to='tale_app/videos', null=True, blank=True)
    targetemotion = models.IntegerField(db_column='targetemotion', blank=True)
    taskimage = models.ImageField(db_column='image', upload_to='tale_app/pictures', null=True, blank=True)
    tasktext = models.CharField(db_column='name', max_length=128, blank=True, null=True)
    type = models.IntegerField(db_column='type', null=False)
    order = models.IntegerField(db_column='order', null=False)

    class Meta:
        db_table = 'content'

    def __str__(self):
        return 'NAME: {} ID:{} ORDER:{}'.format(self.taleid.name, self.id,  self.order)


class EmojiIcon(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    primaryid = models.IntegerField(db_column='primaryid', null=False)
    emotionid = models.IntegerField(db_column='emotionid', null=False)
    image = models.ImageField(db_column='image', upload_to='tale_app/pictures', blank=False)

    class Meta:
        db_table = 'emojiicons'

    def __str__(self):
        return 'PID: {} EID:{}'.format(self.primaryid, self.emotionid)

