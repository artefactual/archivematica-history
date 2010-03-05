<?php

/**
 * BaseSip
 * 
 * This class has been auto-generated by the Doctrine ORM Framework
 * 
 * @property string $identifier
 * @property string $title
 * @property timestamp $dateReceived
 * @property string $provenance
 * @property string $partOf
 * @property Doctrine_Collection $SipStatusLogs
 * @property Doctrine_Collection $Files
 * 
 * @method string              getIdentifier()    Returns the current record's "identifier" value
 * @method string              getTitle()         Returns the current record's "title" value
 * @method timestamp           getDateReceived()  Returns the current record's "dateReceived" value
 * @method string              getProvenance()    Returns the current record's "provenance" value
 * @method string              getPartOf()        Returns the current record's "partOf" value
 * @method Doctrine_Collection getSipStatusLogs() Returns the current record's "SipStatusLogs" collection
 * @method Doctrine_Collection getFiles()         Returns the current record's "Files" collection
 * @method Sip                 setIdentifier()    Sets the current record's "identifier" value
 * @method Sip                 setTitle()         Sets the current record's "title" value
 * @method Sip                 setDateReceived()  Sets the current record's "dateReceived" value
 * @method Sip                 setProvenance()    Sets the current record's "provenance" value
 * @method Sip                 setPartOf()        Sets the current record's "partOf" value
 * @method Sip                 setSipStatusLogs() Sets the current record's "SipStatusLogs" collection
 * @method Sip                 setFiles()         Sets the current record's "Files" collection
 * 
 * @package    dashboard
 * @subpackage model
 * @author     Your name here
 * @version    SVN: $Id$
 */
abstract class BaseSip extends sfDoctrineRecord
{
    public function setTableDefinition()
    {
        $this->setTableName('sip');
        $this->hasColumn('identifier', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
        $this->hasColumn('title', 'string', 255, array(
             'type' => 'string',
             'notnull' => true,
             'length' => '255',
             ));
        $this->hasColumn('dateReceived', 'timestamp', 25, array(
             'type' => 'timestamp',
             'notnull' => true,
             'length' => '25',
             ));
        $this->hasColumn('provenance', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
        $this->hasColumn('partOf', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
    }

    public function setUp()
    {
        parent::setUp();
        $this->hasMany('SipStatusLog as SipStatusLogs', array(
             'local' => 'id',
             'foreign' => 'sip_id'));

        $this->hasMany('File as Files', array(
             'local' => 'id',
             'foreign' => 'sip_id'));
    }
}