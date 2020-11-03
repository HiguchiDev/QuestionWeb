from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import reverse

class TopRefirectView(TemplateView):
    #template_name = "question_main.html"

    def get(self, request, **kwargs):
        return HttpResponseRedirect(reverse('top'))