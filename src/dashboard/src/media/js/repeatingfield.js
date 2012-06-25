/*

Field definition example:

{
  'someFieldName': {
    'value': 'someValue',
    'type':  'input',
    'label': 'some text'
  }
}

Type will default to textarea.

*/
var RepeatingRecordRecordView = Backbone.View.extend({
  initialize: function(id, definition, url) {
    this.id = id;
    this.definition = definition;
    this.url = url;
  },

  getValues: function() {
    var values = {};
    $(this.el).children().children().each(function() {
      values[$(this).attr('name')] = $(this).val();
    });
    return values;
  },

  render: function() {
    this.el = $('<div></div>');

    for(field in this.definition) {
      var type = this.definition[field].type
        , label = this.definition[field].label;

      if (typeof type == 'undefined') {
        type = 'textarea';
      }

      var $container = $('<div></div>')
        , $input = $('<' + type + '></' + type + '>');

      $input.attr('name', field);
      $input.val(this.definition[field].value);

      if (typeof label != 'undefined') {
        this.el.append('<b>' + label + '</b><br/>');
      }

      if (this.id > 0) {
        var self = this;
        $input.change(function() {
          var data = self.getValues();

          data.id = self.id;

          $.ajax({
            url: self.url,
            type: 'POST',
            data: data,
            success: function(result) {
            }
          });
        });
      }

      $container.append($input);
      this.el.append($container);
    }

    return this;
  }
});

/*

Field schema example:

{
  'someFieldName': {
    'type':  'input',
    'label': 'some text'
  }
}

Type will default to textarea.

*/
var RepeatingRecordView = Backbone.View.extend({

  initialize: function() {
    this.items = [];

    if (this.options.schema) {
      this.schema = this.options.schema;
    }

    if (this.options.description) {
      this.description = this.options.description;
    }

    if (this.options.parentId) {
      this.parentId = this.options.parentId;
    }

    if (this.options.url) {
      this.url = this.options.url;
    }

    this.waitingForInput = false;
  },

  newLinkEl: function() {
    var $linkEl = $('<div class="btn">New ' + this.description + '</div>')
      , self = this;

    $linkEl.click(function() {
      $(this).attr('disabled', 'true');
      if (!self.waitingForInput) {
      self.waitingForInput = true;
      var field = new RepeatingRecordRecordView(
          0,
          self.schema
        )
        , fieldEl = field.render().el;

      var $input = $(fieldEl)
        , $div = $('<div/>');

      $div.append($input);
      $(self.el).append($div);
      $input.on('change', function() {
        $.ajax({
          url: self.url,
          type: 'POST',
          data: field.getValues(),
          success: function(result) {
            $(self).attr('disabled', 'false');
            self.waitingForInput = false;
            self.render();
          }
        });
      });

      }
    });

    return $linkEl;
  },

  appendDelHandlerToRecord: function(fieldEl, id) {
    var $delHandle = $('<span>Delete</span>')
      , self = this;

    $(fieldEl).append($delHandle);

    $delHandle.click(function() {
      var deleteConfirm = 'Are you sure?';
      if (confirm(deleteConfirm)) {
        $.ajax({
          url: self.url + '/' + id,
          type: 'DELETE',
          data: {'id': id},
          success: function(result) {
            self.render();
          }
        });
      }
    });
  },

  render: function() {
    var self = this;
    $.ajax({
      url: self.url,
      type: 'GET',
      success: function(result) {
        $(self.el)
          .empty()
          .append(self.newLinkEl());

        // cycle through each result
        for(var index in result.results) {
          // use schema as basis of definition
          var newDef = {}
          for(var field in self.schema) {
            newDef[field] = {
              type: self.schema[field].type,
              label: self.schema[field].label
            };
          }

          // get single result
          var fieldData = result.results[index];

          // populate definition clone with result values
          for (var field in fieldData.values) {
            if (typeof newDef[field] != 'undefined') {
              newDef[field]['value'] = fieldData.values[field];
            }
          }

          var field = new RepeatingRecordRecordView(
                fieldData.id,
                newDef,
                self.url
              )
            , fieldEl = field.render().el;

          self.appendDelHandlerToRecord(fieldEl, fieldData.id);

          $(self.el).append(fieldEl);
        }
      }
    });
    return this;
  }
});
