function setStatus(message, state) {
  const statusDiv = document.querySelector("#status-div");
  if (statusDiv) {
      statusDiv.innerText = message;
      switch (state) {
          case 'running':
              statusDiv.classList.remove('alert-secondary', 'alert-danger');
              statusDiv.classList.add('alert-success');
              break;
          case 'error':
              statusDiv.classList.remove('alert-secondary', 'alert-success');
              statusDiv.classList.add('alert-danger');
              break;
          default:
              statusDiv.classList.remove('alert-success', 'alert-danger');
              statusDiv.classList.add('alert-secondary');
      }
  }
}

$('#upload-form').on('submit', function (e) {
  e.preventDefault();

  setStatus('Uploading...', 'running');

  var formData = new FormData(this);
  $.ajax({
      url: '/',
      type: 'POST',
      data: formData,
      success: function() {
          setStatus('Upload complete.', 'waiting');
      },
      error: function (error) {
          setStatus('Error during upload.', 'error');
          console.error("Error:", error);
      },
      cache: false,
      contentType: false,
      processData: false
  });
});
