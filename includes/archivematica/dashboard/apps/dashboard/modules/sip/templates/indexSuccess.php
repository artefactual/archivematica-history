<h1>Sips List</h1>

<table>
  <thead>
    <tr>
      <th>Id</th>
      <th>Sip status</th>
      <th>Identifier</th>
      <th>Title</th>
      <th>Date submitted</th>
      <th>Provenance</th>
      <th>Part of</th>
      <th>Checksum</th>
      <th>Checksum type</th>
    </tr>
  </thead>
  <tbody>
    <?php foreach ($sips as $sip): ?>
    <tr>
      <td><a href="<?php echo url_for('sip/show?id='.$sip->getId()) ?>"><?php echo $sip->getId() ?></a></td>
      <td><?php echo $sip->getSipStatusId() ?></td>
      <td><?php echo $sip->getIdentifier() ?></td>
      <td><?php echo $sip->getTitle() ?></td>
      <td><?php echo $sip->getDateSubmitted() ?></td>
      <td><?php echo $sip->getProvenance() ?></td>
      <td><?php echo $sip->getPartOf() ?></td>
      <td><?php echo $sip->getChecksum() ?></td>
      <td><?php echo $sip->getChecksumType() ?></td>
    </tr>
    <?php endforeach; ?>
  </tbody>
</table>

  <a href="<?php echo url_for('sip/new') ?>">New</a>
