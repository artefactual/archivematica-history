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

<h2>Status log</h2>
<table>
  <tbody>
  <thead>
    <tr>
      <th><?php echo __('SIP status')?></th>
      <th><?php echo __('Closed at') ?></th>
      <th><?php echo __('Opened at') ?></th>
    </tr>
  </thead>
    <tr class="odd"><td><?php echo $sip->getCurrentStatusLog()->getSipStatus()->getName() ?></td><td></td><td><?php echo $sip->getCurrentStatusLog()->getOpenedAt() ?></td></tr>
  <?php foreach($sip->getStatusLog() as $log): ?>
    <tr class="<?php echo 0 == $row++ % 2 ? 'even' : 'odd' ?>">
    <td><?php echo $log->getSipStatus()?></td><td><?php echo $log->getClosedAt() ?></td><td><?php echo $log->getOpenedAt() ?></td></tr>
  <?php endforeach; ?>
  </tbody>
</table>

<a href="<?php echo url_for('sip/edit?id='.$sip->getId()) ?>">Edit</a>
&nbsp;
<a href="<?php echo url_for('sip/index') ?>">List</a>
