<h1>Sips List</h1>

<table>
  <thead>
    <tr>
      <th>Status</th>
      <th>Identifier</th>
      <th>Title</th>
      <th>Date submitted</th>
      <th>Provenance</th>
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

  <a href="<?php echo url_for('sip/new') ?>">New</a>
