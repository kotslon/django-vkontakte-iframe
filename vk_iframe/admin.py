#coding: utf-8
from django.contrib import admin
from vk_iframe.models import Country, City, Profile
from vk_iframe.utils import get_app_id, get_app_secret
from django.utils.translation import ugettext_lazy as _


class CountryAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']


class CityAdmin(admin.ModelAdmin):
    list_display = ['title', 'country', 'id']
    list_filter = ['country']
    search_fields = ['title', 'id']

    actions = ['load_from_vkontakte']

    def load_from_vkontakte(self, request, queryset):
        import vkontakte
        api = vkontakte.API(get_app_id(), get_app_secret(), timeout=5)
        cids = ','.join([str(city.pk) for city in queryset])
        vk_data = api.getCities(cids=cids)
        for item in vk_data:
            city = City.objects.get(pk=item['cid'])
            city.title = item['name']
            city.save()
    load_from_vkontakte.short_description = _("Load city data")


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__first_name', 'user__last_name', 'user__username',
                     'vk_id', 'domain', 'home_phone', 'mobile_phone']

admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Profile, ProfileAdmin)
