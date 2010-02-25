<table>
  <tbody>
    <tr>
      <th>Id:</th>
      <td><?php echo $sip->getId() ?></td>
    </tr>
    <tr>
      <th>Identifier:</th>
      <td><?php echo $sip->getIdentifier() ?></td>
    </tr>
    <tr>
      <th>Title:</th>
      <td><?php echo $sip->getTitle() ?></td>
    </tr>
    <tr>
      <th>Date received:</th>
      <td><?php echo $sip->getDateReceived() ?></td>
    </tr>
    <tr>
      <th>Provenance:</th>
      <td><?php echo $sip->getProvenance() ?></td>
    </tr>
    <tr>
      <th>Part of:</th>
      <td><?php echo $sip->getPartOf() ?></td>
    </tr>
    <tr>
      <th>Checksum:</th>
      <td><?php echo $sip->getChecksum() ?></td>
    </tr>
    <tr>
      <th>Checksum type:</th>
      <td><?php echo $sip->getChecksumType() ?></td>
    </tr>
  </tbody>
</table>

<hr />

<a href="<?php echo url_for('sip/edit?id='.$sip->getId()) ?>">Edit</a>
&nbsp;
<a href="<?php echo url_for('sip/index') ?>">List</a>
