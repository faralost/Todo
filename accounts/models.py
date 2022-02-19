from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE,
                                verbose_name='Профиль')
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars', verbose_name='Аватар')
    github_profile = models.URLField(verbose_name='Ссылка на Гитхаб', null=True, blank=True)
    about = models.TextField(max_length=1000, verbose_name='О себе', null=True, blank=True)

    def __str__(self):
        return f"Профиль: {self.user.username}. {self.id}"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
