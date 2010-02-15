<?php use_stylesheets_for_form($form) ?>
<?php use_javascripts_for_form($form) ?>

<form action="<?php echo url_for('file/'.($form->getObject()->isNew() ? 'create' : 'update').(!$form->getObject()->isNew() ? '?id='.$form->getObject()->getId() : '')) ?>" method="post" <?php $form->isMultipart() and print 'enctype="multipart/form-data" ' ?>>
<?php if (!$form->getObject()->isNew()): ?>
<input type="hidden" name="sf_method" value="put" />
<?php endif; ?>
  <table>
    <tfoot>
      <tr>
        <td colspan="2">
          <?php echo $form->renderHiddenFields(false) ?>
          &nbsp;<a href="<?php echo url_for('file/index') ?>">Back to list</a>
          <?php if (!$form->getObject()->isNew()): ?>
            &nbsp;<?php echo link_to('Delete', 'file/delete?id='.$form->getObject()->getId(), array('method' => 'delete', 'confirm' => 'Are you sure?')) ?>
          <?php endif; ?>
          <input type="submit" value="Save" />
        </td>
      </tr>
    </tfoot>
    <tbody>
      <?php echo $form->renderGlobalErrors() ?>
      <tr>
        <th><?php echo $form['sip_id']->renderLabel() ?></th>
        <td>
          <?php echo $form['sip_id']->renderError() ?>
          <?php echo $form['sip_id'] ?>
        </td>
      </tr>
      <tr>
        <th><?php echo $form['aip_id']->renderLabel() ?></th>
        <td>
          <?php echo $form['aip_id']->renderError() ?>
          <?php echo $form['aip_id'] ?>
        </td>
      </tr>
      <tr>
        <th><?php echo $form['file_status_id']->renderLabel() ?></th>
        <td>
          <?php echo $form['file_status_id']->renderError() ?>
          <?php echo $form['file_status_id'] ?>
        </td>
      </tr>
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
        <th><?php echo $form['original_filename']->renderLabel() ?></th>
        <td>
          <?php echo $form['original_filename']->renderError() ?>
          <?php echo $form['original_filename'] ?>
        </td>
      </tr>
      <tr>
        <th><?php echo $form['clean_filename']->renderLabel() ?></th>
        <td>
          <?php echo $form['clean_filename']->renderError() ?>
          <?php echo $form['clean_filename'] ?>
        </td>
      </tr>
      <tr>
        <th><?php echo $form['filepath']->renderLabel() ?></th>
        <td>
          <?php echo $form['filepath']->renderError() ?>
          <?php echo $form['filepath'] ?>
        </td>
      </tr>
      <tr>
        <th><?php echo $form['date']->renderLabel() ?></th>
        <td>
          <?php echo $form['date']->renderError() ?>
          <?php echo $form['date'] ?>
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
        <th><?php echo $form['formats_list']->renderLabel() ?></th>
        <td>
          <?php echo $form['formats_list']->renderError() ?>
          <?php echo $form['formats_list'] ?>
        </td>
      </tr>
    </tbody>
  </table>
</form>
