<?php

/**
 * BaseAip
 * 
 * This class has been auto-generated by the Doctrine ORM Framework
 * 
 * @property string $identifier
 * @property timestamp $dateAccepted
 * @property string $checksum
 * @property string $checksum_type
 * @property string $location
 * @property string $dip_location
 * @property Doctrine_Collection $AipStatusLogs
 * @property Doctrine_Collection $Files
 * 
 * @method string              getIdentifier()    Returns the current record's "identifier" value
 * @method timestamp           getDateAccepted()  Returns the current record's "dateAccepted" value
 * @method string              getChecksum()      Returns the current record's "checksum" value
 * @method string              getChecksumType()  Returns the current record's "checksum_type" value
 * @method string              getLocation()      Returns the current record's "location" value
 * @method string              getDipLocation()   Returns the current record's "dip_location" value
 * @method Doctrine_Collection getAipStatusLogs() Returns the current record's "AipStatusLogs" collection
 * @method Doctrine_Collection getFiles()         Returns the current record's "Files" collection
 * @method Aip                 setIdentifier()    Sets the current record's "identifier" value
 * @method Aip                 setDateAccepted()  Sets the current record's "dateAccepted" value
 * @method Aip                 setChecksum()      Sets the current record's "checksum" value
 * @method Aip                 setChecksumType()  Sets the current record's "checksum_type" value
 * @method Aip                 setLocation()      Sets the current record's "location" value
 * @method Aip                 setDipLocation()   Sets the current record's "dip_location" value
 * @method Aip                 setAipStatusLogs() Sets the current record's "AipStatusLogs" collection
 * @method Aip                 setFiles()         Sets the current record's "Files" collection
 * 
 * @package    dashboard
 * @subpackage model
 * @author     Your name here
 * @version    SVN: $Id$
 */
abstract class BaseAip extends sfDoctrineRecord
{
    public function setTableDefinition()
    {
        $this->setTableName('aip');
        $this->hasColumn('identifier', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
        $this->hasColumn('dateAccepted', 'timestamp', 25, array(
             'type' => 'timestamp',
             'notnull' => true,
             'length' => '25',
             ));
        $this->hasColumn('checksum', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
        $this->hasColumn('checksum_type', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
        $this->hasColumn('location', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
        $this->hasColumn('dip_location', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
    }

    public function setUp()
    {
        parent::setUp();
        $this->hasMany('AipStatusLog as AipStatusLogs', array(
             'local' => 'id',
             'foreign' => 'aip_id'));

        $this->hasMany('File as Files', array(
             'local' => 'id',
             'foreign' => 'aip_id'));
    }
}