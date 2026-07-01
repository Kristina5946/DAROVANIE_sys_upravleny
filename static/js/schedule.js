(function () {
    const config = window.SCHEDULE_CONFIG || {};
    const directionTypes = config.directionTypes || {};
    const studentsUrl = config.studentsUrl || '';

    function getCsrf() {
        const el = document.querySelector('[name=csrfmiddlewaretoken]');
        return el ? el.value : '';
    }

    function getModal() {
        return document.getElementById('modal-slot');
    }

    function getSlotForm() {
        return document.getElementById('slot-form');
    }

    function isIndividualDirection(directionId) {
        return directionTypes[directionId] === 'individual';
    }

    async function loadStudents(directionId, selectedId) {
        const wrap = document.getElementById('slot-student-wrap');
        const select = document.getElementById('id_slot_student');
        if (!wrap || !select) return;

        if (!directionId || !isIndividualDirection(directionId)) {
            wrap.hidden = true;
            select.value = '';
            select.innerHTML = '<option value="">— выберите ученика —</option>';
            return;
        }

        wrap.hidden = false;
        select.innerHTML = '<option value="">Загрузка…</option>';

        try {
            const resp = await fetch(`${studentsUrl}?direction=${encodeURIComponent(directionId)}`);
            if (!resp.ok) {
                select.innerHTML = '<option value="">Ошибка загрузки</option>';
                return;
            }
            const data = await resp.json();
            select.innerHTML = '<option value="">— выберите ученика —</option>';
            (data.students || []).forEach((s) => {
                const opt = document.createElement('option');
                opt.value = s.id;
                opt.textContent = s.name;
                if (selectedId && s.id === selectedId) opt.selected = true;
                select.appendChild(opt);
            });
            if (selectedId) select.value = selectedId;
        } catch (e) {
            select.innerHTML = '<option value="">Ошибка загрузки</option>';
        }
    }

    function openSlotModal(card, title) {
        const modal = getModal();
        const form = getSlotForm();
        if (!modal || !form || !card) return;

        document.getElementById('slot_id').value = card.getAttribute('data-slot-id') || '';
        document.getElementById('modal-slot-title').textContent = title || 'Слот расписания';

        const setVal = (name, val) => {
            const field = form.querySelector(`[name=${name}]`);
            if (!field) return;
            if (val === null || val === undefined || val === '') {
                field.value = '';
            } else {
                field.value = val;
            }
        };

        const directionId = card.getAttribute('data-direction') || '';
        setVal('direction', directionId);
        setVal('day_of_week', card.getAttribute('data-day'));
        setVal('start_time', card.getAttribute('data-start'));
        setVal('end_time', card.getAttribute('data-end'));
        setVal('teacher', card.getAttribute('data-teacher'));
        setVal('classroom', card.getAttribute('data-classroom'));

        loadStudents(directionId, card.getAttribute('data-student') || '');
        modal.hidden = false;
    }

    function resetSlotModal(day) {
        const modal = getModal();
        const form = getSlotForm();
        if (!modal || !form) return;
        form.reset();
        document.getElementById('slot_id').value = '';
        document.getElementById('modal-slot-title').textContent = 'Новое занятие';
        if (day !== undefined && day !== null) {
            const daySelect = form.querySelector('[name=day_of_week]');
            if (daySelect) daySelect.value = day;
        }
        const directionSelect = form.querySelector('[name=direction]');
        const directionId = directionSelect ? directionSelect.value : '';
        loadStudents(directionId, '');
        modal.hidden = false;
    }

    // Модалки
    document.querySelectorAll('[data-modal-open]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('data-modal-open');
            if (id === 'modal-slot' && btn.hasAttribute('data-new-slot')) {
                resetSlotModal('');
                return;
            }
            const modal = document.getElementById(id);
            if (modal) modal.hidden = false;
        });
    });

    document.querySelectorAll('[data-modal-close]').forEach((el) => {
        el.addEventListener('click', () => {
            const modal = el.closest('.modal');
            if (modal) modal.hidden = true;
        });
    });

    document.querySelectorAll('[data-add-slot-day]').forEach((btn) => {
        btn.addEventListener('click', () => {
            resetSlotModal(btn.getAttribute('data-add-slot-day'));
        });
    });

    document.querySelectorAll('[data-edit-slot]').forEach((btn) => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const card = btn.closest('.week-slot') || btn.closest('.table-slot-row');
            openSlotModal(card, 'Редактировать занятие');
        });
    });

    const directionSelect = document.getElementById('id_slot_direction');
    if (directionSelect) {
        directionSelect.addEventListener('change', () => {
            loadStudents(directionSelect.value, '');
        });
        if (directionSelect.value) {
            loadStudents(directionSelect.value, document.getElementById('id_slot_student')?.value || '');
        }
    }

    // SortableJS — перетаскивание между днями
    const grid = document.getElementById('week-grid');
    if (grid && typeof Sortable !== 'undefined') {
        const reorderUrl = grid.getAttribute('data-reorder-url');
        const lists = grid.querySelectorAll('[data-day-list]');

        lists.forEach((listEl) => {
            Sortable.create(listEl, {
                group: 'schedule-week',
                animation: 150,
                ghostClass: 'sortable-ghost',
                draggable: '.week-slot',
                onEnd: () => persistOrder(reorderUrl),
            });
        });
    }

    function persistOrder(url) {
        if (!url) return;
        const items = [];
        document.querySelectorAll('[data-day-list]').forEach((listEl) => {
            const day = parseInt(listEl.getAttribute('data-day-list'), 10);
            listEl.querySelectorAll('.week-slot').forEach((slot, index) => {
                items.push({
                    id: slot.getAttribute('data-slot-id'),
                    day: day,
                    sort_order: index,
                });
            });
        });

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrf(),
            },
            body: JSON.stringify({ items }),
        }).catch(() => {});
    }
})();
