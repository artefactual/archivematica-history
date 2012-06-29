var TransferComponentFormView = Backbone.View.extend({
  initialize: function(options) {
    this.form_layout_template = _.template(options.form_layout_template);
    this.modal_template = options.modal_template;
    this.sourceDirectories = options.sourceDirectories;
  },

  showSelector: function(sourceDir) {

   // display action selector in modal window
    $(this.modal_template).modal({show: true});

    // make it destroy rather than hide modal
    $('#transfer-component-select-close, #transfer-component-select-cancel').click(function() {
      $('#transfer-component-select-modal').remove();
    });

    // add directory selector
    createDirectoryPicker(
      sourceDir,
      'transfer-component-select-modal',
      'path_container'
    );
  },

  addedPaths: function() {
    var paths = [];
    $('.transfer_path').each(function() {
      paths.push($(this).text());
    });
    return paths;
  },

  render: function() {
    var $pathAreaEl = $('<div></div>')
       , $pathContainerEl = $('<div id="path_container"></div>');

    this.pathContainerEl = $pathContainerEl;

    // add path container to parent container
    $pathAreaEl.append($pathContainerEl);

    // add button to add paths via a pop-up selector
    var $buttonContainer = $('<div></div>')
      , $addButton = $('<span id="path_add_button" class="btn">Add</span>')
      , $sourceDirSelect = $('<select id="path_source_select"></select>')
      , $startTransferButton = $('<span id="start_transfer_button" class="btn">Start Transfer</span>')
      , self = this;

    $buttonContainer
      .append($addButton)
      .append($sourceDirSelect)
      .append($startTransferButton);

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

    // make start transfer button clickable
    $('#start_transfer_button').click(function() {
      var transferName = $('#transfer-name').val();

      if (!transferName)
      {
        alert('Please enter a transfer name');
      } else {
        var transferData = {
          'name':            transferName,
          'type':            $('#transfer-type').val(),
          'accessionNumber': '',
          'sourcePaths':     self.addedPaths()
        };
        console.log(transferData);
      }
    });
  }
});
