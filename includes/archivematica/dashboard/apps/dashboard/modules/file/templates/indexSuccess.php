<h1>Files List</h1>

<table>
  <thead>
    <tr>
      <th>Id</th>
      <th>Sip</th>
      <th>Aip</th>
      <th>Identifier</th>
      <th>Title</th>
      <th>Original filename</th>
      <th>Clean filename</th>
      <th>Filepath</th>
      <th>Date</th>
      <th>Checksum</th>
      <th>Checksum type</th>
    </tr>
  </thead>
  <tbody>
    <?php foreach ($files as $file): ?>
    <tr>
      <td><a href="<?php echo url_for('file/show?id='.$file->getId()) ?>"><?php echo $file->getId() ?></a></td>
      <td><?php echo $file->getSipId() ?></td>
      <td><?php echo $file->getAipId() ?></td>
      <td><?php echo $file->getIdentifier() ?></td>
      <td><?php echo $file->getTitle() ?></td>
      <td><?php echo $file->getOriginalFilename() ?></td>
      <td><?php echo $file->getCleanFilename() ?></td>
      <td><?php echo $file->getFilepath() ?></td>
      <td><?php echo $file->getDate() ?></td>
      <td><?php echo $file->getChecksum() ?></td>
      <td><?php echo $file->getChecksumType() ?></td>
    </tr>
    <?php endforeach; ?>
  </tbody>
</table>

  <a href="<?php echo url_for('file/new') ?>">New</a>
