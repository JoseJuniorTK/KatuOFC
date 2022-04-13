from html.entities import name2codepoint
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import os
import json
from intmeta.intmetapp import core
from intmeta.intmetapp import subcalls

# Create your views here.

def index(request):
    return render(request, 'index.html')

def kraken(request):
    global attribute, dfd3, maxpercent, dfd3_2, maxreads, total_reads
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        attribute = request.POST.get('attributeid')
        savefile = FileSystemStorage()
        name = savefile.save(uploaded_file.name, uploaded_file) # pega o nome do arquivo
        d = os.getcwd() # how we get the current directory
        file_directory = d+'/media/'+name #saving the file in the media directory
        print("kraken file")
        # Tratamento de erro, modifica o comportamento a cada erro identificado
        try:
            dfd3, dfd3_2, maxpercent, maxreads, total_reads = core.kraken(file_directory, attribute)    
        except IndexError:
            return redirect(index)
        except ValueError:
            return redirect(index)
        subcalls.krakenkrona(file_directory)
        return redirect(results)
    return render(request, 'kraken.html')


def clark(request):
    global attribute, dfd3, maxpercent, dfd3_2, maxreads, total_reads
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        savefile = FileSystemStorage()
        name = savefile.save(uploaded_file.name, uploaded_file) # pega o nome do arquivo
        uploaded_file2 = request.FILES['document2']
        savefile2 = FileSystemStorage()
        name2 = savefile2.save(uploaded_file2.name, uploaded_file2) # pega o nome do arquivo
        d = os.getcwd() # how we get the current directory
        file_directory = d+'/media/'+name #saving the file in the media directory
        file_directory2 = d+'/media/'+name2 #saving the file in the media directory
        # Tratamento de erro, modifica o comportamento a cada erro identificado
        try:
            dfd3, dfd3_2, maxpercent, maxreads, total_reads = core.clark(file_directory) 
        except IndexError:
            return redirect(index)
        except ValueError:
            return redirect(index)             
        subcalls.clarkkrona(file_directory2)
        return redirect(results)
    return render(request, 'clark.html')


def metamaps(request):
    return render(request, 'metamaps.html')


def about(request):
    return render(request, 'about.html')


def krona(request):
    return render(request, 'krona.html')    


def results(request):
    # O arquivo volta do parse já convertido para dicionário
    # Agora nós convertemos o dicionário para JSON
    dfd3_json = json.dumps(dfd3, indent = 4, default=str, ensure_ascii=False)
    return render(request, 'results.html', {'dfd3_json':dfd3_json, 'dfd3_2':dfd3_2, 'maxreads':maxreads,'total_reads':total_reads, 'maxpercent':maxpercent})