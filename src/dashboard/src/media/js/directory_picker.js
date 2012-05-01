var DirectoryPickerView = FileExplorer.extend({

  initialize: function() {
    this.structure=         {};
    this.options.closeDirsByDefault = true;
    this.options.hideFiles =        true;

    this.render();

    var self;
    this.options.nameClickHandler = function(result) { 
      if (result.type == 'directory') { 
        self.alert('User clicked name of ' + result.type + ' at path ' + result.path); 
      } 
    };

    var self = this;
    this.options.actionHandlers = [ 
      { 
        name: 'Add Source', 
        description: 'Add Source Directory', 
        iconHtml: '<b>Add</b>', 
        logic: function(result) { 
          self.addSource(self, result.path); 
        } 
      } 
    ]; 
  },

  addSource: function(fileExplorer, path) {
    var self = this;
    $.post(
      '/administration/sources/json/',
      {path: path},
      function(response) {
        self.alert(response.message);
        self.updateSources();
      }
    );
  },

  deleteSource: function(id) {
    var self = this;
    if (confirm('Are you sure you want to delete this?')) {
      $.post(
        '/administration/sources/delete/json/' + id + '/',
        {},
        function(response) {
          self.alert(response.message);
          self.updateSources();
        }
      );
    }
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

  alert: function(message, title) {
    title = title || '';
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

  bootstrapConfirm: function(message, logic) {
  }
});
