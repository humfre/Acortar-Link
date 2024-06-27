document.getElementById('shortenForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const url = document.getElementById('url').value.trim();
    const customId = document.getElementById('custom_id').value.trim();

    fetch('/shorten', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url, custom_id: customId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('result').className = 'alert alert-danger';
            document.getElementById('result').textContent = data.error;
        } else {
            document.getElementById('result').className = 'alert alert-success';
            document.getElementById('result').textContent = `URL acortada: ${data.short_url}`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').className = 'alert alert-danger';
        document.getElementById('result').textContent = 'Ocurrió un error al acortar la URL.';
    });
});
