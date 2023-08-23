from django import template

register = template.Library()

CURRENCIES_SYMBOLS = {
    'rub': 'Р',
    'usd': '$',
}


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def currency(value, code='rub'):
    """
      value: значение, к которому нужно применить фильтр
      code: код валюты
      """
    """
    value: значение, к которому нужно применить фильтр
    """
    postfix = CURRENCIES_SYMBOLS[code]
    # Возвращаемое функцией значение подставится в шаблон.
    return f'{value} {postfix}'


@register.filter(name='censors')
def censor(value):
    """
    value: header, content
    """

    stopwords = ['козёл', 'черт', 'редиска']
    word = value.replace(',', "")
    word = word.replace('-', "")
    word = word.split()
    if type(value) is str:
        for word in stopwords:
            value = value.replace(word, word[0] + "*" * (len(word) - 1))
            value = value.replace(word.capitalize(), word[0] + "*" * (len(word) - 1))
    else:
        raise ValueError('Ошибка, это не переменная строкого типа')

    return f'{value}'
