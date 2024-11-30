from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from .api import EconomicsAPI
from django.http import StreamingHttpResponse
import json


class index(TemplateView):
    template_name = "economics/index.html"
    context = {}
    
    def get(self, request):
        
        return render(request, self.template_name, self.context)


# Get all current values
def get_current_values():

    api = EconomicsAPI()
    
    for indicator in api.INDICATORS_DICT:
        data = api.indicator_current(indicator)
        yield data


# return once value at a time
def fetch_all_values(request):
    
    def stream_indicators():
        api = EconomicsAPI()
        for data in get_current_values():
            # Convert the dictionary to JSON and yield it line by line
            yield json.dumps(data) + "\n"

    # Use StreamingHttpResponse to stream the data
    return StreamingHttpResponse(stream_indicators(), content_type="application/json")


# Get current value
def get_current_value(request,indicador, year):

    api = EconomicsAPI()

    return api.indicator_current(indicador, year)