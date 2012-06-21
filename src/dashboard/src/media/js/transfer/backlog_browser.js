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
      actionHandlers: [{
        name: 'Start transfer',
        description: 'Start transfer',
        iconHtml: '<img src="/media/images/accept.png" />',
        logic: function(result) {
          arrange.confirm(
            'Add transfer',
            'Are you sure you want to add this as a transfer?',
            function() {
              $.post(
                '/filesystem/copy_from_arrange/',
                {filepath: result.path},
                function(result) {
                  var title = (result.error) ? 'Error' : '';
                  arrange.alert(
                    title,
                    result.message
                  );
                }
              );
            }
          );
        }
      }]
  });

  arrange.moveHandler = moveHandler;

  arrange.refresh(arrangeDirectory);
}
