from django import template
from app.models import Order

# register template tag
register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)  # orders by the user, excluding previous orders
        if qs.exists():
            return qs[0].items.count()
    return 0
