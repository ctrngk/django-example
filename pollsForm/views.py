from django.shortcuts import render

# Create your views here.
########################################
# pollsForm/views.py
########################################

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from .models import Choice, Question
from django import forms
from django.forms import widgets
from .forms import ChoiceForm


class IndexView(generic.ListView):
    template_name = 'pollsForm/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'pollsForm/results.html'


@csrf_protect
def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    c_set = Choice.objects.filter(question=question_id)

    if request.method == 'GET':
        cforms = ChoiceForm()
        cforms.fields['choice_text'] = forms.ModelChoiceField(queryset=c_set,
                                                              empty_label=None,
                                                              widget=widgets.RadioSelect)
        variables = {
            'choice_forms': cforms,
            'question': p,
        }
        return render(
            request,
            'pollsForm/detail.html',
            variables,
        )

    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data['choice_text']
            selected_choice = p.choice_set.get(pk=pk)
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('pollsForm:results', args=(p.id,)))

        if not form.is_valid():
            # change input char to radio
            form.fields['choice_text'] = forms.ModelChoiceField(queryset=c_set,
                                                                empty_label=None,
                                                                widget=widgets.RadioSelect)
            variables = {
               'choice_forms' : form,
                'question': p,
            }
            return render(
                request,
                'pollsForm/detail.html',
                variables,
            )
