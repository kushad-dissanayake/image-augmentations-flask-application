function submitForm(link) {
    const form = document.createElement('form');
    form.method = 'GET';
    form.action = link;
    document.body.appendChild(form);
    form.submit();
}