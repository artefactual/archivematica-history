<?php

/**
 * menu actions.
 *
 * @package    dashboard
 * @subpackage menu
 * @author     Your name here
 * @version    SVN: $Id: actions.class.php 145 2010-02-22 07:20:13Z peter $
 */
class menuActions extends sfActions
{
 /**
  * Executes index action
  *
  * @param sfRequest $request A request object
  */
  public function executeIndex(sfWebRequest $request)
  {
    $this->forward('default', 'module');
  }
}
