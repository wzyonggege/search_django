from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def result(request):
    return render(request, 'result.html')


def search(request):
    return


def suggest(request):
    return


