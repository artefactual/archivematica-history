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
      var $transferPathRowEl = $('<div></div>')
        , $transferPathEl = $('<span class="transferPath"></span>')
        , $transferPathDeleteRl = $('<span style="float:right"><img src="/media/images/delete.png" /></span>');

      $transferPathDeleteRl.click(function() {
        $transferPathRowEl.remove();
      });

      $transferPathEl.html('/' + result.path);
      $transferPathRowEl.append($transferPathEl);
      $transferPathRowEl.append($transferPathDeleteRl);
      $('#' + targetCssId).append($transferPathRowEl);
      $('#' + modalCssId).remove();

      // tiger stripe transfer paths
      $('.transferPath').each(function() {
        $(this).parent().css('background-color', '');
      });
      $('.transferPath:odd').each(function() {
        $(this).parent().css('background-color', '#eee');
      });

      /*
      $('#explorer').hide();

      $.post(
        '/filesystem/ransfer/',
        {filepath: result.path},
        function(result) {
          if (result.error == undefined) {
            window.location = '/transfer/';
          } else {
            $('#explorer').show();
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
  });
}
