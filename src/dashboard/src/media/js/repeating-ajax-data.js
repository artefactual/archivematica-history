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
var RepeatingDataRecordView = Backbone.View.extend({
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
    this.el = $('<div class="repeating-ajax-data-row"></div>');

    for(field in this.definition) {
      var type = this.definition[field].type
        , label = this.definition[field].label
        , options = this.definition[field].options;

      if (typeof type == 'undefined') {
        type = 'textarea';
      } else {
        type = type;
      }

      var $container = $('<div></div>')
        , $input = $('<' + type + '></' + type + '>');

      if (type == 'select') {
        for(var value in options) {
          var $option = $('<option>' + options[value] + '</option>');
          $option.attr('value', value);
          $input.append($option);
        }
      }

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
              $input.hide();
              $input.fadeIn();
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
    'type':  'select',
    'options': {
      '': '',
      '1': 'One',
      '2': 'Two'
    },
    'label': 'some text'
  }
}

Type will default to textarea.

*/
var RepeatingDataView = Backbone.View.extend({

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
      var field = new RepeatingDataRecordView(
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
            $input.hide();
            $input.fadeIn(function() {
              self.render();
            });
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
    if (this.parentId != '' && this.parentId != 'None') {
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
                label: self.schema[field].label,
                options: self.schema[field].options
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

            var field = new RepeatingDataRecordView(
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
    }
    return this;
  }
});
