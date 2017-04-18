from django.shortcuts import render

# Create your views here.
########################################
# polls/views.py
########################################

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@csrf_protect
def vote(request, question_id):
    # get method
    if request.method == 'GET':
        # <form action="{% url 'polls:vote' question.id %}" method="post">
        p = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/detail.html', {
            'question': p,
        })
    # post method
    # http://localhost:8000/polls/<question.id>/vote/
    # form-data
    # csrfmiddlewaretoken | bBVTmf7ZGudLbWRJ
    # choice | 9
    if request.method == 'POST':
        p = get_object_or_404(Question, pk=question_id)
        try:
            # <input type="radio" name="choice" value="{{ choice.id }}">
            selected_choice = p.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': p,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))