from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category, FORBIDDEN_WORDS


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем стили Bootstrap ко всем полям
        for field_name, field in self.fields.items():
            if field_name != 'category':  # Для select особый подход
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-select'

        # Добавляем placeholder для полей
        self.fields['name'].widget.attrs['placeholder'] = 'Введите название товара'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание товара'
        self.fields['price'].widget.attrs['placeholder'] = '0.00'
        self.fields['price'].widget.attrs['step'] = '0.01'
        self.fields['price'].widget.attrs['min'] = '0'

    def clean_name(self):
        """Валидация названия на запрещенные слова"""
        name = self.cleaned_data.get('name')
        if name:
            name_lower = name.lower()
            for word in FORBIDDEN_WORDS:
                if word in name_lower:
                    raise ValidationError(
                        f'Название содержит запрещенное слово: "{word}". '
                        f'Пожалуйста, удалите его.'
                    )
        return name

    def clean_description(self):
        """Валидация описания на запрещенные слова"""
        description = self.cleaned_data.get('description')
        if description:
            desc_lower = description.lower()
            for word in FORBIDDEN_WORDS:
                if word in desc_lower:
                    raise ValidationError(
                        f'Описание содержит запрещенное слово: "{word}". '
                        f'Пожалуйста, удалите его.'
                    )
        return description

    def clean_price(self):
        """Валидация цены (не может быть отрицательной)"""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError(
                'Цена не может быть отрицательной. '
                'Пожалуйста, введите корректную цену.'
            )
        return price

    def clean_image(self):
        """Дополнительная валидация изображения (формат и размер)"""
        image = self.cleaned_data.get('image')
        if image:
            # Проверка размера файла (максимум 5 МБ)
            if image.size > 5 * 1024 * 1024:  # 5 MB
                raise ValidationError(
                    'Размер изображения не должен превышать 5 МБ. '
                    f'Текущий размер: {image.size / (1024 * 1024):.1f} МБ'
                )

            # Проверка формата файла
            valid_formats = ['image/jpeg', 'image/png', 'image/jpg']
            if image.content_type not in valid_formats:
                raise ValidationError(
                    'Поддерживаются только форматы JPEG и PNG. '
                    f'Загруженный формат: {image.content_type}'
                )
        return image
