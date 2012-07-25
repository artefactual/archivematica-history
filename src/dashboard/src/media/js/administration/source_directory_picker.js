$(document).ready(function() {
  $('#directories').hide();
  $('#source_page_instructions').hide();

  var ajaxChildDataUrl = '/filesystem/children/'
    , picker = new DirectoryPickerView({
      el:               $('#explorer'),
      levelTemplate:    $('#template-dir-level').html(),
      entryTemplate:    $('#template-dir-entry').html(),
      ajaxChildDataUrl: ajaxChildDataUrl
  });
  picker.updateSources(function() {
    var picker = new DirectoryPickerView({
      el: $('#explorer'),
      levelTemplate: $('#template-dir-level').html(),
      entryTemplate: $('#template-dir-entry').html(),
      ajaxChildDataUrl: ajaxChildDataUrl
    });
    picker.busy();
    picker.structure = {
      'name': 'home',
      'parent': '',
      'children': []
    };
    picker.render();
    picker.idle();
    $('#directories').slideDown();
    $('#source_page_instructions').fadeIn();
  });
});
