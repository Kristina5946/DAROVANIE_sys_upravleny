/**
 * Автоподсчёт суммы и даты окончания абонемента.
 */
document.querySelectorAll('.topup-form').forEach((form) => {
    const lessonsInput = form.querySelector('.topup-lessons')
        || form.querySelector('[name="total_lessons"]');
    const amountInput = form.querySelector('.topup-amount')
        || form.querySelector('[name="amount"]');
    const suggestedEl = form.querySelector('.topup-suggested');
    const endSuggestedEl = form.querySelector('.topup-end-suggested')
        || form.querySelector('.edit-end-suggested');
    const endDateInput = form.querySelector('.topup-end-date')
        || form.querySelector('.edit-end-date');
    const paymentDateInput = form.querySelector('[name="payment_date"]');
    const startDateInput = form.querySelector('[name="start_date"]');
    const fromMonthStartInput = form.querySelector('[name="from_month_start"]');
    const fromNextMonthInput = form.querySelector('[name="from_next_month"]');
    const autoEndDateInput = form.querySelector('.edit-auto-end-date');
    const carriedInput = form.querySelector('[name="carried_lessons"]');
    const directionId = form.dataset.directionId;
    const studentId = form.dataset.studentId;
    const pricePerLesson = parseFloat(form.dataset.pricePerLesson || '0');
    let amountTouched = false;
    let endDateTouched = false;

    if (!lessonsInput || !directionId) return;

    if (amountInput) {
        amountInput.addEventListener('input', () => {
            amountTouched = true;
        });
    }

    if (endDateInput) {
        endDateInput.addEventListener('input', () => {
            endDateTouched = true;
        });
    }

    const formatDateRu = (iso) => {
        if (!iso) return '—';
        const [y, m, d] = iso.split('-');
        return `${d}.${m}.${y}`;
    };

    const getLessonsCount = () => {
        const base = parseInt(lessonsInput.value || '1', 10);
        const carried = carriedInput ? parseInt(carriedInput.value || '0', 10) : 0;
        return Math.max(1, base + (Number.isNaN(carried) ? 0 : carried));
    };

    const getFromMonthStart = () => {
        if (fromNextMonthInput && fromNextMonthInput.checked) return false;
        if (fromMonthStartInput) return fromMonthStartInput.checked;
        return false;
    };

    const getFromNextMonth = () => fromNextMonthInput ? fromNextMonthInput.checked : false;

    const getPaymentDate = () => {
        if (startDateInput && startDateInput.value) return startDateInput.value;
        if (paymentDateInput && paymentDateInput.value) return paymentDateInput.value;
        return new Date().toISOString().slice(0, 10);
    };

    const fetchEstimate = async () => {
        const lessons = getLessonsCount();
        const params = new URLSearchParams({
            direction_id: directionId,
            lessons: String(lessons),
            from_month_start: getFromMonthStart() ? '1' : '0',
            from_next_month: getFromNextMonth() ? '1' : '0',
            payment_date: getPaymentDate(),
        });
        if (studentId) params.set('student_id', studentId);
        try {
            const res = await fetch(`/api/estimate-subscription/?${params.toString()}`);
            if (!res.ok) return;
            const data = await res.json();
            if (suggestedEl && data.amount) suggestedEl.textContent = data.amount;
            if (amountInput && data.amount && !amountTouched) {
                amountInput.value = data.amount;
            }
            if (endSuggestedEl && data.end_date) {
                endSuggestedEl.textContent = formatDateRu(data.end_date);
            }
            if (endDateInput && data.end_date) {
                const useAuto = autoEndDateInput
                    ? autoEndDateInput.checked
                    : !endDateTouched && !endDateInput.value;
                if (useAuto) {
                    endDateInput.value = data.end_date;
                }
            }
        } catch (_) {
            /* ignore */
        }
    };

    const calcLocal = () => {
        const lessons = getLessonsCount();
        if (pricePerLesson > 0 && amountInput) {
            const sum = Math.round(pricePerLesson * lessons);
            if (suggestedEl) suggestedEl.textContent = sum;
            if (!amountTouched) amountInput.value = sum;
        }
        fetchEstimate();
    };

    lessonsInput.addEventListener('input', calcLocal);
    if (carriedInput) carriedInput.addEventListener('input', calcLocal);
    if (paymentDateInput) paymentDateInput.addEventListener('change', calcLocal);
    if (startDateInput) startDateInput.addEventListener('change', calcLocal);
    if (fromMonthStartInput) fromMonthStartInput.addEventListener('change', calcLocal);
    if (fromNextMonthInput) {
        fromNextMonthInput.addEventListener('change', () => {
            if (fromNextMonthInput.checked && fromMonthStartInput) {
                fromMonthStartInput.checked = false;
            }
            calcLocal();
        });
    }
    if (autoEndDateInput) {
        autoEndDateInput.addEventListener('change', () => {
            if (autoEndDateInput.checked) {
                endDateTouched = false;
            }
            calcLocal();
        });
    }

    calcLocal();
});
