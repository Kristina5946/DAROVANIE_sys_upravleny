/**
 * Автоподсчёт суммы абонемента при изменении количества занятий.
 * Ручная сумма не перезаписывается, если пользователь её менял.
 */
document.querySelectorAll('.topup-form').forEach((form) => {
    const lessonsInput = form.querySelector('.topup-lessons');
    const amountInput = form.querySelector('.topup-amount');
    const suggestedEl = form.querySelector('.topup-suggested');
    const directionId = form.dataset.directionId;
    const pricePerLesson = parseFloat(form.dataset.pricePerLesson || '0');
    let amountTouched = false;

    if (!lessonsInput || !amountInput || !directionId) return;

    amountInput.addEventListener('input', () => {
        amountTouched = true;
    });

    const calcLocal = () => {
        const lessons = parseInt(lessonsInput.value || '8', 10);
        if (pricePerLesson > 0) {
            const sum = Math.round(pricePerLesson * lessons);
            if (suggestedEl) suggestedEl.textContent = sum;
            if (!amountTouched) amountInput.value = sum;
            return;
        }
        fetchEstimate();
    };

    const fetchEstimate = async () => {
        const lessons = lessonsInput.value || 8;
        try {
            const res = await fetch(
                `/api/estimate-subscription/?direction_id=${directionId}&lessons=${lessons}`,
            );
            if (!res.ok) return;
            const data = await res.json();
            if (suggestedEl) suggestedEl.textContent = data.amount;
            if (!amountTouched) {
                amountInput.value = data.amount;
            }
        } catch (_) {
            /* ignore */
        }
    };

    lessonsInput.addEventListener('input', calcLocal);
    calcLocal();
});
