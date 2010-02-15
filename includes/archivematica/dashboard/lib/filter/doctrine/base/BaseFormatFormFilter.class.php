<?php

/**
 * Format filter form base class.
 *
 * @package    dashboard
 * @subpackage filter
 * @author     Your name here
 * @version    SVN: $Id$
 */
abstract class BaseFormatFormFilter extends BaseFormFilterDoctrine
{
  public function setup()
  {
    $this->setWidgets(array(
      'name'         => new sfWidgetFormFilterInput(array('with_empty' => false)),
      'extension'    => new sfWidgetFormFilterInput(),
      'mime_type'    => new sfWidgetFormFilterInput(),
      'registry_uri' => new sfWidgetFormFilterInput(),
      'files_list'   => new sfWidgetFormDoctrineChoice(array('multiple' => true, 'model' => 'File')),
    ));

    $this->setValidators(array(
      'name'         => new sfValidatorPass(array('required' => false)),
      'extension'    => new sfValidatorPass(array('required' => false)),
      'mime_type'    => new sfValidatorPass(array('required' => false)),
      'registry_uri' => new sfValidatorPass(array('required' => false)),
      'files_list'   => new sfValidatorDoctrineChoice(array('multiple' => true, 'model' => 'File', 'required' => false)),
    ));

    $this->widgetSchema->setNameFormat('format_filters[%s]');

    $this->errorSchema = new sfValidatorErrorSchema($this->validatorSchema);

    $this->setupInheritance();

    parent::setup();
  }

  public function addFilesListColumnQuery(Doctrine_Query $query, $field, $values)
  {
    if (!is_array($values))
    {
      $values = array($values);
    }

    if (!count($values))
    {
      return;
    }

    $query->leftJoin('r.FormatRole FormatRole')
          ->andWhereIn('FormatRole.file_id', $values);
  }

  public function getModelName()
  {
    return 'Format';
  }

  public function getFields()
  {
    return array(
      'id'           => 'Number',
      'name'         => 'Text',
      'extension'    => 'Text',
      'mime_type'    => 'Text',
      'registry_uri' => 'Text',
      'files_list'   => 'ManyKey',
    );
  }
}
