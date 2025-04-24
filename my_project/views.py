from django.shortcuts import render
from django.contrib.auth.views import PasswordResetView


def handler404(request, exception):
    """ Error Handler 404 - Page Not Found """
    return render(request, "errors/404.html", status=404)


class TextOnlyPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.txt'
    subject_template_name = 'registration/password_reset_subject.txt'

    def form_valid(self, form):
        print(">>> MA VUE EST UTILISÉE <<<")
        return super().form_valid(form)
