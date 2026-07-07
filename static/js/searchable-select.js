/**
 * Поисковый select: подпись-плейсхолдер, ввод для поиска, сортировка по совпадению.
 */
(function () {
    'use strict';

    const SELECTORS = 'select.searchable-select, select[data-searchable]';
    const LIST_Z_INDEX = '100000';

    function normalize(text) {
        return (text || '').toLowerCase().replace(/\s+/g, ' ').trim();
    }

    function scoreOption(label, query) {
        const t = normalize(label);
        const q = normalize(query);
        if (!q) return 0;
        if (t === q) return 200;
        if (t.startsWith(q)) return 150 - t.length * 0.1;
        const idx = t.indexOf(q);
        if (idx >= 0) return 100 - idx;
        for (const w of t.split(' ')) {
            if (w.startsWith(q)) return 80;
        }
        return -1;
    }

    function getPlaceholder(select) {
        const emptyOption = Array.from(select.options).find((o) => !o.value);
        return select.dataset.placeholder
            || (emptyOption ? emptyOption.text.trim() : '')
            || 'Начните вводить для поиска…';
    }

    function initSearchableSelect(select) {
        if (select.dataset.searchableInit === '1') return;
        select.dataset.searchableInit = '1';

        const wrapper = document.createElement('div');
        wrapper.className = 'searchable-select-wrap';

        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'searchable-select__input';
        input.autocomplete = 'off';
        input.spellcheck = false;

        const list = document.createElement('div');
        list.className = 'searchable-select__list';
        list.hidden = true;
        list.setAttribute('role', 'listbox');

        input.placeholder = getPlaceholder(select);
        if (select.id) {
            input.id = `${select.id}_search`;
            const label = document.querySelector(`label[for="${select.id}"]`);
            if (label) label.setAttribute('for', input.id);
        }

        select.classList.add('searchable-select__native');
        select.parentNode.insertBefore(wrapper, select);
        wrapper.appendChild(input);
        wrapper.appendChild(list);
        wrapper.appendChild(select);

        let listInBody = false;
        let suppressClose = false;

        function syncInputFromSelect() {
            const opt = select.options[select.selectedIndex];
            input.value = opt && opt.value ? opt.text : '';
            input.placeholder = getPlaceholder(select);
        }

        function buildOptions(query) {
            return Array.from(select.options)
                .map((opt) => ({
                    opt,
                    score: !opt.value ? -1 : scoreOption(opt.text, query),
                }))
                .filter(({ opt, score }) => {
                    if (!opt.value) return false;
                    return query.trim() === '' || score >= 0;
                })
                .sort((a, b) => {
                    if (b.score !== a.score) return b.score - a.score;
                    return a.opt.text.localeCompare(b.opt.text, 'ru');
                });
        }

        function positionList() {
            const rect = input.getBoundingClientRect();
            list.style.position = 'fixed';
            list.style.top = `${rect.bottom + 4}px`;
            list.style.left = `${rect.left}px`;
            list.style.width = `${Math.max(rect.width, 180)}px`;
            list.style.zIndex = LIST_Z_INDEX;
        }

        function openList() {
            if (!listInBody) {
                document.body.appendChild(list);
                listInBody = true;
            }
            positionList();
            list.hidden = false;
            wrapper.classList.add('is-open');
        }

        function closeList() {
            list.hidden = true;
            wrapper.classList.remove('is-open');
            if (listInBody) {
                wrapper.appendChild(list);
                listInBody = false;
            }
        }

        function renderList(query) {
            list.innerHTML = '';
            const items = buildOptions(query);
            if (!items.length) {
                const empty = document.createElement('div');
                empty.className = 'searchable-select__empty';
                empty.textContent = query.trim()
                    ? (select.dataset.emptySearchText || 'Ничего не найдено')
                    : (select.dataset.emptyText || 'Нет вариантов для выбора');
                list.appendChild(empty);
                openList();
                return;
            }
            items.slice(0, 30).forEach(({ opt }) => {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'searchable-select__option';
                btn.setAttribute('role', 'option');
                if (select.value === opt.value) btn.classList.add('is-selected');
                btn.textContent = opt.text;
                btn.addEventListener('mousedown', (e) => {
                    e.preventDefault();
                    suppressClose = true;
                    select.value = opt.value;
                    syncInputFromSelect();
                    closeList();
                    select.dispatchEvent(new Event('change', { bubbles: true }));
                });
                list.appendChild(btn);
            });
            openList();
        }

        function onScrollOrResize() {
            if (!list.hidden && listInBody) positionList();
        }

        syncInputFromSelect();

        input.addEventListener('mousedown', () => {
            suppressClose = true;
        });

        input.addEventListener('focus', () => {
            suppressClose = true;
            input.value = '';
            renderList('');
            setTimeout(() => { suppressClose = false; }, 0);
        });

        input.addEventListener('input', () => {
            const match = Array.from(select.options).find(
                (o) => o.value && normalize(o.text) === normalize(input.value),
            );
            if (match) {
                select.value = match.value;
            } else if (!input.value.trim()) {
                select.value = '';
            }
            renderList(input.value);
        });

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeList();
                syncInputFromSelect();
            }
            if (e.key === 'Enter') {
                e.preventDefault();
                const first = list.querySelector('.searchable-select__option');
                if (first) first.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
            }
        });

        input.addEventListener('blur', () => {
            setTimeout(() => {
                if (suppressClose) return;
                closeList();
                syncInputFromSelect();
            }, 150);
        });

        document.addEventListener('mousedown', (e) => {
            if (suppressClose) return;
            if (!wrapper.contains(e.target) && !list.contains(e.target)) {
                closeList();
                syncInputFromSelect();
            }
        });

        window.addEventListener('scroll', onScrollOrResize, true);
        window.addEventListener('resize', onScrollOrResize);
    }

    function initCheckboxFilter(container) {
        if (container.dataset.checkboxFilterInit === '1') return;
        container.dataset.checkboxFilterInit = '1';

        const input = document.createElement('input');
        input.type = 'search';
        input.className = 'checkbox-filter__input';
        input.placeholder = 'Найти направление…';
        input.autocomplete = 'off';
        container.parentNode.insertBefore(input, container);

        input.addEventListener('input', () => {
            const q = normalize(input.value);
            const labels = Array.from(container.querySelectorAll('label'));
            labels.forEach((label) => {
                const text = normalize(label.textContent);
                const score = !q ? 0 : scoreOption(text, q);
                const show = !q || score >= 0;
                label.classList.toggle('checkbox-filter__hidden', !show);
                label.dataset.filterScore = show ? String(score) : '-1';
            });
            if (q) {
                labels
                    .filter((l) => l.dataset.filterScore !== '-1')
                    .sort((a, b) => {
                        const diff = Number(b.dataset.filterScore) - Number(a.dataset.filterScore);
                        return diff !== 0 ? diff : a.textContent.localeCompare(b.textContent, 'ru');
                    })
                    .forEach((l) => container.appendChild(l));
            }
        });
    }

    function initAll(root) {
        root.querySelectorAll(SELECTORS).forEach(initSearchableSelect);
        root.querySelectorAll('[data-checkbox-filter]').forEach(initCheckboxFilter);
    }

    function syncSearchableSelect(select) {
        if (!select) return;
        const wrap = select.closest('.searchable-select-wrap');
        if (!wrap) return;
        const input = wrap.querySelector('.searchable-select__input');
        if (!input) return;
        const opt = select.options[select.selectedIndex];
        input.value = opt && opt.value ? opt.text : '';
        input.placeholder = getPlaceholder(select);
    }

    function syncSearchableForm(form) {
        if (!form) return;
        form.querySelectorAll(SELECTORS).forEach(syncSearchableSelect);
    }

    document.addEventListener('DOMContentLoaded', () => initAll(document));
    window.initSearchableSelects = initAll;
    window.syncSearchableSelect = syncSearchableSelect;
    window.syncSearchableForm = syncSearchableForm;
})();
