from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.forms import DirectionForm, SearchForm
from core.models import Direction, LessonType
from core.services.subscriptions import get_direction_student_cards


@login_required
def direction_list(request):
    search_form = SearchForm(request.GET or None)
    directions = Direction.objects.annotate(
        students_count=Count('students', distinct=True),
        active_subs_count=Count(
            'subscriptions',
            filter=Q(subscriptions__status='active'),
            distinct=True,
        ),
    ).order_by('name')

    if search_form.is_valid():
        q = search_form.cleaned_data.get('q', '').strip()
        if q:
            directions = directions.filter(
                Q(name__icontains=q) | Q(description__icontains=q),
            )
        lesson_type = search_form.cleaned_data.get('lesson_type')
        if lesson_type:
            directions = directions.filter(lesson_type=lesson_type)

    return render(request, 'pages/directions/list.html', {
        'directions': directions,
        'search_form': search_form,
        'lesson_types': LessonType.choices,
        'page_title': 'Направления',
        'total_count': directions.count(),
    })


@login_required
def direction_detail(request, pk):
    direction = get_object_or_404(
        Direction.objects.annotate(
            students_count=Count('students', distinct=True),
        ),
        pk=pk,
    )
    edit_mode = request.GET.get('edit') == '1'
    student_cards = get_direction_student_cards(direction)

    if request.method == 'POST' and request.POST.get('action') == 'save_direction':
        form = DirectionForm(request.POST, instance=direction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Направление сохранено.')
            return redirect('core:direction_detail', pk=pk)
        messages.error(request, 'Проверьте поля формы.')
    else:
        form = DirectionForm(instance=direction) if edit_mode else None

    return render(request, 'pages/directions/detail.html', {
        'direction': direction,
        'student_cards': student_cards,
        'form': form,
        'edit_mode': edit_mode,
        'page_title': direction.name,
    })


@login_required
def direction_create(request):
    if request.method == 'POST':
        form = DirectionForm(request.POST)
        if form.is_valid():
            direction = form.save()
            messages.success(request, f'Направление «{direction.name}» создано.')
            return redirect('core:direction_detail', pk=direction.pk)
    else:
        form = DirectionForm()

    return render(request, 'pages/directions/form.html', {
        'form': form,
        'page_title': 'Новое направление',
        'is_create': True,
    })


@login_required
@require_POST
def direction_delete(request, pk):
    direction = get_object_or_404(Direction, pk=pk)
    name = direction.name
    direction.delete()
    messages.success(request, f'Направление «{name}» удалено.')
    return redirect('core:direction_list')
