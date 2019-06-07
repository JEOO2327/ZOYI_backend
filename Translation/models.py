from django.db import models

#TODO : name이 dot과 영어 소문자만 입력 받도록 하기
class Key(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.TextField(unique = True)

class Translation(models.Model):
    id = models.AutoField(primary_key = True)
    key_id = models.ForeignKey(Key, related_name = 'translations', on_delete = models.CASCADE)

    locale = models.TextField(
            choices = (
                ('ko', 'KOREAN'),
                ('en', 'ENGLISH'),
                ('ja', 'JAPANESE')
            )
        )

    value = models.TextField()
