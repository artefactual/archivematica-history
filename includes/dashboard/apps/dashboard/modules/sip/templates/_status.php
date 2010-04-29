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
    <tr class="odd"><td><div class="statusIcon"><?php echo image_tag($sip->getCurrentStatusLog()->getSipStatus()->getIcon())?></div><?php echo $sip->getCurrentStatusLog()->getSipStatus()->getName() ?></td><td></td><td><?php echo $sip->getCurrentStatusLog()->getOpenedAt() ?></td></tr>
  <?php foreach($sip->getStatusLog() as $log): ?>
    <tr class="<?php echo 0 == $row++ % 2 ? 'even' : 'odd' ?>">
    <td><div class="statusIcon"><?php echo image_tag($log->getSipStatus()->getIcon())?></div><?php echo $log->getSipStatus()?></td><td><?php echo $log->getClosedAt() ?></td><td><?php echo $log->getOpenedAt() ?></td></tr>
  <?php endforeach; ?>
  </tbody>
</table>
