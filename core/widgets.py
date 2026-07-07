from django import forms


class SearchableSelect(forms.Select):
    """Select с поиском по вводу (инициализируется в JS)."""

    def __init__(self, attrs=None, choices=()):
        merged = {'data-searchable': 'true', 'autocomplete': 'off'}
        if attrs:
            merged.update(attrs)
        css = merged.get('class', '')
        if 'searchable-select' not in css:
            merged['class'] = f'{css} searchable-select'.strip()
        super().__init__(attrs=merged, choices=choices)


def searchable_select(css_class='', placeholder=None, **extra):
    """Удобный конструктор SearchableSelect с подписью-плейсхолдером."""
    attrs = {}
    if css_class:
        attrs['class'] = css_class
    if placeholder:
        attrs['data-placeholder'] = placeholder
    attrs.update(extra)
    return SearchableSelect(attrs=attrs)
