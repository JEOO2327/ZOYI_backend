from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
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
        if not queryset.exists() :
            return HttpResponseBadRequest('Object Not Exist - Key Object does not exist')
        return JsonResponse ({
            "keys" : list(queryset.values())
        })

    def post(self, request):
        received_json_data=json.loads(request.body)
        form = KeyForm(received_json_data)
        if form.is_valid():
            key_object = form.save()
            return JsonResponse({
                "key" : model_to_dict(key_object)
            })
        else :
            return HttpResponseBadRequest(form.message)

@method_decorator(csrf_exempt, name='dispatch')
class Key_Update_View(View):
    def put(self, request, pk):
        instance = get_object_or_404(Key, id = pk)
        received_json_data=json.loads(request.body)
        form = KeyForm(received_json_data or None, instance = instance)
        if form.is_valid():
            key_object = form.save()
            return JsonResponse({
                "key" : model_to_dict(key_object)
            })
        else :
            return HttpResponseBadRequest(form.message)

#TODO : db optimization
@method_decorator(csrf_exempt, name='dispatch')
class Translation_Get_Put_Post_View(View):
    def get(self, request, key_id, locale):
        key_object = get_object_or_404(Key, id = key_id)
        translation_object = get_object_or_404(Translation, key_id = key_object, locale = locale)
        return JsonResponse ({
            "translation": model_to_dict(translation_object)
        })

    def put(self, request, key_id, locale):
        key_object = get_object_or_404(Key, id = key_id)
        instance = get_object_or_404(Translation, key_id = key_object, locale = locale)
        # parsing json data to dictionary
        received_json_data=json.loads(request.body)
        received_json_data['locale'] = locale
        received_json_data['key_id'] = key_id

        form = TranslationForm(received_json_data or None, instance = instance)
        if form.is_valid() :
            translation_object = form.save()
            return JsonResponse({
                "translation": model_to_dict(translation_object)
            })
        else :
            return HttpResponseBadRequest(form.message)

    def post(self, request, key_id, locale):
        key_object = get_object_or_404(Key, id = key_id)
        translation_objects = Translation.objects.filter(key_id = key_object, locale = locale)
        # Check duplicate
        if translation_objects.exists():
            return HttpResponseBadRequest('Duplicate POST - Translation with { key_id : ' + str(key_id) + ', locale : ' + locale + ' } already exists')

        received_json_data=json.loads(request.body)
        received_json_data['locale'] = locale
        received_json_data['key_id'] = key_id

        form = TranslationForm(received_json_data)
        if form.is_valid():
            translation_object = form.save()
            return JsonResponse({
                "translation": model_to_dict(translation_object)
            })
        else :
            return HttpResponseBadRequest(form.message)


class Translations_Get_View(View):
    def get(self, request, key_id):
        key_object = get_object_or_404(Key, id = key_id)
        translation_objects = Translation.objects.filter(key_id = key_object)
        if not translation_objects.exists():
            return HttpResponseBadRequest('Object Not Exist - Translation Object with [ "key_id" : ' + str(key_id) + ' ] does not exist')
        return JsonResponse ({"translations" : list(translation_objects.values())})


class Language_Get_View(View):
    def get(self, request):
        string_to_find_locale = request.GET.get('message')
        if not string_to_find_locale:
            return HttpResponseBadRequest('Message Not Exist - Message to find locale does not exist')
        detect_result = detectlanguage.simple_detect(string_to_find_locale)
        return JsonResponse({
            "locale" : detect_result
        })
