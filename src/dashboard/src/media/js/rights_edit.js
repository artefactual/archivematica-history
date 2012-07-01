function setUpRepeatingRightsGrantedNotesRecords(parentId) {
  var schema = {
    'rightsgrantednote': {},
  };
  setUpRepeatingField('rightsfields_', parentId, 'Rights Note', schema, '/formdata/rightsnote/' + parentId + '/');
}

function setUpRepeatingCopyrightNotesRecords(parentId) {
  var schema = {
    'copyrightnote': {},
  };
  setUpRepeatingField('copyrightnotes_', parentId, 'Copyright Note', schema, '/formdata/copyrightnote/' + parentId + '/');
}

function setUpRepeatingLicenseNotesRecords(parentId) {
  var schema = {
    'licensenote': {},
  };
  setUpRepeatingField('licensenotes_', parentId, 'License Note', schema, '/formdata/licensenote/' + parentId + '/');
}

function setUpRepeatingCopyrightDocumentationIdentifierRecords(parentId) {
  var schema = {
    'copyrightdocumentationidentifiertype': {
      'label': 'Type',
      'type': 'input'
    },
    'copyrightdocumentationidentifiervalue': {
      'label': 'Value',
      'type': 'input'
    },
    'copyrightdocumentationidentifierrole': {
      'label': 'Role',
      'type': 'input'
    }
  };
  setUpRepeatingField('copyrightdocidfields_', parentId, 'Copyright Documentation Identifier', schema, '/formdata/copyrightdocumentationidentifier/' + parentId + '/');
}

function setUpRepeatingStatuteDocumentationIdentifierRecords(parentId) {
  var schema = {
    'statutedocumentationidentifiertype': {
      'label': 'Type',
      'type': 'input'
    },
    'statutedocumentationidentifiervalue': {
      'label': 'Value',
      'type': 'input'
    },
    'statutedocumentationidentifierrole': {
      'label': 'Role',
      'type': 'input'
    }
  };
  setUpRepeatingField('statutedocidfields_', parentId, 'Statute Documentation Identifier', schema, '/formdata/statutedocumentationidentifier/' + parentId + '/');
}

function setUpRepeatingLicenseDocumentationIdentifierRecords(parentId) {
  var schema = {
    'licensedocumentationidentifiertype': {
      'label': 'Type',
      'type': 'input'
    },
    'licensedocumentationidentifiervalue': {
      'label': 'Value',
      'type': 'input'
    },
    'licensedocumentationidentifierrole': {
      'label': 'Role',
      'type': 'input'
    }
  };
  setUpRepeatingField('licensedocidfields_', parentId, 'License Documentation Identifier', schema, '/formdata/licensedocumentationidentifier/' + parentId + '/');
}

function setUpRepeatingOtherRightsDocumentationIdentifierRecords(parentId) {
  var schema = {
    'otherrightsdocumentationidentifiertype': {
      'label': 'Type',
      'type': 'input'
    },
    'otherrightsdocumentationidentifiervalue': {
      'label': 'Value',
      'type': 'input'
    },
    'otherrightsdocumentationidentifierrole': {
      'label': 'Role',
      'type': 'input'
    }
  };
  setUpRepeatingField('otherrightsdocidfields_', parentId, 'Other Rights Documentation Identifier', schema, '/formdata/otherrightsdocumentationidentifier/' + parentId + '/');
}

function setUpRepeatingOtherRightsNotesRecords(parentId) {
  var schema = {
    'otherrightsnote': {},
  };
  setUpRepeatingField('otherrightsnotes_', parentId, 'Other Rights Note', schema, '/formdata/otherrightsnote/' + parentId + '/');
}

// repeating child field to a formset bound to existing data
function setUpRepeatingField(idPrefix, parentId, description, schema, url) {
  var rights = new RepeatingDataView({
    el: $('#' + idPrefix + parentId),
    description: description,
    parentId: parentId,
    schema: schema,
    url: url
  });
  rights.render();
}

// logic to show appropriate subform
function revealSelectedBasis() {
  var basis = $('#id_rightsbasis').val()
    , formsets = {
      'Copyright': 'copyright_formset',
      'Statute':   'statute_formset',
      'License':   'license_formset',
      'Policy':    false,
      'Donor':     false,
      'Other':     'other_formset'
  }

  // hide all formsets except basis
  for (var key in formsets) {
    if (key != basis && formsets[key]) {
      $('#' + formsets[key]).hide();
    }
  }

  // if basis has a formset, show it
  if (formsets[basis]) {
    $('#' + formsets[basis]).show();
  }
}

// setup
$(document).ready(function() {

  $.extend($.inputmask.defaults.definitions, {
    'y': {
      'validator': '[012]\\d\\d\\d',
      'cardinality': 4,
      'prevalidator': [
        { 'validator': '[012]', 'cardinality': 1 }
      ]
    }
  });

  $('input[name*="date"]').inputmask('y/m/d');

  // active formset changer
  $('#id_rightsbasis').change(revealSelectedBasis);
  revealSelectedBasis();

  if ($('#id_rightsholder').length > 0) {
    // lookup rightsholder
    $.get('lookup/rightsholder/' + $('#id_rightsholder').val(), function(data) {
      $('#id_rightsholder').val(data);
    });

    // attach autocomplete
    $("#id_rightsholder").autocomplete({  

      // define callback to format results  
      source: function(req, add){  
 
        // pass request to server  
        $.getJSON("autocomplete/rightsholders", {'text': req.term}, function(data) {  
 
          // create array for response objects  
          var suggestions = [];  
  
          // process response  
          $.each(data, function(i, val){  
            suggestions.push(val);  
          });  

          // pass array to callback  
          add(suggestions);  
        });
      }
    });
  }
});
