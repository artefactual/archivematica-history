<?php

/**
 * Aip filter form base class.
 *
 * @package    dashboard
 * @subpackage filter
 * @author     Your name here
 * @version    SVN: $Id$
 */
abstract class BaseAipFormFilter extends BaseFormFilterDoctrine
{
  public function setup()
  {
    $this->setWidgets(array(
      'aip_status_id' => new sfWidgetFormDoctrineChoice(array('model' => $this->getRelatedModelName('AipStatus'), 'add_empty' => true)),
      'identifier'    => new sfWidgetFormFilterInput(),
      'dateAccepted'  => new sfWidgetFormFilterDate(array('from_date' => new sfWidgetFormDate(), 'to_date' => new sfWidgetFormDate(), 'with_empty' => false)),
      'checksum'      => new sfWidgetFormFilterInput(),
      'checksum_type' => new sfWidgetFormFilterInput(),
      'location'      => new sfWidgetFormFilterInput(),
      'dip_location'  => new sfWidgetFormFilterInput(),
    ));

    $this->setValidators(array(
      'aip_status_id' => new sfValidatorDoctrineChoice(array('required' => false, 'model' => $this->getRelatedModelName('AipStatus'), 'column' => 'id')),
      'identifier'    => new sfValidatorPass(array('required' => false)),
      'dateAccepted'  => new sfValidatorDateRange(array('required' => false, 'from_date' => new sfValidatorDateTime(array('required' => false, 'datetime_output' => 'Y-m-d 00:00:00')), 'to_date' => new sfValidatorDateTime(array('required' => false, 'datetime_output' => 'Y-m-d 23:59:59')))),
      'checksum'      => new sfValidatorPass(array('required' => false)),
      'checksum_type' => new sfValidatorPass(array('required' => false)),
      'location'      => new sfValidatorPass(array('required' => false)),
      'dip_location'  => new sfValidatorPass(array('required' => false)),
    ));

    $this->widgetSchema->setNameFormat('aip_filters[%s]');

    $this->errorSchema = new sfValidatorErrorSchema($this->validatorSchema);

    $this->setupInheritance();

    parent::setup();
  }

  public function getModelName()
  {
    return 'Aip';
  }

  public function getFields()
  {
    return array(
      'id'            => 'Number',
      'aip_status_id' => 'ForeignKey',
      'identifier'    => 'Text',
      'dateAccepted'  => 'Date',
      'checksum'      => 'Text',
      'checksum_type' => 'Text',
      'location'      => 'Text',
      'dip_location'  => 'Text',
    );
  }
}
