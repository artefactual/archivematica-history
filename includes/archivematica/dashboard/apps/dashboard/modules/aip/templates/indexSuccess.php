<h2 class="element-invisible">Toolbar</h2>
<div class="toolbar">
  <ul>
    <li><?php echo link_to(image_tag('folder_add_48.png'), array('module' => 'aip', 'action' => 'new'), array('title' => __('new AIP'))) ?></li>
    <li><?php echo link_to(image_tag('refresh_48.png'), array('module' => 'aip', 'action' => 'index'), array('title' => __('refresh page'))) ?></li>
    <li><?php echo link_to(image_tag('printer_48.png'), array('module' => 'report', 'action' => 'index'), array('title' => __('print report'))) ?></li>
    <li><?php echo link_to(image_tag('search_48.png'), array('module' => 'search', 'action' => 'index'), array('title' => __('search'))) ?></li>
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
