from django.shortcuts import render
from test_app.models import TestModel
from daguerre.helpers import adjust


# Create your views here.
def index(request):
    my_model = TestModel.objects.get()
    import pdb; pdb.set_trace()
    return render(request, 'index.html', {'my_model': my_model})
