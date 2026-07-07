from django import forms
from django.utils import timezone

from core.models import Direction, LessonType, Parent, Payment, PaymentType, Student, Teacher, ScheduleSlot, SingleLesson, ScheduleException, Classroom, WeekDay, SingleLessonType, LessonExceptionType
from core.widgets import searchable_select


class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Поиск',
        widget=forms.TextInput(attrs={
            'placeholder': 'Имя, телефон родителя…',
            'class': 'search-input',
            'autocomplete': 'off',
        }),
    )
    direction = forms.ModelChoiceField(
        queryset=Direction.objects.all(),
        required=False,
        label='Направление',
        empty_label='Все направления',
        widget=searchable_select('filter-select', 'Все направления'),
    )
    gender = forms.ChoiceField(
        required=False,
        label='Пол',
        choices=[('', 'Любой'), ('boy', 'Мальчик'), ('girl', 'Девочка')],
        widget=searchable_select('filter-select', 'Любой'),
    )
    lesson_type = forms.ChoiceField(
        required=False,
        label='Формат',
        choices=[('', 'Все'), *LessonType.choices],
        widget=searchable_select('filter-select', 'Все форматы'),
    )


class StudentForm(forms.ModelForm):
    parent_name = forms.CharField(label='ФИО родителя', max_length=255, required=False)
    parent_phone = forms.CharField(label='Телефон', max_length=50, required=False)
    parent_email = forms.EmailField(label='Email родителя', required=False)

    class Meta:
        model = Student
        fields = [
            'name', 'date_of_birth', 'gender', 'notes', 'registration_date', 'directions',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'field-input'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'field-input'}),
            'gender': forms.Select(attrs={'class': 'field-input'}),
            'notes': forms.Textarea(attrs={'class': 'field-input', 'rows': 3}),
            'registration_date': forms.DateInput(attrs={'type': 'date', 'class': 'field-input'}),
            'directions': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['directions'].queryset = Direction.objects.order_by('name')
        for name in ('date_of_birth', 'registration_date'):
            if name not in self.fields:
                continue
            self.fields[name].localize = False
            self.fields[name].widget = forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'field-input'},
            )
            self.fields[name].input_formats = ['%Y-%m-%d', '%d.%m.%Y']
        # В карточке ученика registration_date не в шаблоне — убираем при редактировании
        if self.instance.pk:
            self.fields.pop('registration_date', None)
        if self.instance.pk and self.instance.parent:
            self.fields['parent_name'].initial = self.instance.parent.name
            self.fields['parent_phone'].initial = self.instance.parent.phone
            self.fields['parent_email'].initial = self.instance.parent.email

    def clean_date_of_birth(self):
        value = self.cleaned_data.get('date_of_birth')
        if (
            value is None
            and self.instance.pk
            and self.instance.date_of_birth
            and not str(self.data.get('date_of_birth', '')).strip()
        ):
            return self.instance.date_of_birth
        return value

    def save(self, commit=True):
        student = super().save(commit=False)
        parent_name = self.cleaned_data.get('parent_name', '').strip()
        parent_phone = self.cleaned_data.get('parent_phone', '').strip()
        parent_email = self.cleaned_data.get('parent_email', '').strip()

        if parent_name or parent_phone:
            if student.parent_id:
                parent = student.parent
                parent.name = parent_name or parent.name
                parent.phone = parent_phone
                parent.email = parent_email
                parent.save()
            else:
                parent = Parent.objects.create(
                    name=parent_name or f'Родитель {student.name}',
                    phone=parent_phone,
                    email=parent_email,
                )
                student.parent = parent

        if commit:
            student.save()
            self.save_m2m()
        return student


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_date', 'amount', 'direction', 'payment_type', 'notes']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'field-input field-input--sm'}),
            'amount': forms.NumberInput(attrs={'class': 'field-input field-input--sm', 'step': '0.01', 'placeholder': '0'}),
            'direction': searchable_select('field-input field-input--sm', 'Направление не выбрано'),
            'payment_type': searchable_select('field-input field-input--sm', 'Тип оплаты'),
            'notes': forms.TextInput(attrs={'class': 'field-input field-input--sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].localize = False
        self.fields['direction'].queryset = Direction.objects.order_by('name')
        self.fields['direction'].empty_label = 'Направление не выбрано'

    def clean_payment_type(self):
        value = self.cleaned_data.get('payment_type')
        return value or PaymentType.SUBSCRIPTION


class PaymentQuickAddForm(forms.ModelForm):
    payment_type = forms.ChoiceField(
        choices=[('', 'Тип оплаты'), *PaymentType.choices],
        required=False,
        label='Тип оплаты',
        widget=searchable_select('field-input field-input--sm', 'Тип оплаты'),
    )

    class Meta:
        model = Payment
        fields = ['student', 'payment_date', 'amount', 'direction', 'payment_type', 'notes']
        widgets = {
            'student': searchable_select('field-input field-input--sm', 'Ученик не выбран'),
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'field-input field-input--sm'}),
            'amount': forms.NumberInput(attrs={'class': 'field-input field-input--sm', 'step': '0.01', 'placeholder': '0'}),
            'direction': searchable_select('field-input field-input--sm', 'Направление не выбрано'),
            'notes': forms.TextInput(attrs={'class': 'field-input field-input--sm', 'placeholder': 'Примечание'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].localize = False
        self.fields['direction'].queryset = Direction.objects.order_by('name')
        self.fields['direction'].empty_label = 'Направление не выбрано'
        self.fields['student'].queryset = Student.objects.order_by('name')
        self.fields['student'].empty_label = 'Ученик не выбран'
        if not self.is_bound:
            self.fields['payment_date'].initial = timezone.localdate()
            self.fields['payment_type'].initial = ''

    def clean_payment_type(self):
        value = self.cleaned_data.get('payment_type')
        return value or PaymentType.SUBSCRIPTION


class PaymentFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Поиск',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ученик, родитель, примечание…',
            'class': 'search-input',
            'autocomplete': 'off',
        }),
    )
    date_from = forms.DateField(
        required=False,
        label='С',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'filter-select'}),
    )
    date_to = forms.DateField(
        required=False,
        label='По',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'filter-select'}),
    )
    direction = forms.ModelChoiceField(
        queryset=Direction.objects.all(),
        required=False,
        label='Направление',
        empty_label='Все направления',
        widget=searchable_select('filter-select', 'Все направления'),
    )
    payment_type = forms.ChoiceField(
        required=False,
        label='Тип оплаты',
        choices=[('', 'Все типы'), *PaymentType.choices],
        widget=searchable_select('filter-select', 'Все типы'),
    )


class SubscriptionTopUpForm(forms.Form):
    direction = forms.ModelChoiceField(
        queryset=Direction.objects.none(),
        widget=forms.HiddenInput(),
    )
    lessons_count = forms.IntegerField(
        min_value=1,
        max_value=50,
        initial=8,
        label='Количество занятий',
        widget=forms.NumberInput(attrs={'class': 'field-input', 'id': 'id_lessons_count'}),
    )
    amount = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        label='Сумма оплаты, ₽',
        widget=forms.NumberInput(attrs={
            'class': 'field-input',
            'step': '0.01',
            'id': 'id_amount',
        }),
    )
    payment_date = forms.DateField(
        label='Дата оплаты',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'field-input'}),
    )
    notes = forms.CharField(
        required=False,
        label='Примечание',
        widget=forms.TextInput(attrs={'class': 'field-input', 'placeholder': 'Абонемент'}),
    )

    def __init__(self, student, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student = student
        self.fields['direction'].queryset = student.directions.all()
        self.fields['amount'].localize = False
        if not self.is_bound:
            self.fields['payment_date'].initial = timezone.localdate()


class DirectionForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = [
            'name', 'description', 'lesson_type',
            'price_per_lesson', 'single_lesson_cost', 'subscription_cost',
            'min_age', 'max_age', 'gender',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'field-input'}),
            'description': forms.Textarea(attrs={'class': 'field-input', 'rows': 2}),
            'lesson_type': forms.Select(attrs={'class': 'field-input'}),
            'price_per_lesson': forms.NumberInput(attrs={'class': 'field-input', 'step': '50'}),
            'single_lesson_cost': forms.NumberInput(attrs={'class': 'field-input', 'step': '50'}),
            'subscription_cost': forms.NumberInput(attrs={'class': 'field-input', 'step': '100'}),
            'min_age': forms.NumberInput(attrs={'class': 'field-input'}),
            'max_age': forms.NumberInput(attrs={'class': 'field-input'}),
            'gender': forms.Select(attrs={'class': 'field-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('price_per_lesson', 'single_lesson_cost', 'subscription_cost'):
            self.fields[name].localize = False


class DateRangeFilterForm(forms.Form):
    date_from = forms.DateField(
        required=False,
        label='С',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'filter-select'}),
    )
    date_to = forms.DateField(
        required=False,
        label='По',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'filter-select'}),
    )
    direction = forms.ModelChoiceField(
        queryset=Direction.objects.all(),
        required=False,
        label='Направление',
        empty_label='Все направления',
        widget=searchable_select('filter-select', 'Все направления'),
    )


class TeacherFilterForm(forms.Form):
    date_from = forms.DateField(
        required=False,
        label='С',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'filter-select'}),
    )
    date_to = forms.DateField(
        required=False,
        label='По',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'filter-select'}),
    )
    directions = forms.ModelMultipleChoiceField(
        queryset=Direction.objects.none(),
        required=False,
        label='Направления',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'teacher-filter-directions'}),
    )

    def __init__(self, *args, teacher_directions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if teacher_directions is not None:
            self.fields['directions'].queryset = teacher_directions


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'phone', 'email', 'hire_date', 'notes', 'directions']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'field-input'}),
            'phone': forms.TextInput(attrs={'class': 'field-input'}),
            'email': forms.EmailInput(attrs={'class': 'field-input'}),
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class': 'field-input'}),
            'notes': forms.Textarea(attrs={'class': 'field-input', 'rows': 2}),
            'directions': forms.CheckboxSelectMultiple(),
        }


class ScheduleSlotForm(forms.ModelForm):
    class Meta:
        model = ScheduleSlot
        fields = [
            'direction', 'student', 'day_of_week', 'start_time', 'end_time',
            'teacher', 'classroom', 'is_archived',
        ]
        widgets = {
            'direction': searchable_select('field-input', 'Направление не выбрано', id='id_slot_direction'),
            'student': searchable_select(
                'field-input', 'Ученик не выбран', id='id_slot_student',
                **{'data-empty-text': 'На этом направлении пока нет учеников'},
            ),
            'day_of_week': searchable_select('field-input', 'День не выбран'),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'field-input'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'field-input'}),
            'teacher': searchable_select('field-input', 'Преподаватель не назначен'),
            'classroom': searchable_select('field-input', 'Кабинет не указан'),
            'is_archived': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].required = False
        self.fields['student'].empty_label = 'Ученик не выбран'
        self.fields['teacher'].required = False
        self.fields['teacher'].empty_label = 'Преподаватель не назначен'
        self.fields['classroom'].required = False
        self.fields['classroom'].empty_label = 'Кабинет не указан'
        self.fields['direction'].empty_label = 'Направление не выбрано'
        self.fields['direction'].queryset = Direction.objects.order_by('name')
        direction_id = None
        if self.instance and self.instance.pk and self.instance.direction_id:
            direction_id = self.instance.direction_id
        elif self.data.get('direction'):
            direction_id = self.data.get('direction')
        if direction_id:
            self.fields['student'].queryset = Student.objects.filter(
                directions__pk=direction_id,
            ).order_by('name').distinct()
        else:
            self.fields['student'].queryset = Student.objects.none()

    def clean(self):
        cleaned = super().clean()
        direction = cleaned.get('direction')
        student = cleaned.get('student')
        if direction and direction.lesson_type == LessonType.INDIVIDUAL:
            if not student:
                self.add_error('student', 'Для индивидуального занятия выберите ученика.')
            elif not student.directions.filter(pk=direction.pk).exists():
                self.add_error('student', 'Ученик не записан на это направление.')
        elif direction and direction.lesson_type == LessonType.GROUP:
            cleaned['student'] = None
        return cleaned


class SingleLessonForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all().order_by('name'),
        label='Ученик',
        empty_label='Ученик не выбран',
        widget=searchable_select('field-input', 'Ученик не выбран'),
    )
    direction = forms.ModelChoiceField(
        queryset=Direction.objects.all().order_by('name'),
        label='Направление',
        empty_label='Направление не выбрано',
        widget=searchable_select('field-input', 'Направление не выбрано'),
    )
    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all().order_by('name'),
        label='Преподаватель',
        empty_label='Преподаватель не назначен',
        widget=searchable_select('field-input', 'Преподаватель не назначен'),
    )
    lesson_date = forms.DateField(
        label='Дата',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'field-input'}),
    )
    start_time = forms.TimeField(
        label='Начало',
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'field-input'}),
    )
    end_time = forms.TimeField(
        label='Конец',
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'field-input'}),
    )
    lesson_type = forms.ChoiceField(
        choices=[('', 'Тип не выбран'), *SingleLessonType.choices],
        label='Тип',
        widget=searchable_select('field-input', 'Тип не выбран'),
    )
    create_payment = forms.BooleanField(
        required=False,
        initial=True,
        label='Создать оплату',
    )
    payment_amount = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        label='Сумма, ₽',
        widget=forms.NumberInput(attrs={'class': 'field-input', 'step': '50'}),
    )
    notes = forms.CharField(
        required=False,
        label='Примечание',
        widget=forms.TextInput(attrs={'class': 'field-input'}),
    )


class ScheduleExceptionForm(forms.Form):
    lesson_date = forms.DateField(
        label='Дата',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'field-input'}),
    )
    schedule_slot = forms.ModelChoiceField(
        queryset=ScheduleSlot.objects.filter(is_archived=False),
        label='Занятие',
        empty_label='Занятие не выбрано',
        widget=searchable_select('field-input', 'Занятие не выбрано'),
    )
    exception_type = forms.ChoiceField(
        choices=LessonExceptionType.choices,
        label='Тип',
        widget=searchable_select('field-input', 'Тип исключения'),
    )
    substitute_teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all().order_by('name'),
        required=False,
        label='Заменяющий преподаватель',
        empty_label='Преподаватель не назначен',
        widget=searchable_select('field-input', 'Преподаватель не назначен'),
    )
    notes = forms.CharField(
        required=False,
        label='Примечание',
        widget=forms.TextInput(attrs={'class': 'field-input'}),
    )
