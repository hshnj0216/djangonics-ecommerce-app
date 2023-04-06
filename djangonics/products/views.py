from django.shortcuts import render

# Create your views here.
def browse_all(request):
    return render(request, 'products/browse_all.html')