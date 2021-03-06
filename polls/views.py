from django.utils import timezone

from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic
from polls.models import Question, Choice


class IndexView(generic.ListView):
    """
    ListView generic views uses a default template called <app_name>/<model_name>_list.html. 
    We use template_name to tell ListView to use our existing polls/index.html template. The 
    variable context_object_name designate the name of the variable to use in the context.
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        #return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

        """
        Returns the queryset that will be used to retrieve the object that this view will 
        display. By default, get_queryset() returns the value of the queryset attribute if 
        it is set, otherwise it constructs a QuerySet by calling the all() method on the 
        model attributes default manager.
        """

        """
        Question.objects.filter(pub_date__lte=timezone.now()) returns a queryset containing 
        Questions whose pub_date is less than or equal to - that is, earlier than or equal 
        to - timezone.now.
        """

class DetailView(generic.DetailView):
    """The DetailView genereic view expects the primary key value captured from
    the URL to be called 'pk'. By default, the DetailView generic view uses
    a template polls/question_detail.html. The template_name attribute is used
    to tell Django to use a specific template name instead of the autogenerated
    default template for the results list view.
    """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """
    Each generic view needs to know what model it will be action upon. This is
    provided usind the model attribute.
    """
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', { 'question': p, 'error_message': "You didn't select a choice.", })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

        """
        request.POST is a dictionary-like object that lets you access submitted
        data by key name. In this case, request.POST['choice'] returns the ID
        of the selected choice, as a string. request.POST values are always
        strings.
        """

        """
        request.POST['choice'] will raise KeyError if choice wasnt provided in
        POST data. The above code checks for KeyError and redisplays the question
        form with an error message if choice isnt given.
        """

        """
        After incrementing the choice count, the code returns an
        HttpResponseRedirect rather than a normal HttpResponse.
        HttpResponseRedirect takes a single argument: the URL to which the user
        will be redirected (see the following point for how we construct the URL
        in this case).
        """

        """
        As the Python comment above points out, you should always return an
        HttpResponseRedirect after successfully dealing with POST data. This tip
        isnt specific to Django; its just good Web development practice.
        """

        """
        We are using the reverse() function in the HttpResponseRedirect
        constructor in this example. This function helps avoid
        having to hardcode a URL in the view function. It is given the name
        of the view that we want to pass control to and the variable portion
        of the URL pattern that points to that view. In this case, using the
        URLconf we set up in Tutorial 3, this reverse() call will return a
        string like.
        """
