document.getElementById('compare-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const playerA = document.getElementById('playerA').value;
    const playerB = document.getElementById('playerB').value;
    const week = document.getElementById('week').value;

    fetch('/compare', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ playerA: playerA, playerB: playerB, week: week }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('result').innerHTML = `<p>${data.error}</p>`;
        } else {
            document.getElementById('result').innerHTML = `<p>${data.result}</p>`;
        }
    })
    .catch((error) => {
        document.getElementById('result').innerHTML = `<p>Error: ${error}</p>`;
    });
});
