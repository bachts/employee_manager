from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import OkrForm
# Create your views here.

def get_okr(request):
    if request.method == 'POST':
        
        form = OkrForm(request.POST)
        
        if form.is_valid():
            print(form.cleaned_data)
            return HttpResponseRedirect('/yes/')
    else:
        form = OkrForm()

      
    return render(request, 'okrform.html', {'form': form.as_p()})