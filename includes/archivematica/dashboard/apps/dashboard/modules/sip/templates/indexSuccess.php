<div class="toolbar">
  <ul>
    <li><?php echo link_to(image_tag('folder_add_48.png'), array('module' => 'sip', 'action' => 'new'), array('title' => __('new SIP'))) ?></li>
    <li><?php echo link_to(image_tag('refresh_48.png'), array('module' => 'sip', 'action' => 'index'), array('title' => __('refresh page'))) ?></li>
    <li><?php echo link_to(image_tag('printer_48.png'), array('module' => 'report', 'action' => 'index'), array('title' => __('print report'))) ?></li>
    <li><?php echo link_to(image_tag('search_48.png'), array('module' => 'search', 'action' => 'index'), array('title' => __('search'))) ?></li>
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
