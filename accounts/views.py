from ecommerce.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_POST
from django.views.generic.detail import DetailView

from .forms import LoginForm, SignupForm, UserChangeForm
from .models import User, EmailToken

from store.models import Order, ShippingAddress
from store.forms import ShippingAddressForm
# Create your views here.

# the reason i named it like that is because login is the name of the function
# used to log the user in
def sign_in(request):
    if request.user.is_authenticated:
        return redirect('/')

    redirect_url = request.POST.get('next') or '/'

    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect(redirect_url)
        form.add_error(
            field = 'email',
            error = 'error: please make sure that you provided the right credentials'
        )
    return render(request, 'accounts/login.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('store:home-page')
    form = SignupForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        return redirect('accounts:login')
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def settings_view(request):
    form = UserChangeForm(instance=request.user)
    shipping_address_form = ShippingAddressForm()
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return redirect('accounts:settings')
        else:
            return HttpResponse('inalid form')
    context = {
        'form': form,
        'shipping_address_form': shipping_address_form
    }
    return render(request, 'accounts/settings.html', context)


@require_POST
@login_required(login_url='/account/login')
def change_email(request):
    user = request.user  
    t = EmailToken.objects.create(user=user)
    host = request.get_host()
    path = reverse('accounts:old-token-validation', kwargs={'token': t})
    old_email_confirmation_link = f'http://{host}{path}'
    recipient = request.user.email

    send_mail(
        subject = 'request for changing email',
        message = 'I do not know how is this gonna be displayed',
        html_message = f'hey {request.user.first_name}, you requested changing your email, click on this link to proceed, <a href="{old_email_confirmation_link}" target="_blank"> click here </a>',
        from_email = EMAIL_HOST_USER,
        recipient_list = [recipient],
        fail_silently=False,
        )

    return redirect('accounts:token_sent_success')

@login_required(login_url='/account/login')
def token_sent_success(request):
    email = request.user.email
    return render(request, 'accounts/token_sent_success.html', {'email':email})

@login_required(login_url='/account/login')
def old_token_validation(request, token):
    # get the token from the url argument and look it up using the token string
    # if it's active, deactivate it, and redirect to entering new email view
    try:
        token_obj = EmailToken.objects.get(token=token)
        if token_obj.active:
            token_obj.active = False
            token_obj.save()
            return render(request, 'accounts/token_validated.html')
    except Exception as error:
        return render(request, 'accounts/token_error.html', {'error':error})

# when you get back from the gym, make the view to send the new email token, one to confirm it and change the email, and one to say
# the operation was successful

@require_POST
@login_required(login_url='/account/login')
def new_email_token(request):
    recipient = request.POST.get('email')

    # try if the new email is already taken
    try:
        email_exists = User.objects.get(email=recipient)
        return HttpResponse('this email is taken, please try again')
    except:
        pass

    user = request.user  
    t = EmailToken.objects.create(user=user)
    host = request.get_host()
    path = reverse('accounts:new-token-validation', kwargs={'token': t})
    new_email_confirmation_link = f'http://{host}{path}'

    send_mail(
        subject = 'new email confirmation',
        message = 'I do not know how is this gonna be displayed',
        html_message = f'hey {request.user.first_name}, you requested changing your email, click on <a href="{new_email_confirmation_link}" target="_blank"> this link </a> to confirm your new email',
        from_email = EMAIL_HOST_USER,
        recipient_list = [recipient],
        fail_silently=False,
        )

    request.session['email'] = recipient

    return redirect('accounts:new-email-token-sent-success')

@login_required(login_url='/account/login')
def new_email_token_sent_success(request):
    email = request.session['email']
    return render(request, 'accounts/new-email-token-sent-success.html', {'email':email})

@login_required(login_url='/account/login')
def new_token_validation(request, token):
    try:
        token_obj = EmailToken.objects.get(token=token)
        user = request.user
        if token_obj.active:
            token_obj.active = False
            token_obj.save()
            user.email = request.session['email']
            user.save()
            del request.session['email']
            return render(request, 'accounts/new-token-validated.html')
    except Exception as error:
        return render(request, 'accounts/token_error.html', {'error': error})

@login_required(login_url='/account/login')
def new_token_validated(request):
    return render(request, ('accounts/new-token-validated.html'))

class OrderDetails(DetailView):
    model = Order
    slug_field = 'order_id'
    slug_url_kwarg = 'order_id'
    template_name = 'accounts/order_details.html'


# try to figure out how to do it with CBVs
@require_POST
def add_shipping_address(request):
    form = ShippingAddressForm(request.POST)
    if form.is_valid():
        address = form.save(commit=False)
        address.user = request.user
        address.save()
        return redirect('accounts:settings')

@require_POST
def delete_shipping_address(request, address_pk):
    address = ShippingAddress.objects.get(pk=address_pk)
    address.delete()
    redirect_path = request.POST.get('redirect_path')
    return redirect(redirect_path)