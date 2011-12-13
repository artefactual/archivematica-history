function revealSelectedBasis() {
  var basis = $('#id_rightsbasis').val()
    , formsets = {
      'Copyright': 'copyright_formset',
      'Statute':   'statute_formset',
      'License':   'license_formset',
      'Policy':    false,
      'Donor':     false
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

$(document).ready(function() {
  $('#id_rightsbasis').change(revealSelectedBasis);
  revealSelectedBasis();
});
