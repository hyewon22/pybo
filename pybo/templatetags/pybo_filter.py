import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()  #  register는 유효한 tag library를 만들기 위한 모듈 레벨의 인스턴스 객체

@register.filter
def sub(value, arg) :
    return value - arg

@register.filter()
def mark(value) :
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))