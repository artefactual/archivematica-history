[?php

/**
 * <?php echo $this->getModuleName() ?> module configuration.
 *
 * @package    dashboard
 * @subpackage <?php echo $this->getModuleName()."\n" ?>
 * @author     Your name here
 * @version    SVN: $Id$
 */
abstract class Base<?php echo ucfirst($this->getModuleName()) ?>GeneratorHelper extends sfModelGeneratorHelper
{
  public function getUrlForAction($action)
  {
    return 'list' == $action ? '<?php echo $this->params['route_prefix'] ?>' : '<?php echo $this->params['route_prefix'] ?>_'.$action;
  }
}
