document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-modal-open]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('data-modal-open');
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

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal:not([hidden])').forEach((modal) => {
                modal.hidden = true;
            });
        }
    });
});
