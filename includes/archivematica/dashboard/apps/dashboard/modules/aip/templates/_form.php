<?php use_stylesheets_for_form($form) ?>
<?php use_javascripts_for_form($form) ?>

<form action="<?php echo url_for('aip/'.($form->getObject()->isNew() ? 'create' : 'update').(!$form->getObject()->isNew() ? '?id='.$form->getObject()->getId() : '')) ?>" method="post" <?php $form->isMultipart() and print 'enctype="multipart/form-data" ' ?>>
<?php if (!$form->getObject()->isNew()): ?>
<input type="hidden" name="sf_method" value="put" />
<?php endif; ?>
  <table>
    <tfoot>
      <tr>
        <td colspan="2">
          <?php echo $form->renderHiddenFields(false) ?>
          &nbsp;<a href="<?php echo url_for('aip/index') ?>">Back to list</a>
          <?php if (!$form->getObject()->isNew()): ?>
            &nbsp;<?php echo link_to('Delete', 'aip/delete?id='.$form->getObject()->getId(), array('method' => 'delete', 'confirm' => 'Are you sure?')) ?>
          <?php endif; ?>
          <input type="submit" value="Save" />
        </td>
      </tr>
    </tfoot>
    <tbody>
      <?php echo $form->renderGlobalErrors() ?>
      <tr>
        <th><?php echo $form['identifier']->renderLabel() ?></th>
        <td>
          <?php echo $form['identifier']->renderError() ?>
          <?php echo $form['identifier'] ?>
        </td>
      </tr>
      <tr>
        <th><?php echo $form['dateAccepted']->renderLabel() ?></th>
        <td>
          <?php echo $form['dateAccepted']->renderError() ?>
          <?php echo $form['dateAccepted'] ?>
        </td>
      </tr>
      <tr>
        <th><?php echo $form['checksum']->renderLabel() ?></th>
        <td>
          <?php echo $form['checksum']->renderError() ?>
          <?php echo $form['checksum'] ?>
        </td>
      </tr>
      <tr>
        <th><?php echo $form['checksum_type']->renderLabel() ?></th>
        <td>
          <?php echo $form['checksum_type']->renderError() ?>
          <?php echo $form['checksum_type'] ?>
        </td>
      </tr>
      <tr>
        <th><?php echo $form['location']->renderLabel() ?></th>
        <td>
          <?php echo $form['location']->renderError() ?>
          <?php echo $form['location'] ?>
        </td>
      </tr>
      <tr>
        <th><?php echo $form['dip_location']->renderLabel() ?></th>
        <td>
          <?php echo $form['dip_location']->renderError() ?>
          <?php echo $form['dip_location'] ?>
        </td>
      </tr>
    </tbody>
  </table>
</form>
