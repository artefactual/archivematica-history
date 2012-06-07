var DirectoryPickerView = fileBrowser.FileExplorer.extend({

  initialize: function() {
    this.structure = {};
    this.options.closeDirsByDefault = true;
    this.options.hideFiles =        true;

    this.render();

    var self;
    this.options.nameClickHandler = function(result) { 
      if (result.type == 'directory') { 
        self.alert(
          'Click',
          'User clicked name of ' + result.type + ' at path ' + result.path
        ); 
      } 
    };

    var self = this;
    this.options.actionHandlers = [ 
      { 
        name: 'Browse', 
        description: 'Browse', 
        iconHtml: '<b>Browse</b>', 
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
      } 
    ]; 
  }
});

function createDirectoryPicker(baseDirectory) {
  var url = '/filesystem/contents/?path=' + encodeURIComponent(baseDirectory)
  $('#source_page_instructions').hide();
  var picker = new DirectoryPickerView({
    el: $('#explorer'),
    levelTemplate: $('#template-dir-level').html(),
    entryTemplate: $('#template-dir-entry').html()
  });

  picker.busy();

  $.get(url, function(results) {
    picker.structure = results;
    picker.render();
    picker.idle();
    $('#source_page_instructions').fadeIn();
  });
}
