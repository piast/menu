from django.db import models
from django.urls import reverse


class Menu(models.Model):
    title = models.CharField(max_length=20, verbose_name='Menu title')
    slug = models.SlugField(max_length=255, verbose_name='Slug', null=True)
    named_url = models.CharField(max_length=255, verbose_name='Named URL', blank=True)

    class Meta:
        verbose_name = 'menu'
        verbose_name_plural = 'menu'

    def __str__(self):
        return self.title

    def get_url(self):
        if self.named_url:
            url = reverse(self.named_url)
        else:
            url = 'f/{self.slug}/'
        return url



class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name='items', verbose_name='menu',
                                blank=True, null=True, on_delete=models.CASCADE)

    parent = models.ForeignKey('self', blank=True, null=True, related_name='children',
                                verbose_name='parent menu item', on_delete=models.CASCADE)

    title = models.CharField(max_length=100, verbose_name='Item title')
    url = models.CharField(max_length=255, verbose_name='Link', blank=True)
    named_url = models.CharField(max_length=255, verbose_name='Named URL', blank=True)

    level = models.IntegerField(verbose_name='Level in tree', default=0,
        help_text='')

    position = models.IntegerField(verbose_name='Position', null=True,
        help_text='Item position among other site tree items under the same parent. Stating from 0')



    def save(self, *args, **kwargs):
        if self.parent:
            self.level = self.parent.level + 1

        all_neighbours = MenuItem.objects.filter(
            parent=self.parent, menu=self.menu).exclude(id=self.id).order_by('-position')

        try:
            last_position = all_neighbours[0].position
        except IndexError:
            last_position = None


        if (last_position and self.position) is not None:
            if self.position <= last_position:
                for neighbour in all_neighbours:
                    if neighbour.position >= self.position:
                        MenuItem.objects.filter(id=neighbour.id).update(position=neighbour.position + 1)
        elif last_position is not None and self.position is None:
            self.position = last_position + 1
        elif (last_position and self.position) is None:
            self.position = 0

        return super(MenuItem, self).save(*args, **kwargs)


    class Meta:
        verbose_name = 'menu item'
        verbose_name_plural = 'menu items'
        ordering = ('position', )

    def get_url(self):
        if self.named_url:
            url = reverse(self.named_url)
        elif self.url:
            url = self.url
        else:
            url = '/'

        return url

    def __str__(self):
        return self.title