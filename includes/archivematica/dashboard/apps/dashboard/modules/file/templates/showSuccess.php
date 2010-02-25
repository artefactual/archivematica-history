<table>
  <tbody>
    <tr>
      <th>Id:</th>
      <td><?php echo $file->getId() ?></td>
    </tr>
    <tr>
      <th>Sip:</th>
      <td><?php echo $file->getSipId() ?></td>
    </tr>
    <tr>
      <th>Aip:</th>
      <td><?php echo $file->getAipId() ?></td>
    </tr>
    <tr>
      <th>Identifier:</th>
      <td><?php echo $file->getIdentifier() ?></td>
    </tr>
    <tr>
      <th>Title:</th>
      <td><?php echo $file->getTitle() ?></td>
    </tr>
    <tr>
      <th>Original filename:</th>
      <td><?php echo $file->getOriginalFilename() ?></td>
    </tr>
    <tr>
      <th>Clean filename:</th>
      <td><?php echo $file->getCleanFilename() ?></td>
    </tr>
    <tr>
      <th>Filepath:</th>
      <td><?php echo $file->getFilepath() ?></td>
    </tr>
    <tr>
      <th>Date:</th>
      <td><?php echo $file->getDate() ?></td>
    </tr>
    <tr>
      <th>Checksum:</th>
      <td><?php echo $file->getChecksum() ?></td>
    </tr>
    <tr>
      <th>Checksum type:</th>
      <td><?php echo $file->getChecksumType() ?></td>
    </tr>
  </tbody>
</table>

<hr />

<a href="<?php echo url_for('file/edit?id='.$file->getId()) ?>">Edit</a>
&nbsp;
<a href="<?php echo url_for('file/index') ?>">List</a>
