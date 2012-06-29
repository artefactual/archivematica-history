var DirectorySelectorView = fileBrowser.FileExplorer.extend({

  initialize: function() {
    this.structure = {};
    this.options.closeDirsByDefault = true;
    this.options.hideFiles = true;

    this.render();

    this.options.actionHandlers = []
  }
});

function createDirectoryPicker(baseDirectory, modalCssId, targetCssId) {
  $('#page_instructions').hide();

  var url = '/filesystem/contents/?path=' + encodeURIComponent(baseDirectory)

  var selector = new DirectorySelectorView({
    el: $('#explorer'),
    levelTemplate: $('#template-dir-level').html(),
    entryTemplate: $('#template-dir-entry').html()
  });

  selector.options.actionHandlers.push({
    name: 'Select',
    description: 'Select',
    iconHtml: '<img src="/media/images/accept.png" />',
    logic: function(result) {
      var $transferPathEl = $('<div class="transferPath"></div>');
      $transferPathEl.html(result.path);
      $('#' + targetCssId).append($transferPathEl);
      $('#' + modalCssId).remove();
      /*
      $('#explorer').hide();

      $('#page_instructions')
        .text('Copying to backlog... ')
        .append('<img src="/media/images/ajax-loader.gif"/>');

      $.post(
        '/filesystem/ransfer/',
        {filepath: result.path},
        function(result) {
          if (result.error == undefined) {
            window.location = '/transfer/';
          } else {
            $('#explorer').show();
            $('#page_instructions').text('');
            alert(result.message);
          }
        }
      )
      */
    }
  });

  selector.busy();

  $.get(url, function(results) {
    selector.structure = results;
    selector.render();

    selector.idle();
    $('#page_instructions').fadeIn();
  });
}
