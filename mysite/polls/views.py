from pyexpat import model
from django.urls import reverse

from django.http import Http404,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.sites.shortcuts import get_current_site
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login,logout
from django.views import generic
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_text
from django.contrib.auth.models import User
from .forms import SignUp
from .tokens import account_activation_token
# Create your views here.

class IndexView(generic.ListView):
    template_name = "home.htm"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]

class DetailsView(generic.DetailView):
    model=Question
    template_name = "details.htm"



class ResultsView(generic.DetailView):
    model=Question
    template_name = "results.htm"

def vote(r,question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=r.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(r,"details.htm",{
            'question':question,
            'error_message':"you did not slected choice"
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse("results", args=(question.id,)))


def register(r):
    userForm = SignUp(r.POST or None)

    if r.method == "POST":
        if userForm.is_valid():
            user = userForm.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(r)
            subject = "Activate your Poll Portal Account"
            message = render_to_string("registration/account_activate_email.html",{
                    'user': user,
                    'domain': current_site.domain,
                    'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),

            })
            user.email_user(subject,message)
            return redirect("account_activation_sent")


    return render(r,"registration/register.html",{
        'userForm': userForm
    })

def account_activation_sent(r):
    return render(r,"registration/account_activation_sent.html")

    
def activate(r,uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(r,user)
        return redirect("home")
    else:
        return render(r,"registration/account_activation_invalid.html")

def loginFunction(r):
    userForm = AuthenticationForm(r.POST or None)
    if r.method == "POST":
        username = r.POST.get("username")
        password = r.POST.get("password")
        user = authenticate(username=username,password=password)
        login(r,user)
        return redirect("home")

    return render(r,"registration/login.html",{
        "userForm": userForm
    })

def logoutUser(r):
    logout(r)
    return redirect("login")