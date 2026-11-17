from django.http import HttpResponse


def health(request):
    return HttpResponse("FixIt está no ar.")
