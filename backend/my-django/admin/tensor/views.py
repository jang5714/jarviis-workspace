from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

from admin.tensor.models import Calculator, FashionClassification

import matplotlib.pyplot as plt

@api_view(['GET'])
@parser_classes([JSONParser])
def calculator(request):
    Calculator().process()
    return JsonResponse({'calculator': 'Success'})

@api_view(['GET'])
@parser_classes([JSONParser])
def fashion(request):
    FashionClassification().fashion()
    return JsonResponse({'FashionClassification': 'Success'})
