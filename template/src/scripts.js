// only enable submit button if valid email address is entered
// add listener to input email to enable the submit button if valid email address is entered
function validateEmail(email) {
  var re = /\S+@\S+\.\S+/;
  return re.test(email);
}

document.getElementById('email').addEventListener('input', function() {
  var email = document.getElementById('email').value;
  var submitButton = document.getElementById('submit');
  submitButton.disabled = !validateEmail(email);
});

document.getElementById('submit').addEventListener('click', function() {
    // post details to backend
    var email = document.getElementById('email').value;
    var page_identifier = document.getElementById('page_identifier').value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/email", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({email: email, site: page_identifier}));
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
            if (xhr.status === 201) {
            // replace form with success message
            var form = document.getElementById('form');
            form.style.display = 'none';
            var success = document.getElementById('success');
            success.style.display = 'block';
      } else {
        // error alert
        alert('There was an error, please try again');
      }
        }
    };

});
