$('#upload-form').on('submit', function (e) {
  e.preventDefault();
  
  var formData = new FormData(this);
  $.ajax({
    url: '/',
    type: 'POST',
    data: formData,
    error: function (error) {
      console.error("Error:", error);
    },
    cache: false,
    contentType: false,
    processData: false
  });
});
