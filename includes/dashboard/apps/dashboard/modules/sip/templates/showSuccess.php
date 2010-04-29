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
  </tbody>
</table>

<hr />

<?php echo get_partial('sip/status', array('sip' => $sip)) ?>

<hr />

<a href="<?php echo url_for('sip/edit?id='.$sip->getId()) ?>">Edit</a>
&nbsp;
<a href="<?php echo url_for('sip/index') ?>">List</a>
