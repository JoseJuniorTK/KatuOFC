from html.entities import name2codepoint
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import os
import json
from intmeta.intmetapp import core

# Create your views here.


def index(request):
    return render(request, 'index.html')


def facilitamei_index(request):
    return render(request, 'facilitamei_index.html')
