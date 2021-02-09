from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm, ProfileForm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from app.models import Order, OrderItem, Lesson, Item
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import CourseCalendar
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.safestring import mark_safe
from .models import Account


@csrf_protect
@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect("app:home")


# Login and Signup View
@csrf_protect
def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("app:home")

    # Login
    if request.method == 'POST' and 'login' in request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            print("valid")
            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect("app:home")
                else:
                    messages.warning(request, 'Please verify your email address to login!')
                    return redirect('login')

        else:
            try:
                acc = Account.objects.get(email=request.POST['email'])
                if acc.is_active:
                    context['message'] = 'Please enter correct email and password !'
                else:
                    context['message'] = 'Email address not verified!'
                    messages.warning(request, 'Please verify your email address to login.')
            except Account.DoesNotExist:
                context['message'] = 'Please enter correct email and password !'
            context['login_form'] = form
            context['signup_form'] = SignUpForm()

    # Signup
    elif request.method == 'POST' and 'signup' in request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Account Confirmation mail
            current_site = get_current_site(request)  # current site domain
            mail_subject = 'Activate your IID Account.'
            html_message = render_to_string('account/account_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            plain_message = strip_tags(html_message)

            print("Plain message: ", plain_message)
            from_email = None  # This will have no effect is you have set DEFAULT_FROM_EMAIL in settings.py
            to_email = form.cleaned_data.get('email')
            fail_silently = False  # Set to true when Debug is False

            send_mail(mail_subject, plain_message, from_email, [to_email], fail_silently, html_message=html_message)

            messages.info(request, mark_safe("A verification link has been sent to your email account" "<br />"
                                             "Please confirm your email address to complete the registration"))

            return redirect("login")

        else:
            context['login_form'] = LoginForm()
            context['signup_form'] = form

    # get request, display both signup and login forms
    else:
        form = LoginForm()
        from1 = SignUpForm()
        context['login_form'] = form
        context['signup_form'] = from1
    return render(request, 'account/login.html', context)


# Account Activate/Email Confirm View
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        # Welcome Email
        subject = "Welcome to IID"
        html_message = render_to_string('app/welcome_email.html',
                                        {'name': user.first_name + " " + user.last_name,
                                         'confirm_url': request.build_absolute_uri(reverse('app:home')),
                                         'contact_url': request.build_absolute_uri(reverse('app:contact'))})
        plain_message = strip_tags(html_message)
        from_email = None  # This will have no effect is you have set DEFAULT_FROM_EMAIL in settings.py
        to = user.email  # This is a string, will be sent as a list
        fail_silently = False  # True in production

        send_mail(subject, plain_message, from_email, [to], fail_silently, html_message=html_message)

        # Welcome Notification
        messages.success(request, 'Your account has been verified.')
        return redirect('app:home')
    else:
        messages.warning(request, 'Sorry, verification failed! Contact us if the issue persists.')
        return redirect('app:home')


@login_required(login_url='/login')
@csrf_protect
@csrf_exempt
def profile_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("app:home")

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("account:profile")
        else:
            context['profile_form'] = form
    else:
        form = ProfileForm(
            initial={
                "email": request.user.email,
                "phone": request.user.phone,
                "country": request.user.country,
                "dob": request.user.dob,
                "hq": request.user.hq
            }
        )
        context['profile_form'] = form
    return render(request, 'account/profile.html', context)


@login_required(login_url='/login')
def MyCourses(request):
    try:
        order_item = OrderItem.objects.filter(user=request.user, ordered=True)
        # courses = OrderItem
        context = {'order_items': order_item}
        if not order_item:
            messages.info(request, "You haven't purchased any course yet!")
            context['flag'] = True  # True if no courses present
        return render(request, "account/mycourses.html", context)

    except ObjectDoesNotExist:
        context = {'flag': True}
        messages.info(request, "You haven't purchased any course yet!")
        return render(request, "account/mycourses.html", context)


@login_required(login_url='/login')
def LessonList(request, slug):
    try:
        bought_courses = Item.objects.filter(orderitem__user=request.user, orderitem__ordered=True)  # Purchased courses
        course = Item.objects.get(slug=slug)  # course user requesting to view
        context = {}
        if course in bought_courses:
            order_item = OrderItem.objects.get(user=request.user, item=course)
            if order_item.course_age():
                lessons = Lesson.objects.filter(course=course)
                context = {'course': course, 'lessons': lessons}
            else:
                messages.info(request, "Course Expired!")
        else:
            messages.info(request, "You haven't purchased this course!")
        return render(request, "account/lesson_list.html", context)
    except ObjectDoesNotExist:
        return redirect("app:error")


def schedule(request):
    calendar = CourseCalendar.objects.all()

    return render(request, "account/training-schedule.html", {"calendar": calendar})
