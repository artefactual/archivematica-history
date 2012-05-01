$(document).ready(function() {
  var picker = new DirectoryPickerView({
      el: $('#explorer'),
      levelTemplate: $('#template-dir-level').html(),
      entryTemplate: $('#template-dir-entry').html()
  });
  picker.updateSources(function() {
    var picker = new DirectoryPickerView({
      el: $('#explorer'),
      levelTemplate: $('#template-dir-level').html(),
      entryTemplate: $('#template-dir-entry').html()
    });
    picker.busy();
    $.get('/filesystem/contents/', function(results) {
      picker.structure = results;
      picker.render();
      picker.idle();
    });
  });
});
