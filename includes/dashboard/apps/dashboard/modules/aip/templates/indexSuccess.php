<h1>Aips List</h1>

<table>
  <thead>
    <tr>
      <th>Id</th>
      <th>Identifier</th>
      <th>Date accepted</th>
      <th>Location</th>
      <th>Dip location</th>
    </tr>
  </thead>
  <tbody>
    <?php foreach ($aips as $aip): ?>
    <tr>
      <td><a href="<?php echo url_for('aip/show?id='.$aip->getId()) ?>"><?php echo $aip->getId() ?></a></td>
      <td><?php echo $aip->getIdentifier() ?></td>
      <td><?php echo $aip->getDateAccepted() ?></td>
      <td><?php echo $aip->getLocation() ?></td>
      <td><?php echo $aip->getDipLocation() ?></td>
    </tr>
    <?php endforeach; ?>
  </tbody>
</table>

  <a href="<?php echo url_for('aip/new') ?>">New</a>
