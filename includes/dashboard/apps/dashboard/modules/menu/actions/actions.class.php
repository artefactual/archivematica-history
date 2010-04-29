<?php

/**
 * menu actions.
 *
 * @package    dashboard
 * @subpackage menu
 * @author     Your name here
 * @version    SVN: $Id$
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
