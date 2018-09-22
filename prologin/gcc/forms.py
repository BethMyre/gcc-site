import json

from datetime import date

from django import forms

from gcc.models import Question, Answer, Forms, AnswerTypes, Event


class EmailForm(forms.Form):
    # See here for why 254 max
    # http://www.rfc-editor.org/errata_search.php?rfc=3696&eid=1690
    email = forms.EmailField(label='Adresse électronique', max_length=254)


def build_dynamic_form(form, user):
    """
    Initialize a django form with fields described in models.Question
    :param form: the form that must be displayed / edited
    :type form: models.Form
    :type user: settings.AUTH_USER_MODEL
    """

    class DynamicForm(forms.Form):
        """
        A form generated for a specific set of questions, specificly for one user.

        `form` and `user` are the parameters of function gcc.models.build_dynamic_form(form)
        which generated this class.
        """

        def __init__(self, *args, **kwargs):
            super(DynamicForm, self).__init__(*args, **kwargs)

            # Add fields to the form
            self.questions = \
                Question.objects.filter(form=form.value).order_by('order')

            for question in self.questions:
                # set basic fields parameters
                basic_args = {
                    'label': question.question,
                    'required': question.required,
                    'help_text': question.comment
                }
                fieldId = 'field' + str(question.pk)

                # Try to load existing configuration
                try:
                    answer = Answer.objects.get(question=question, user=user)
                    basic_args['initial'] = answer.response
                except Answer.DoesNotExist:
                    pass

                if question.response_type == AnswerTypes.boolean.value:
                    self.fields[fieldId] = forms.BooleanField(**basic_args)
                elif question.response_type == AnswerTypes.integer.value:
                    self.fields[fieldId] = forms.IntegerField(**basic_args)
                elif question.response_type == AnswerTypes.date.value:
                    self.fields[fieldId] = forms.DateField(**basic_args)
                elif question.response_type == AnswerTypes.string.value:
                    self.fields[fieldId] = forms.CharField(**basic_args)
                elif question.response_type == AnswerTypes.text.value:
                    self.fields[fieldId] = forms.CharField(widget=forms.Textarea, **basic_args)

        def save(self):
            """
            Saves all filled fields for `user`.
            """
            data = self.cleaned_data

            for question in self.questions:
                fieldId = 'field' + str(question.pk)

                if data[fieldId] is not None:
                    # Try to modify existing answer, overwise create a new answer
                    try:
                        answer = Answer.objects.get(user=user, question=question)
                    except Answer.DoesNotExist:
                        answer = Answer(
                            user = user,
                            question = question
                        )

                    answer.response = data[fieldId]
                    answer.save()

    return DynamicForm


class ApplicationValidationForm(forms.Form):
    """
    Select the top three events a candidate wants to participate in.
    """
    # Get a list of (primary_key, event name) for the selectors
    events = Event.objects.filter(
        signup_start__lt = date.today(),
        signup_end__gt = date.today()
    )
    events_selection = [(None, '')] + [(event.pk, str(event)) for event in events]

    priority1 = forms.TypedChoiceField(label='1er choix', choices=events_selection, required=True)
    priority2 = forms.TypedChoiceField(label='2nd choix', choices=events_selection)
    priority3 = forms.TypedChoiceField(label='3e choix', choices=events_selection)
