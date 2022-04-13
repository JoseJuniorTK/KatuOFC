import os, os.path
import subprocess

# Modulo de chamadas de subprocessos, executamos scripts aqui onde cada argumento 
# E programa é unido em um unico comando chamado pelo subprocess call.

def krakenkrona(fileinput):
    # Camada de segurança pra garantir que a informação errada não seja passada para o html que a pessoa vai visualizar
    # É feita a contagem de arquivos temporarios no diretorio e é atribuido um numero a cada uma
    # Assim o arquivo sempre vai carregar o temporario correto.
    DIR = './tmpfiles/krona'
    filecount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    # Argumentos e a chamada do programa
    programa = './intmeta/intmetapp/krona/kreport2krona.py'
    arg1_1 = '-r'
    arg2_1 = str(fileinput)
    arg3_1 = '-o'
    nomesaida = f'tmpfiles/krona/Kronatmp{filecount}.krn'
    subprocess.call([programa, arg1_1, arg2_1, arg3_1, nomesaida], shell=False)

    # Conversão arquivo krona para html
    programa = './intmeta/intmetapp/krona/scripts/ImportText.pl'
    arg1_2 = str(nomesaida)
    arg2_2 = '-o'
    nomehtml = 'templates/krona.html'
    subprocess.call([programa, arg1_2, arg2_2, nomehtml], shell=False)
    return 0

def clarkkrona(fileinput):
    # Conversão arquivo krona para html
    programa = './intmeta/intmetapp/krona/scripts/ImportTaxonomy.pl'
    arg1_2 = str(fileinput)
    arg2_2 = '-o'
    nomehtml = 'templates/krona.html'
    subprocess.call([programa, arg1_2, arg2_2, nomehtml], shell=False)
    return 0