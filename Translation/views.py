from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import JsonResponse, HttpResponseBadRequest
import json

from .models import Key
from .models import Translation
from .form import TranslationForm
from .form import KeyForm

import detectlanguage


detectlanguage.configuration.api_key = "ee97da1f2c23d8274796a0b99fd620c8"

@method_decorator(csrf_exempt, name='dispatch')
class Key_Get_Post_View(View):
    def get(self, requuest):
        queryset = Key.objects.all()
        json_result = []

        if not queryset.exists() :
            return HttpResponseBadRequest('Object Not Exist - Key Object does not exist')

        for key in queryset:
            json_object = dict(id = key.id, name = key.name)
            json_result.append(json_object)
        return JsonResponse ({"keys" : json_result})

    def post(self, request):
        received_json_data=json.loads(request.body)
        # check {name} is empty
        try:
            Dictionary_data = dict(
                name = received_json_data['name'],
            )
        except:
            return HttpResponseBadRequest('Invalid name - name is empty')

        form = KeyForm(Dictionary_data)
        if form.is_valid():
            Key_Object = Key.objects.create(name = form.cleaned_data['name'])
            return JsonResponse({
                "key" : {
                    "id" : Key_Object.id,
                    "name" : Key_Object.name
                }
            })
        else :
            return HttpResponseBadRequest(form.message)


@method_decorator(csrf_exempt, name='dispatch')
class Key_Update_View(View):
    def put(self, request, pk):
        received_json_data=json.loads(request.body)
        try:
            Dictionary_data = dict(
                name = received_json_data['name'],
            )
        except:
            return HttpResponseBadRequest('Invalid name - name is empty')

        form = KeyForm(Dictionary_data)
        if form.is_valid():
            try:
                Key_Object = Key.objects.get(id = pk)
            except:
                return HttpResponseBadRequest('Object Not Exist - Key with [ "id" : ' + id + ' ] does not exist')

            Key_Object.name = received_json_data['name']
            Key_Object.save()
            return JsonResponse({
                "key" : {
                    "id" : Key_Object.id,
                    "name" : Key_Object.name
                }
            })
        else :
            return HttpResponseBadRequest(form.message)


#TODO : db optimization
@method_decorator(csrf_exempt, name='dispatch')
class Translation_Get_Put_Post_View(View):
    def get(self, requuest, keyId, locale):
        Key_Object = Key.objects.filter(id = keyId)
        if not Key_Object.exists():
            return HttpResponseBadRequest('Invalid keyId - Key Object with [ "id" : ' + str(keyId) + ' ] does not exist')

        try:
            Translation_Objects = Translation.objects.filter(keyId = Key_Object[0], locale = locale)
            return JsonResponse ({
                "translation": {
                    "id" : Translation_Objects[0].id,
                    "keyId" : keyId,
                    "locale" : locale,
                    "value" : Translation_Objects[0].value
                }
            })
        except :
            return HttpResponseBadRequest('Object Not Exist - Translation Object with ["keyId" : ' + str(keyId) + ', "locale" : ' + locale + '] does not exist')

    def put(self, request, keyId, locale):
        Key_Object = Key.objects.filter(id = keyId)
        if not Key_Object.exists():
            return HttpResponseBadRequest('Invalid keyId - Key Object with [ "id" : ' + str(keyId) + ' ] does not exist')

        received_json_data=json.loads(request.body)
        try:
            Dictionary_data = dict(
                keyId = keyId,
                locale = locale,
                value = received_json_data['value'],
            )
        except:
            return HttpResponseBadRequest('Invalid value - value is empty')

        form = TranslationForm(Dictionary_data)
        if form.is_valid() :
            try:
                Translation_Objects = Translation.objects.filter(keyId = Key_Object[0], locale = locale)
                Translation_Object = Translation_Objects[0]
            except:
                return HttpResponseBadRequest('Object Not Exist - Translation Object with ["keyId" : ' + str(keyId) + ', "locale" : ' + locale + '] does not exist')
            Translation_Object.value = received_json_data['value']
            Translation_Object.save()
            return JsonResponse({
                "translation": {
                    "id" : Translation_Object.id,
                    "keyId" : Translation_Object.keyId.id,
                    "locale" : Translation_Object.locale,
                    "value" : Translation_Object.value
                }
            })
        else :
            return HttpResponseBadRequest(form.message)

    def post(self, request, keyId, locale):
        Key_Object = Key.objects.filter(id = keyId)
        if not Key_Object.exists():
            return HttpResponseBadRequest('Invalid keyId - Key Object with [ "id" : ' + str(keyId) + ' ] does not exist')

        received_json_data=json.loads(request.body)
        try:
            Dictionary_data = dict(
                keyId = keyId,
                locale = locale,
                value = received_json_data['value'],
            )
        except:
            return HttpResponseBadRequest('Invalid value - value is empty')

        Translation_Object = Translation.objects.filter(keyId = Key_Object[0], locale = locale)
        if Translation_Object.exists():
            return HttpResponseBadRequest('Duplicate POST - Translation with { keyId : ' + str(keyId) + ', locale : ' + locale + ' } already exists')

        form = TranslationForm(Dictionary_data)
        if form.is_valid():
            Translation_Object = Translation.objects.create(
                keyId = Key_Object[0],
                locale = locale,
                value = received_json_data['value']
            )
            return JsonResponse({
                "translation": {
                    "id" : Translation_Object.id,
                    "keyId" : Translation_Object.keyId.id,
                    "locale" : Translation_Object.locale,
                    "value" : Translation_Object.value
                }
            })
        else :
            return HttpResponseBadRequest(form.message)


class Translations_Get_View(View):
    def get(self, request, keyId):
        KeyObject = Key.objects.filter(id = keyId)
        if not KeyObject.exists():
            return HttpResponseBadRequest('Invalid keyId - Key Object with [ "id" : ' + str(keyId) + ' ] does not exist')

        TransObjects = Translation.objects.filter(keyId = KeyObject[0])
        if not TransObjects.exists():
            return HttpResponseBadRequest('Object Not Exist - Translation Object with [ "keyId" : ' + str(keyId) + ' ] does not exist')

        json_result = []
        for Trans in TransObjects:
            json_object = dict(id = Trans.id, keyId = keyId, locale = Trans.locale, value = Trans.value)
            json_result.append(json_object)
        return JsonResponse ({"translations" : json_result})


class Language_Get_View(View):
    def get(self, request):
        StringToFindLocale = request.GET.get('message')
        if not StringToFindLocale:
            return HttpResponseBadRequest('Message Not Exist - Message to find locale does not exist')
        detectResult = detectlanguage.simple_detect(StringToFindLocale)
        return JsonResponse({
            "locale" : detectResult
            })
