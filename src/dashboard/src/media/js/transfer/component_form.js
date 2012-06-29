var TransferComponentFormView = Backbone.View.extend({
  initialize: function(options) {
    this.form_layout_template = _.template(options.form_layout_template);
    this.sourceDirectories = options.sourceDirectories;
    this.directories = [];
  },

  showSelector: function(sourceDir) {

   // display action selector in modal window
    $('<div class="modal hide" id="transfer-component-select-modal"><div class="modal-header"><button type="button" class="close" id="transfer-component-select-close" data-dismiss="modal">×</button><h3>Select a directory</h3></div><div class="modal-body" id="transfer-component-select-body"><div id="explorer" class="backbone-file-explorer"></div></div><div class="modal-footer"><a href="#" class="btn" data-dismiss="modal" id="transfer-component-select-cancel">Cancel</a></div></div>')
    .modal({show: true});

    // make it destroy rather than hide modal
    $('#transfer-component-select-close').click(function() {
      $('#transfer-component-select-modal').remove();
    });

    // add directory selector
    createDirectoryPicker(
      sourceDir,
      'transfer-component-select-modal',
      'path_container'
    );
  },

  render: function() {
    var $pathAreaEl = $('<div></div>')
       , $pathContainerEl = $('<div id="path_container"></div>');

    this.pathContainerEl = $pathContainerEl;

    // populate path container with any existing directories
    for(var index in this.directories)
    {
      var dirRow = $('<div></div>').html(this.directories[index]);
      $pathContainerEl.append(dirRow);
    }

    // add path container to parent container
    $pathAreaEl.append($pathContainerEl);

    // add button to add paths via a pop-up selector
    var $buttonContainer = $('<div></div>')
      , $addButton = $('<span id="path_add_button" class="btn">Add</span>')
      , $sourceDirSelect = $('<select id="path_source_select"></select>')
      , self = this;

    $buttonContainer.append($addButton);
    $buttonContainer.append($sourceDirSelect);
    $pathAreaEl.append($buttonContainer);

    // populate select with source directory values
    $.each(this.sourceDirectories, function(id, path) {   
      $sourceDirSelect
        .append($("<option></option>")
        .attr("value", id)
        .text(path)); 
    });

    // populate view's DOM element with template output
    var context = {
      transfer_paths: $pathAreaEl.html()
    };
    $(this.el).html(this.form_layout_template(context));

    // make add button clickable
    $('#path_add_button').click(function() {
      // add modal containing directory selector
      // selecting makes modal disappear, adds directory, and re-renders
      self.showSelector($sourceDirSelect.text());
    });
  }
});
