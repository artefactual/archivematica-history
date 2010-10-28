<table>
  <tbody>
    <tr>
      <th>Id:</th>
      <td><?php echo $aip->getId() ?></td>
    </tr>
    <tr>
      <th>Identifier:</th>
      <td><?php echo $aip->getIdentifier() ?></td>
    </tr>
    <tr>
      <th>Date accepted:</th>
      <td><?php echo $aip->getDateAccepted() ?></td>
    </tr>
    <tr>
      <th>Location:</th>
      <td><?php echo $aip->getLocation() ?></td>
    </tr>
    <tr>
      <th>Dip location:</th>
      <td><?php echo $aip->getDipLocation() ?></td>
    </tr>
  </tbody>
</table>

<hr />

<a href="<?php echo url_for('aip/edit?id='.$aip->getId()) ?>">Edit</a>
&nbsp;
<a href="<?php echo url_for('aip/index') ?>">List</a>
