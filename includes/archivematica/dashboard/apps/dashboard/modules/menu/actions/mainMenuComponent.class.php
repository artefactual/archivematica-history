<?php

/*
 * This file is part of Archivematica.
 *
 * Archivematica is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * Archivematica is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.
 */

/**
 * Build main user navigation menu as simple xhtml lists, relying on css styling to
 * format the display of the menus.
 *
 * @package    Archivematica Dashboard
 * @subpackage menu
 * @version    
 * @author     Peter Van Garderen <peter@artefactual.com)
 */

class MainMenuComponent extends sfComponent
{
  public function execute($request)
  {
  // set active menu option
  $this->mdlName = sfContext::getInstance()->getModuleName();
  
  $this->option1 = ($this->mdlName =='sip' ? 'active' : null);
  $this->option2 = ($this->mdlName =='aip' ? 'active' : null);
  $this->option3 = null;
  $this->option4 = null;
  }
}

