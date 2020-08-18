from django.contrib import messages
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect

from product.models import commentForm, comment


def index(request):
    return HttpResponse("my product page")

def addcomment(request):
    return HttpResponse("add comment")

def addcomment(request,id):
   url = request.META.get('HTTP_REFERER')

   if request.method == 'POST':
      form = commentForm(request.POST)
      if form.is_valid():
         data = comment()
         data.subject = form.cleaned_data['subject']
         data.comment = form.cleaned_data['comment']
         data.rate = form.cleaned_data['rate']
         data.ip = request.META.get('REMOTE_ADDR')
         data.product_id=id
         current_user= request.user
         data.user_id=current_user.id
         data.save()
         messages.success(request, "Your review has ben sent. Thank you for your interest.")
         return HttpResponseRedirect(url)
