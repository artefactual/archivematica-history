<?php

/**
 * aip actions.
 *
 * @package    dashboard
 * @subpackage aip
 * @author     Your name here
 * @version    SVN: $Id: actions.class.php 127 2010-02-19 23:03:24Z peter $
 */
class aipActions extends sfActions
{
  public function executeIndex(sfWebRequest $request)
  {
    $this->aips = Doctrine::getTable('Aip')
      ->createQuery('a')
      ->execute();
  }

  public function executeShow(sfWebRequest $request)
  {
    $this->aip = Doctrine::getTable('Aip')->find(array($request->getParameter('id')));
    $this->forward404Unless($this->aip);
  }

  public function executeNew(sfWebRequest $request)
  {
    $this->form = new AipForm();
  }

  public function executeCreate(sfWebRequest $request)
  {
    $this->forward404Unless($request->isMethod(sfRequest::POST));

    $this->form = new AipForm();

    $this->processForm($request, $this->form);

    $this->setTemplate('new');
  }

  public function executeEdit(sfWebRequest $request)
  {
    $this->forward404Unless($aip = Doctrine::getTable('Aip')->find(array($request->getParameter('id'))), sprintf('Object aip does not exist (%s).', $request->getParameter('id')));
    $this->form = new AipForm($aip);
  }

  public function executeUpdate(sfWebRequest $request)
  {
    $this->forward404Unless($request->isMethod(sfRequest::POST) || $request->isMethod(sfRequest::PUT));
    $this->forward404Unless($aip = Doctrine::getTable('Aip')->find(array($request->getParameter('id'))), sprintf('Object aip does not exist (%s).', $request->getParameter('id')));
    $this->form = new AipForm($aip);

    $this->processForm($request, $this->form);

    $this->setTemplate('edit');
  }

  public function executeDelete(sfWebRequest $request)
  {
    $request->checkCSRFProtection();

    $this->forward404Unless($aip = Doctrine::getTable('Aip')->find(array($request->getParameter('id'))), sprintf('Object aip does not exist (%s).', $request->getParameter('id')));
    $aip->delete();

    $this->redirect('aip/index');
  }

  protected function processForm(sfWebRequest $request, sfForm $form)
  {
    $form->bind($request->getParameter($form->getName()), $request->getFiles($form->getName()));
    if ($form->isValid())
    {
      $aip = $form->save();

      $this->redirect('aip/edit?id='.$aip->getId());
    }
  }
}
