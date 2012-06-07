var DirectorySelectorView = fileBrowser.FileExplorer.extend({

  initialize: function() {
    this.structure = {};
    this.options.closeDirsByDefault = true;
    this.options.hideFiles = true;

    this.render();

    this.options.actionHandlers = []
  }
});

function createDirectoryPicker(baseDirectory) {
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
    iconHtml: '<b>Select</b>',
    logic: function(result) {
      $.post(
        '/filesystem/copy_to_originals/',
        {filepath: result.path},
        function(result) {
          console.log(result);
          alert(result.message);
          if (result.error == undefined) {
            window.location = '/transfer/browser/';
          }
        }
      )
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
