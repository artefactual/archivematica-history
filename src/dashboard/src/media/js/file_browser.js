var FileExplorer = fileBrowser.FileExplorer.extend({

  initialize: function() {
    this.structure=         {};
    this.options.closeDirsByDefault = true;

    this.render();
    this.initDragAndDrag();

    var self = this;
    this.options.nameClickHandler = function(result) { 
      if (result.type == 'directory') { 
        self.alert(
          'Click',
          'User clicked name of ' + result.type + ' at path ' + result.path
        ); 
      } 
    };

    this.options.actionHandlers = [ 
      { 
        name: 'Delete', 
        description: 'Delete file or directory', 
        iconHtml: "<img src='/media/images/delete.png' />", 
        logic: function(result) { 
          self.deleteEntry(result.path, result.type); 
        } 
      } 
    ]; 
  },

  deleteEntry: function(path, type) {
    var self = this;
    $.post(
      '/filesystem/delete/',
      {filepath: path},
      function(response) {
        self.alert(
          'Delete',
          response.message
        );
        self.refresh();
      }
    );
  },

  refresh: function(path) {
    $(this.el).empty();
    this.initialize();
    this.busy();

    if (path != undefined)
    {
      this.path = path;
    }

    var baseUrl = '/filesystem/contents/';
    url = (this.path != undefined)
      ? baseUrl + '?path=' + encodeURIComponent(this.path)
      : baseUrl;

    var self = this;
    $.get(url, function(results) {
      self.structure = results;
      self.render();
      self.idle();
      //$('#directories').slideDown();
      //$('#source_page_instructions').fadeIn();
    });
  },

  moveHandler: function(move) {
    if (move.allowed) {
      move.self.busy();
      $('#message').text(
        'Dropped ID ' + move.droppedPath + ' onto ' + move.containerPath
      );
      setTimeout(function() {
        move.self.idle();
        $('#message').text('');
      }, 2000);
    } else {
      alert("You can't move a directory into its subdirectory.");
    }
  },

  addSource: function(fileExplorer, path) {
    var self = this;
    $.post(
      '/administration/sources/json/',
      {path: path},
      function(response) {
        self.alert(
          'Add source directory',
          response.message
        );
        self.updateSources();
      }
    );
  },

  deleteSource: function(id) {
    var self = this;
    this.confirm(
      'Delete source directory',
      'Are you sure you want to delete this?',
      function() {
        $.post(
          '/administration/sources/delete/json/' + id + '/',
          {},
          function(response) {
            self.alert(
              'Delete source directory',
              response.message
            );
            self.updateSources();
          }
        );
      }
    );
  },

  updateSources: function(cb) {
    var self = this;
    $.get('/administration/sources/json/', function(results) {
      tableTemplate = _.template($('#template-source-directory-table').html());
      rowTemplate   = _.template($('#template-source-directory-table-row').html());

      $('#directories').empty();
      $('#directories').off('click');

      if (results['directories'].length) {
        var rowHtml = '';

        for(var index in results['directories']) {
          rowHtml += rowTemplate({
            id:   results.directories[index].id,
            path: results.directories[index].path
          });
        }

        $('#directories').append(tableTemplate({rows: rowHtml}));

        $('#directories').on('click', 'a', function() {
          var directoryId = $(this).attr('id').replace('directory_', '');
          self.deleteSource(directoryId);
        });
      }

      if (cb != undefined) {
        cb();
      }
    });
  },

  alert: function(title, message) {
    $('<div class="task-dialog">' + message + '</div>')
      .dialog({
        title: title,
        width: 200,
        height: 200,
        modal: true,
        buttons: [
          {
            text: 'Okay',
            click: function() {
              $(this).dialog('close');
            }
          }
        ]
      });
  },

  confirm: function(title, message, logic) {
    $('<div class="task-dialog">' + message + '</div>')
      .dialog({
        title: title,
        width: 200,
        height: 200,
        modal: true,
        buttons: [
          {
            text: 'Yes',
            click: function() {
              $(this).dialog('close');
              logic();
            }
          },
          {
            text: 'Cancel',
            click: function() {
              $(this).dialog('close');
            }
          }
        ]
      });
  }
});
