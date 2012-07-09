function setupBacklogBrowser(originalsDirectory, arrangeDirectory) {
  function moveHandler(move) {
    // don't allow dragging stuff from originals directory?
    if (move.self.id != 'originals') {
      if (move.allowed) {
        move.self.busy();

        $.post(
          '/filesystem/copy_to_arrange/',
          {
            filepath: move.droppedPath,
            destination: move.containerPath
          },
          function(result) {
            if (result.error == undefined) {
              arrange.refresh(arrangeDirectory);
            } else {
              alert(result.message);
              move.self.idle();
            }
          }
        );
      } else {
        alert("You can't move a directory into its subdirectory.");
      }
    } else {
      alert("You can't copy into the originals directory.");
    }
  }

  var originals = new FileExplorer({
    el: $('#originals'),
    levelTemplate: $('#template-dir-level').html(),
    entryTemplate: $('#template-dir-entry').html()
  });

  originals.moveHandler = moveHandler;

  originals.refresh(originalsDirectory);

  var arrange = new FileExplorer({
    el: $('#arrange'),
    levelTemplate: $('#template-dir-level').html(),
    entryTemplate: $('#template-dir-entry').html(),
    entryClickHandler: function(event) {
      var explorer = event.data.self.explorer
        , explorerId = explorer.id
        , entryEl = this
        , entryId = $(this).attr('id');

      // take note of selected entry
      explorer.selectedEntryId = $(entryEl).attr('id');

      // remove highlighting of existing entries
      $('#' + explorerId).find('.backbone-file-explorer-entry').css('border', '');

      // highlight selected entry
      $(entryEl).css('border', '1px solid blue');
    }
  });

  arrange.options.actionHandlers = [];
  arrange.moveHandler = moveHandler;
  arrange.refresh(arrangeDirectory);

  return arrange;
}
