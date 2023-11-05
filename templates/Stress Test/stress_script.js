// Initialize an object to store user responses
const userResponses = {};

// Get all the option elements
const options = document.querySelectorAll('.option');

// Function to handle option clicks
function handleOptionClick(event) {
    // Get the selected option's data-value and its parent question's ID
    const selectedValue = event.target.getAttribute('data-value');
    const questionId = event.target.parentElement.id;

    // Store the selected value in the userResponses object
    userResponses[questionId] = parseInt(selectedValue);

    // Remove the 'selected' class from all options in the same question
    const questionOptions = event.target.parentElement.querySelectorAll('.option');
    questionOptions.forEach(option => option.classList.remove('selected'));

    // Add the 'selected' class to the clicked option
    event.target.classList.add('selected');
}

// Add click event listeners to all option elements
options.forEach(option => {
    option.addEventListener('click', handleOptionClick);
});

// Function to calculate the final result when needed
function calculateFinalResult() {
    let totalScore = 0;
    for (const question in userResponses) {
        totalScore += userResponses[question];
    }

    // Redirect to the results page with the total score as a query parameter
    window.location.href = `results.html?totalScore=${totalScore}`;
}

// Example: If you have a "Submit" button with an id of "submit-button"
const submitButton = document.getElementById('submit-button');
if (submitButton) {
    submitButton.addEventListener('click', calculateFinalResult);
}
