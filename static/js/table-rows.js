document.querySelectorAll('tr[data-href]').forEach((row) => {
    row.addEventListener('click', (e) => {
        if (e.target.closest('a, button, input, select, label')) return;
        window.location = row.dataset.href;
    });
});
