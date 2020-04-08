from django import template

register=template.Library()

@register.filter
def convertirTipoDocumento(value):
    if value==0:
        return "Archivo"
    elif value==1:
        return "Flujograma"
    elif value==2:
        return "Video"
    else:
        return value

@register.filter
def convertirLinkYoutube(value):
    p=value.rfind("/")
    value=value[p+1:]
    return value