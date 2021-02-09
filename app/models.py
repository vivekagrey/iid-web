from django.db import models
from account.models import Account
from django.shortcuts import reverse
from payu.models import Transaction
from datetime import datetime
from django.utils.timezone import make_aware, make_naive


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    slug = models.SlugField()
    duration = models.CharField(max_length=10, null=True)
    image = models.ImageField(upload_to='CourseImages/')
    online_course = models.NullBooleanField(blank=False, null=False)  # default is None
    expiry = models.DurationField(verbose_name="Course Expiry", blank=False, null=False, help_text='Eg: 30 days, '
                                                                                                   'enter any number '
                                                                                                   'of days for '
                                                                                                   'offline course')
    description1 = models.CharField(max_length=50, blank=True, null=True)
    description2 = models.CharField(max_length=50, blank=True, null=True)
    description3 = models.CharField(max_length=50, blank=True, null=True)
    description4 = models.CharField(max_length=50, blank=True, null=True)
    description5 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'COURSE'
        verbose_name_plural = 'COURSES'

    def __str__(self):
        return self.title

    def get_add_to_cart_url(self):
        return reverse("app:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("app:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def get_lesson_list(self):
        return reverse("account:lesson_list", kwargs={
            'slug': self.slug
        })

    def get_absolute_url(self):
        return reverse("app:course-detail", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Course")

    class Meta:
        verbose_name = 'COURSE PURCHASED'
        verbose_name_plural = 'COURSES PURCHASED'

    def __str__(self):
        return self.item.title

    def get_total_item_price(self):
        return self.item.price

    def get_item(self):
        return self.item

    #
    def course_age(self):
        order = self.order_set.all()[0]
        age = make_aware(datetime.now()) - order.ordered_date
        course = self.item
        if not course.online_course or age <= course.expiry:
            return True
        else:
            return False

    # returns the date on which, the course will expire
    def get_expiry_date(self):
        order = self.order_set.all()[0]
        course = self.item
        exp_date = order.ordered_date + course.expiry
        return make_naive(exp_date)

    def get_order_transaction(self):
        order = self.order_set.all()[0]
        transaction = order.transaction
        if transaction:
            return transaction.transaction_id
        else:
            return None


class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, blank=True, null=True)
    invoice = models.FileField(upload_to='Invoice/', null=True, blank=True)

    class Meta:
        verbose_name = 'ORDER'
        verbose_name_plural = 'ORDERS'

    def __str__(self):
        return self.user.first_name+str(' ')+self.user.last_name

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total


class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    course = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    thumbnail = models.ImageField(null=True, blank=True, upload_to='LessonThumb/')
    video_file = models.FileField(upload_to='Lesson Videos/')
    description1 = models.CharField(max_length=50, blank=True, null=True)
    description2 = models.CharField(max_length=50, blank=True, null=True)
    description3 = models.CharField(max_length=50, blank=True, null=True)
    description4 = models.CharField(max_length=50, blank=True, null=True)
    description5 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Course Lesson'
        verbose_name_plural = 'Course Lessons'

    def __str__(self):
        return self.title


class CourseCalendar(models.Model):
    course_name = models.CharField(max_length=50)
    date = models.CharField(max_length=20)
    location = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Course Calendar'
        verbose_name_plural = 'Course Calendar'

    def __str__(self):
        return self.course_name


class Query(models.Model):
    first_name = models.CharField(verbose_name="First Name", max_length=20)
    last_name = models.CharField(verbose_name="Last Name", max_length=20)
    email = models.EmailField(verbose_name="Email", max_length=50)
    phone = models.CharField(verbose_name="Phone No.", max_length=20)
    query = models.TextField(verbose_name="Query")

    class Meta:
        verbose_name = 'Query'
        verbose_name_plural = 'Queries'

    def __str__(self):
        return self.email


class Organization(models.Model):
    name = models.CharField(verbose_name="Organization", max_length=50)
    location = models.CharField(verbose_name="Location", max_length=30)

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.name


class PilotList(models.Model):
    name = models.CharField(verbose_name="Pilot Name", max_length=30)
    organization = models.CharField(verbose_name="Organization", max_length=50)
    date = models.DateField()
    course = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    certificate_no = models.CharField(verbose_name="Certificate Number", max_length=20)

    class Meta:
        verbose_name = "Pilot"
        verbose_name_plural = "Pilot List"

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(verbose_name="Student Name", max_length=30)
    location = models.CharField(verbose_name="Location", max_length=20)
    certificate_no = models.CharField(verbose_name="Certificate No", max_length=20)
    video_url = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return self.name


class Gallery(models.Model):
    batch_no = models.CharField(verbose_name="Batch No", max_length=3)
    course = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    location = models.CharField(verbose_name="Location", max_length=20)
    image = models.ImageField(upload_to='Gallery/')
    position = models.AutoField(primary_key=True)

    class Meta:
        verbose_name = 'Batch'
        verbose_name_plural = 'Gallery'

    def __str__(self):
        return self.batch_no
