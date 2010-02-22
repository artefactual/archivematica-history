<div class="toolbar">
  <ul>
    <li><?php echo link_to(image_tag('folder-new.png'), array('module' => 'sip', 'action' => 'new'), array('alt' => __('new SIP'))) ?></li>
    <li><?php echo link_to(image_tag('document-print.png'), array('module' => 'report', 'action' => 'index'), array('alt' => __('print report'))) ?></li>
    <li><?php echo link_to(image_tag('system-search.png'), array('module' => 'search', 'action' => 'index'), array('alt' => __('search'))) ?></li>
</div>

<table>
  <thead>
    <tr>
      <th><?php echo __('Status')?></th>
      <th><?php echo __('Identifier') ?></th>
      <th><?php echo __('Title') ?></th>
      <th><?php echo __('Date submitted') ?></th>
      <th><?php echo __('Provenance') ?></th>
    </tr>
  </thead>
  <tbody>
    <?php foreach ($sips as $sip): ?>
    <tr class="<?php echo 0 == $row++ % 2 ? 'even' : 'odd' ?>">
      <td><?php echo $sip->getSipStatus() ?></td>
      <td><a href="<?php echo url_for('sip/show?id='.$sip->getId()) ?>"><?php echo $sip->getIdentifier() ?></a></td>
      <td><?php echo $sip->getTitle() ?></td>
      <td><?php echo $sip->getDateSubmitted() ?></td>
      <td><?php echo $sip->getProvenance() ?></td>
    </tr>
    <?php endforeach; ?>
  </tbody>
</table>
