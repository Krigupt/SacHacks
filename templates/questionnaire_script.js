// Function to load and populate options from the hobbies.csv file
function loadOptionsFromCSV() {
    // Replace 'hobbies.csv' with the correct path to your CSV file
    fetch('hobbies.csv')
        .then(response => response.text())
        .then(data => {
            const options = data.split('\n'); // Split CSV into lines

            const select = document.getElementById('multiSelect');
            for (const option of options) {
                const trimmedOption = option.trim();
                if (trimmedOption !== '') {
                    const optionElement = document.createElement('option');
                    optionElement.textContent = trimmedOption;
                    select.appendChild(optionElement);
                }
            }
        })
        .catch(error => {
            console.error('Error loading CSV:', error);
        });
}

// Call the function to load options when the page loads
window.addEventListener('load', loadOptionsFromCSV);
