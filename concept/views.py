from django.shortcuts import render

def concept(request):
    return render(request, 'concept/concept.html')
