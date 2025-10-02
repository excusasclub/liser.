function copyCodeTailwind(el) {
    const code = el.textContent.trim();
    if (!code) return;

    navigator.clipboard.writeText(code).then(() => {
        const original = el.textContent;
        el.textContent = "✅ Copiado";
        el.classList.remove('text-[#315C95]');
        el.classList.add('bg-green-100', 'text-green-800', 'px-2', 'rounded');

        setTimeout(() => {
            el.textContent = original;
            el.classList.remove('bg-green-100', 'text-green-800', 'px-2', 'rounded');
            el.classList.add('text-[#315C95]');
        }, 1000);
    }).catch(err => {
        console.error('No se pudo copiar: ', err);
    });
}
