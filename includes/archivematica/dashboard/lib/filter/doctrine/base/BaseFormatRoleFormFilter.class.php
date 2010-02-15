<?php

/**
 * FormatRole filter form base class.
 *
 * @package    dashboard
 * @subpackage filter
 * @author     Your name here
 * @version    SVN: $Id$
 */
abstract class BaseFormatRoleFormFilter extends BaseFormFilterDoctrine
{
  public function setup()
  {
    $this->setWidgets(array(
      'role'      => new sfWidgetFormFilterInput(),
    ));

    $this->setValidators(array(
      'role'      => new sfValidatorPass(array('required' => false)),
    ));

    $this->widgetSchema->setNameFormat('format_role_filters[%s]');

    $this->errorSchema = new sfValidatorErrorSchema($this->validatorSchema);

    $this->setupInheritance();

    parent::setup();
  }

  public function getModelName()
  {
    return 'FormatRole';
  }

  public function getFields()
  {
    return array(
      'format_id' => 'Number',
      'file_id'   => 'Number',
      'role'      => 'Text',
    );
  }
}
