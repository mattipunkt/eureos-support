document.getElementById('addNewTicket').addEventListener('submit', function(event) {
    event.preventDefault();
    var ticketData = new FormData(this);
    var token = '{{ csrf_token }}';

    fetch('/pushData/', {method: 'POST', headers: {'X-CSRFToken': token}, body: ticketData, })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network-Response was not okay.');
        }
        return response.json();

    })
    .then(data => {
        console.log('Daten konnten geschickt werden!', data);
    })
    .catch(error => {
        close.error('Fehler in der Übertragung.', data);
    });
});
