const form = document.getElementById('signupForm');
const messageDiv = document.getElementById('message');

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');

if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
      username: form.username.value,
      email: form.email.value,
      password: form.password.value,
    };

    
    try {
      const response = await fetch('/accounts/api/signup/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
      });
      console.log(response);

      const result = await response.json();
      console.log(result);
      messageDiv.textContent = result.message || 'Check your email to verify your account.';
      messageDiv.className = response.ok ? 'success' : 'error';
      if (response.ok) form.reset();
    } catch (err) {
      messageDiv.textContent = 'Network error. Try again.';
      messageDiv.className = 'error';
    }
  });
}
