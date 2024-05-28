from django import template
import math

register = template.Library()


@register.simple_tag
def call_sellprice(price, discount):
    if discount is None or discount is 0:
        return price
    
    sellprice = price
    sellprice = price - (price * discount / 100)
    return math.floor(sellprice)


@register.simple_tag
def progress_bar(quantity, availability):
    if quantity <= 0:
        return 0  # Avoid division by zero

    progress_percentage = (availability * 100) / quantity
    return math.floor(progress_percentage)