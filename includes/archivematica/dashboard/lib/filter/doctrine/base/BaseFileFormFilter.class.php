<?php

/**
 * File filter form base class.
 *
 * @package    dashboard
 * @subpackage filter
 * @author     Your name here
 * @version    SVN: $Id$
 */
abstract class BaseFileFormFilter extends BaseFormFilterDoctrine
{
  public function setup()
  {
    $this->setWidgets(array(
      'sip_id'            => new sfWidgetFormDoctrineChoice(array('model' => $this->getRelatedModelName('Sip'), 'add_empty' => true)),
      'aip_id'            => new sfWidgetFormDoctrineChoice(array('model' => $this->getRelatedModelName('Aip'), 'add_empty' => true)),
      'file_status_id'    => new sfWidgetFormDoctrineChoice(array('model' => $this->getRelatedModelName('FileStatus'), 'add_empty' => true)),
      'identifier'        => new sfWidgetFormFilterInput(),
      'title'             => new sfWidgetFormFilterInput(),
      'original_filename' => new sfWidgetFormFilterInput(),
      'clean_filename'    => new sfWidgetFormFilterInput(),
      'filepath'          => new sfWidgetFormFilterInput(),
      'date'              => new sfWidgetFormFilterDate(array('from_date' => new sfWidgetFormDate(), 'to_date' => new sfWidgetFormDate())),
      'checksum'          => new sfWidgetFormFilterInput(),
      'checksum_type'     => new sfWidgetFormFilterInput(),
      'formats_list'      => new sfWidgetFormDoctrineChoice(array('multiple' => true, 'model' => 'Format')),
    ));

    $this->setValidators(array(
      'sip_id'            => new sfValidatorDoctrineChoice(array('required' => false, 'model' => $this->getRelatedModelName('Sip'), 'column' => 'id')),
      'aip_id'            => new sfValidatorDoctrineChoice(array('required' => false, 'model' => $this->getRelatedModelName('Aip'), 'column' => 'id')),
      'file_status_id'    => new sfValidatorDoctrineChoice(array('required' => false, 'model' => $this->getRelatedModelName('FileStatus'), 'column' => 'id')),
      'identifier'        => new sfValidatorPass(array('required' => false)),
      'title'             => new sfValidatorPass(array('required' => false)),
      'original_filename' => new sfValidatorPass(array('required' => false)),
      'clean_filename'    => new sfValidatorPass(array('required' => false)),
      'filepath'          => new sfValidatorPass(array('required' => false)),
      'date'              => new sfValidatorDateRange(array('required' => false, 'from_date' => new sfValidatorDate(array('required' => false)), 'to_date' => new sfValidatorDateTime(array('required' => false)))),
      'checksum'          => new sfValidatorPass(array('required' => false)),
      'checksum_type'     => new sfValidatorPass(array('required' => false)),
      'formats_list'      => new sfValidatorDoctrineChoice(array('multiple' => true, 'model' => 'Format', 'required' => false)),
    ));

    $this->widgetSchema->setNameFormat('file_filters[%s]');

    $this->errorSchema = new sfValidatorErrorSchema($this->validatorSchema);

    $this->setupInheritance();

    parent::setup();
  }

  public function addFormatsListColumnQuery(Doctrine_Query $query, $field, $values)
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
    return 'File';
  }

  public function getFields()
  {
    return array(
      'id'                => 'Number',
      'sip_id'            => 'ForeignKey',
      'aip_id'            => 'ForeignKey',
      'file_status_id'    => 'ForeignKey',
      'identifier'        => 'Text',
      'title'             => 'Text',
      'original_filename' => 'Text',
      'clean_filename'    => 'Text',
      'filepath'          => 'Text',
      'date'              => 'Date',
      'checksum'          => 'Text',
      'checksum_type'     => 'Text',
      'formats_list'      => 'ManyKey',
    );
  }
}
