$(document).ready(function() {
  var body = $('body')
  var background_image = body.data('background-image');
  if (!!background_image && !body.css('background-image')) {
    body.css('background-image', "url("+background_image+")");
    body.css('background-size', 'cover')
  }

  function submitInplace(e) {
    e.preventDefault();
    var self = this;
    var form = new FormData(this);
    $.ajax({
      type: "POST",
      enctype: "multipart/form-data",
      url: self.action,
      data: form,
      processData: false,
      contentType: false,
      cache: false,
      timeout: 10000,
      success: function(data, textStatus, xhr) {
        location.reload();
      },
      error: function(xhr) {
        switch(xhr.status) {
          case 422:
            var form = $(xhr.responseText);
            form.submit(submitInplace);
            $(self).replaceWith(form);
            break;
          default:
            // TODO: Error handling.
        }
      }
    });
  }

  $(".submit-inplace").submit(submitInplace);
});
