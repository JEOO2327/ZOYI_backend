from django.db import models

class Key(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.TextField(unique = True)

class Translation(models.Model):
    id = models.AutoField(primary_key = True)
    key_id = models.ForeignKey(Key, related_name = 'translations', on_delete = models.CASCADE)
    value = models.TextField()

    locale = models.CharField(max_length = 2,
            choices = (
                ('ko', 'KOREAN'),
                ('en', 'ENGLISH'),
                ('ja', 'JAPANESE')
            )
        )
