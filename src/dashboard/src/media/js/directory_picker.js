var DirectoryPickerView = FileExplorer.extend({

  initialize: function() {
    this.structure=         {};
    this.options.closeDirsByDefault = true;
    this.options.hideFiles =        true;

    this.render();

    this.options.nameClickHandler = function(result) { 
      if (result.type == 'directory') { 
        alert('User clicked name of ' + result.type + ' at path ' + result.path); 
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
        alert(response.message);
        self.updateSources();
      }
    );
  },

  updateSources: function(cb) {
    $.get('/administration/sources/json/', function(results) {
      tableTemplate = _.template($('#template-source-directory-table').html());
      rowTemplate   = _.template($('#template-source-directory-table-row').html());

      $('#directories').empty();
      rowHtml = '';

      for(var index in results['directories']) {
        rowHtml += rowTemplate({
          id:   results.directories[index].id,
          path: results.directories[index].path
        });
      }

      $('#directories').append(tableTemplate({rows: rowHtml}));

      if (cb != undefined) {
        cb();
      }
    });
  }
});
