from django_filters import FilterSet, DateFilter
from .models import Post, PostCategory
from django.forms import DateInput
import django_filters
# Создаем свой набор фильтров для модели Post
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    datetime_post = DateFilter(
        lookup_expr=('lt'),
        widget=DateInput(attrs={'placeholder': 'Select a date', 'type': 'date'}),
        label='Date',
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'header': ['icontains'],
            # количество товаров должно быть больше или равно
            'author_name': ['gt'],
            'types_post': ['exact'],
        }
class PostCategoryFilter(FilterSet):
    class Meta:
        model = PostCategory
        fields = ['category']