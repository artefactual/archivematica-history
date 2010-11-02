<?php

/**
 * Sip
 * 
 * This class has been auto-generated by the Doctrine ORM Framework
 * 
 * @package    dashboard
 * @subpackage model
 * @author     Your name here
 * @version    SVN: $Id: Sip.class.php 166 2010-02-25 23:12:45Z peter $
 */
class Sip extends BaseSip
{

  public function getStatus()
  {
    $q = Doctrine_Query::create()
      ->from('SipStatus s')
      ->leftJoin('s.SipStatusLogs l')
      ->where('l.sip_id = ?', $this->getId())
      ->andWhere('l.closed_at IS NULL');
 
    return $q->fetchOne();
  }

  public function getStatusLog()
  {
    return Doctrine_Query::create()
      ->from('SipStatusLog s')
      ->where('s.sip_id = ?', $this->getId())
      ->andWhere('s.closed_at IS NOT NULL')
      ->orderBy('s.closed_at DESC')
      ->execute();
  }

  public function getCurrentStatusLog()
  {
    $q = Doctrine_Query::create()
      ->from('SipStatusLog s')
      ->where('s.sip_id = ?', $this->getId())
      ->andWhere('s.closed_at IS NULL');

    return $q->fetchOne();
  }  
}
