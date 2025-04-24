from django.shortcuts import render


def concept(request):
    """
    View to render concept page
    """
    return render(request, 'concept/concept.html')
