
document.addEventListener('DOMContentLoaded', function() {

  document.querySelector('#login-button').addEventListener('click', (evt) => {
    const loginBtn = evt.target;

    if (loginBtn.innerHTML === 'Log In') {
      loginBtn.innerHTML = 'Log Out';
    } else {
      loginBtn.innerHTML = 'Log In';
    }
  });
});