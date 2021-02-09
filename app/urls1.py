from django.urls import path
from django.views.generic import TemplateView
from .views import (
    add_to_cart,
    home_view,
    contact_view,
    about_view,
    letters,
    HomeView,
    remove_from_cart,
    OrderSummaryView,
    CheckoutView,
    success,
    failure,
    cancel,
    error404,
    viewpdf,
    organizations_trained,
    pilot_list,
    gallery,
    testimonial,
    course_detail
)

app_name = 'app'

urlpatterns = [

    # URLs for navbar and homepage
    path('', home_view, name="home"),
    path('courses_list/', HomeView.as_view(), name='courses'),
    path('about/', about_view, name="about"),
    path('gallery/', gallery, name="gallery"),
    path('instructors/', TemplateView.as_view(template_name='app/instructors.html'), name="instructors"),
    path('FAQs/', TemplateView.as_view(template_name='app/faqs.html'), name="FAQs"),
    path('DGCA/', TemplateView.as_view(template_name='app/dgca.html'), name="DGCA"),
    path('certification/', TemplateView.as_view(template_name='app/certification.html'), name="certification"),
    path('pilot-list/', pilot_list, name="pilot-list"),
    path('drone-jobs/', TemplateView.as_view(template_name='app/about_us.html'), name="drone-jobs"),
    path('testimonials/', testimonial, name="testimonials"),
    path('news-and-events/', TemplateView.as_view(template_name='app/news-events.html'), name="news-and-events"),
    path('infrastructure/', TemplateView.as_view(template_name='app/infrastructure.html'), name="infrastructure"),
    path('organizations-trained/', organizations_trained, name="organizations"),
    path('contact/', contact_view, name="contact"),
    path('satisfactory-letters/', letters, name="letters"),
    path('error/', error404, name="error"),

    # URLs for Courses, Cart, Payment and pdf
    path('course/<slug>/', course_detail, name='course-detail'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('success/', success, name='order.success'),
    path('failure/', failure, name='order.failure'),
    path('cancel/', cancel, name='order.cancel'),

    path('pdf_view/<slug:tid>', viewpdf, name="pdf_view"),

    path('pdf_template/', TemplateView.as_view(template_name='app/invoice.html'))

]