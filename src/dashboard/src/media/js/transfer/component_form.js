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
    $('#transfer-component-select-close, #transfer-component-select-cancel')
      .click(function() {
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

  startTransfer: function(transfer) {
    var path
      , copied = 0;

    $('.transfer-component-activity-indicator').show();
    // get path to temp directory in which to copy individual transfer
    // components
    $.ajax({
      url: '/filesystem/get_temp_directory/',
      type: 'GET',
      cache: false,
      success: function(results) {

        var tempDir = results.tempDir;

        // copy each transfer component to the temp directory
        for (var index in transfer.sourcePaths) {
          path = transfer.sourcePaths[index];
          $.ajax({
            url: '/filesystem/copy_transfer_component/',
            type: 'POST',
            async: false,
            cache: false,
            data: {
              name:        transfer.name,
              path:        path,
              destination: tempDir
            },
            success: function(results) {
              copied++;
            }
          });
        }
        // move from temp directory to appropriate watchdir
        var url = '/filesystem/ransfer/';
        $.ajax({
          url: url,
          type: 'POST',
          async: false,
          cache: false,
          data: {
            filepath: tempDir + '/' + transfer.name,
            type:     transfer.type
          },
          success: function(results) {
            archivematicaNotifications.add({
              message: 'Transfer copy complete.'
            });
            $('#path_container').html('');
            $('.transfer-component-activity-indicator').hide();
          }
        });
        // report progress
      }
    });
  },

  render: function() {
    var $pathAreaEl = $('<div></div>')
       , $pathContainerEl = $('<div id="path_container"></div>');

    this.pathContainerEl = $pathContainerEl;

    // add button to add paths via a pop-up selector
    var $buttonContainer = $('<div></div>')
      , $addButton = $('<span id="path_add_button" class="btn">Browse</span>')
      , $sourceDirSelect = $('<select id="path_source_select"></select>')
      , $startTransferButton = $('<span id="start_transfer_button" class="btn success">Start transfer</span>')
      , self = this;

    $buttonContainer
      .append($addButton)
      .append($sourceDirSelect)
      .append($startTransferButton);

    $pathAreaEl.append($buttonContainer);

    // add path container to parent container
    $pathAreaEl.append($pathContainerEl);

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
      self.showSelector($sourceDirSelect.children('option:selected').text());
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
          'accessionNumber': $('#transfer-accession-number').val(),
          'sourcePaths':     self.addedPaths()
        };
        self.startTransfer(transferData);
      }
    });
  }
});
