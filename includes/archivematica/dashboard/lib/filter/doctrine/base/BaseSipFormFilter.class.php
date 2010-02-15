<?php

/**
 * Sip filter form base class.
 *
 * @package    dashboard
 * @subpackage filter
 * @author     Your name here
 * @version    SVN: $Id$
 */
abstract class BaseSipFormFilter extends BaseFormFilterDoctrine
{
  public function setup()
  {
    $this->setWidgets(array(
      'sip_status_id' => new sfWidgetFormDoctrineChoice(array('model' => $this->getRelatedModelName('SipStatus'), 'add_empty' => true)),
      'identifier'    => new sfWidgetFormFilterInput(),
      'title'         => new sfWidgetFormFilterInput(array('with_empty' => false)),
      'dateSubmitted' => new sfWidgetFormFilterDate(array('from_date' => new sfWidgetFormDate(), 'to_date' => new sfWidgetFormDate(), 'with_empty' => false)),
      'provenance'    => new sfWidgetFormFilterInput(),
      'partOf'        => new sfWidgetFormFilterInput(),
      'checksum'      => new sfWidgetFormFilterInput(),
      'checksum_type' => new sfWidgetFormFilterInput(),
    ));

    $this->setValidators(array(
      'sip_status_id' => new sfValidatorDoctrineChoice(array('required' => false, 'model' => $this->getRelatedModelName('SipStatus'), 'column' => 'id')),
      'identifier'    => new sfValidatorPass(array('required' => false)),
      'title'         => new sfValidatorPass(array('required' => false)),
      'dateSubmitted' => new sfValidatorDateRange(array('required' => false, 'from_date' => new sfValidatorDateTime(array('required' => false, 'datetime_output' => 'Y-m-d 00:00:00')), 'to_date' => new sfValidatorDateTime(array('required' => false, 'datetime_output' => 'Y-m-d 23:59:59')))),
      'provenance'    => new sfValidatorPass(array('required' => false)),
      'partOf'        => new sfValidatorPass(array('required' => false)),
      'checksum'      => new sfValidatorPass(array('required' => false)),
      'checksum_type' => new sfValidatorPass(array('required' => false)),
    ));

    $this->widgetSchema->setNameFormat('sip_filters[%s]');

    $this->errorSchema = new sfValidatorErrorSchema($this->validatorSchema);

    $this->setupInheritance();

    parent::setup();
  }

  public function getModelName()
  {
    return 'Sip';
  }

  public function getFields()
  {
    return array(
      'id'            => 'Number',
      'sip_status_id' => 'ForeignKey',
      'identifier'    => 'Text',
      'title'         => 'Text',
      'dateSubmitted' => 'Date',
      'provenance'    => 'Text',
      'partOf'        => 'Text',
      'checksum'      => 'Text',
      'checksum_type' => 'Text',
    );
  }
}
