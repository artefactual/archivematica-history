function setupAIPBrowser(directory) {
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

  var explorer = new FileExplorer({
    el: $('#explorer'),
    levelTemplate: $('#template-dir-level').html(),
    entryTemplate: $('#template-dir-entry').html()
  });

  explorer.moveHandler = moveHandler;

  explorer.refresh(directory);
}
