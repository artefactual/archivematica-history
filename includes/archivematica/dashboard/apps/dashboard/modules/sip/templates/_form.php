<?php use_stylesheets_for_form($form) ?>
<?php use_javascripts_for_form($form) ?>

<form action="<?php echo url_for('sip/'.($form->getObject()->isNew() ? 'create' : 'update').(!$form->getObject()->isNew() ? '?id='.$form->getObject()->getId() : '')) ?>" method="post" <?php $form->isMultipart() and print 'enctype="multipart/form-data" ' ?>>
<?php if (!$form->getObject()->isNew()): ?>
<input type="hidden" name="sf_method" value="put" />
<?php endif; ?>
  <table>
    <tfoot>
      <tr>
        <td colspan="2">
          <?php echo $form->renderHiddenFields(false) ?>
          &nbsp;<a href="<?php echo url_for('sip/index') ?>">Back to list</a>
          <?php if (!$form->getObject()->isNew()): ?>
            &nbsp;<?php echo link_to('Delete', 'sip/delete?id='.$form->getObject()->getId(), array('method' => 'delete', 'confirm' => 'Are you sure?')) ?>
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
        <th><?php echo $form['title']->renderLabel() ?></th>
        <td>
          <?php echo $form['title']->renderError() ?>
          <?php echo $form['title'] ?>
        </td>
      </tr>
      <tr>
        <th><?php echo $form['dateReceived']->renderLabel() ?></th>
        <td>
          <?php echo $form['dateReceived']->renderError() ?>
          <?php echo $form['dateReceived'] ?>
        </td>
      </tr>
      <tr>
        <th><?php echo $form['provenance']->renderLabel() ?></th>
        <td>
          <?php echo $form['provenance']->renderError() ?>
          <?php echo $form['provenance'] ?>
        </td>
      </tr>
      <tr>
        <th><?php echo $form['partOf']->renderLabel() ?></th>
        <td>
          <?php echo $form['partOf']->renderError() ?>
          <?php echo $form['partOf'] ?>
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
    </tbody>
  </table>
</form>
