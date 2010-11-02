<?php

/**
 * sip actions.
 *
 * @package    dashboard
 * @subpackage sip
 * @author     Your name here
 * @version    SVN: $Id: actions.class.php 127 2010-02-19 23:03:24Z peter $
 */
class sipActions extends sfActions
{
  public function executeIndex(sfWebRequest $request)
  {
    $this->sips = Doctrine::getTable('Sip')
      ->createQuery('a')
      ->execute();
  }

  public function executeShow(sfWebRequest $request)
  {
    $this->sip = Doctrine::getTable('Sip')->find(array($request->getParameter('id')));
    $this->forward404Unless($this->sip);
  }

  public function executeNew(sfWebRequest $request)
  {
    $this->form = new SipForm();
  }

  public function executeCreate(sfWebRequest $request)
  {
    $this->forward404Unless($request->isMethod(sfRequest::POST));

    $this->form = new SipForm();

    $this->processForm($request, $this->form);

    $this->setTemplate('new');
  }

  public function executeEdit(sfWebRequest $request)
  {
    $this->forward404Unless($sip = Doctrine::getTable('Sip')->find(array($request->getParameter('id'))), sprintf('Object sip does not exist (%s).', $request->getParameter('id')));
    $this->form = new SipForm($sip);
  }

  public function executeUpdate(sfWebRequest $request)
  {
    $this->forward404Unless($request->isMethod(sfRequest::POST) || $request->isMethod(sfRequest::PUT));
    $this->forward404Unless($sip = Doctrine::getTable('Sip')->find(array($request->getParameter('id'))), sprintf('Object sip does not exist (%s).', $request->getParameter('id')));
    $this->form = new SipForm($sip);

    $this->processForm($request, $this->form);

    $this->setTemplate('edit');
  }

  public function executeDelete(sfWebRequest $request)
  {
    $request->checkCSRFProtection();

    $this->forward404Unless($sip = Doctrine::getTable('Sip')->find(array($request->getParameter('id'))), sprintf('Object sip does not exist (%s).', $request->getParameter('id')));
    $sip->delete();

    $this->redirect('sip/index');
  }

  protected function processForm(sfWebRequest $request, sfForm $form)
  {
    $form->bind($request->getParameter($form->getName()), $request->getFiles($form->getName()));
    if ($form->isValid())
    {
      $sip = $form->save();

      $this->redirect('sip/edit?id='.$sip->getId());
    }
  }
}
