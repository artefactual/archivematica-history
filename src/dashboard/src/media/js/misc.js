$(document).ready(
  function()
    {
      $('.preview-help-text')

        // Preview text
        .children('.preview')
          .show()
          .children('a')
            .click(function(event)
              {
                event.preventDefault();
                $(this).closest('.preview').hide();
                $(this).closest('.preview-help-text').children('.content').show();
              })
          .end()
        .end()

        // Content
        .children('.content')
          .hide()
          .append(' <a href="#">(collapse)</a>')
          .children('a')
            .click(function(event)
              {
                event.preventDefault();
                $(this).closest('.content').hide();
                $(this).closest('.preview-help-text').children('.preview').show();
              });
    });
