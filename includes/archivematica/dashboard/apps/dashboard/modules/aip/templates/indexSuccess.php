<div class="toolbar">
  <ul>
    <li><?php echo link_to(image_tag('folder-new.png'), array('module' => 'aip', 'action' => 'new'), array('alt' => __('new AIP'))) ?></li>
    <li><?php echo link_to(image_tag('document-print.png'), array('module' => 'report', 'action' => 'index'), array('alt' => __('print report'))) ?></li>
    <li><?php echo link_to(image_tag('system-search.png'), array('module' => 'search', 'action' => 'index'), array('alt' => __('search'))) ?></li>
</div>

<table>
  <thead>
    <tr>
      <th><?php echo __('Status') ?></th>
      <th><?php echo __('Identifier') ?></th>
      <th><?php echo __('Date accepted') ?></th>
      <th><?php echo __('Location') ?></th>
      <th><?php echo __('Dip location') ?></th>
    </tr>
  </thead>
  <tbody>
    <?php foreach ($aips as $aip): ?>
    <tr class="<?php echo 0 == $row++ % 2 ? 'even' : 'odd' ?>">
      <td><?php echo $aip->getAipStatus() ?></td>
      <td><a href="<?php echo url_for('aip/show?id='.$aip->getId()) ?>"><?php echo $aip->getIdentifier() ?></a></td>
      <td><?php echo $aip->getDateAccepted() ?></td>
      <td><?php echo $aip->getLocation() ?></td>
      <td><?php echo $aip->getDipLocation() ?></td>
    </tr>
    <?php endforeach; ?>
  </tbody>
</table>
