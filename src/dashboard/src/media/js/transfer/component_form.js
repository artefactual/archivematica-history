var TransferComponentFormView = Backbone.View.extend({
  initialize: function() {
    this.directories = [
      '/var/fdfd/fgfghfg/',
      '/usr/df/fgfg/'
    ];
  },

  showSelector: function() {

   // display action selector in modal window
    $('<div class="modal hide" id="transfer-component-select-modal"><div class="modal-header"><button type="button" class="close" id="transfer-component-select-close" data-dismiss="modal">×</button><h3>Select a directory</h3></div><div class="modal-body" id="transfer-component-select-body"><div id="explorer" class="backbone-file-explorer"></div></div><div class="modal-footer"><a href="#" class="btn" data-dismiss="modal" id="transfer-component-select-cancel">Cancel</a></div></div>')
    .modal({show: true});

    // make it destroy rather than hide modal
    $('#transfer-component-select-close').click(function() {
      $('#transfer-component-select-modal').remove();
    });

    // add directory selector
    createDirectoryPicker('/home/demo/backbone-file-explorer');
  },

  render: function() {
    for(var index in this.directories)
    {
      var dirRow = $('<div></div>').html(this.directories[index]);
      $(this.el).append(dirRow);
    }

    var addButton = $('<div class="btn">Add</div>')
      , self = this;

    addButton.click(function() {
      // add modal containing directory selector
      // selecting makes modal disappear, adds directory, and re-renders
      console.log('clicked');
      self.showSelector();
    });

    $(this.el).append(addButton);
  }
});
