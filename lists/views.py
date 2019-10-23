from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item

# Create your views here.
def home_page(request):
	if request.method == "POST":
		# new_item_text = request.POST['item_text']
		# .objects.create is shorthand for creating new Item w/o needing to call .save()
		Item.objects.create(text=request.POST['item_text'])		

		return redirect('/')


	return render(request, 'home.html', {'items': Item.objects.all()})

