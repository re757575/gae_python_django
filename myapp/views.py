from django.http import HttpResponse
from django.shortcuts import render
import random

def home(request):
    excuses = [
        "It was working in my head",
        "I thought I fixed that",
        "Actually, that is a feature",
        "It works on my machine",
    ]

    excuse = random.choice(excuses)
    return render(request, "index.html", {'excuse': excuse})
