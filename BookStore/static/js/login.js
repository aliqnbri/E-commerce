// Get the form data
const formData = new FormData(document.getElementById('loginForm'));

// Create an object to store the form data
const userData = {};
formData.forEach((value, key) => {
    userData[key] = value;
});

// Make a POST request to the API endpoint
fetch('https://your-api-endpoint.com/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
})
.then(response => {
    if (response.ok) {
        // Extract and store the JWT token from the response
        const token = response.headers.get('Authorization');
        
        // Store the JWT token in a cookie
        document.cookie = `jwt=${token}`;

        return response.json();
    }
    throw new Error('Network response was not ok.');
})
.then(data => {
    console.log(data);
})
.catch(error => {
    console.error('There was a problem with your fetch operation:', error);
});