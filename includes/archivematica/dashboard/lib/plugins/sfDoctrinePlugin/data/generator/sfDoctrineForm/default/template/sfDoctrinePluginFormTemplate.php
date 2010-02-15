[?php

/**
 * <?php echo $this->table->getOption('name') ?> form.
 *
 * @package    dashboard
 * @subpackage form
 * @author     Your name here
 * @version    SVN: $Id$
 */
class <?php echo $this->table->getOption('name') ?>Form extends Plugin<?php echo $this->table->getOption('name') ?>Form
{
<?php if ($parent = $this->getParentModel()): ?>
  /**
   * @see <?php echo $parent ?>Form
   */
  public function configure()
  {
    parent::configure();
  }
<?php else: ?>
  public function configure()
  {
  }
<?php endif; ?>
}
