<?php

/**
 * BaseFile
 * 
 * This class has been auto-generated by the Doctrine ORM Framework
 * 
 * @property integer $sip_id
 * @property integer $aip_id
 * @property string $identifier
 * @property string $title
 * @property string $original_filename
 * @property string $clean_filename
 * @property string $filepath
 * @property date $date
 * @property string $checksum
 * @property string $checksum_type
 * @property Sip $Sip
 * @property Aip $Aip
 * @property Doctrine_Collection $Formats
 * @property Doctrine_Collection $FileStatusLogs
 * @property Doctrine_Collection $FormatRole
 * 
 * @method integer             getSipId()             Returns the current record's "sip_id" value
 * @method integer             getAipId()             Returns the current record's "aip_id" value
 * @method string              getIdentifier()        Returns the current record's "identifier" value
 * @method string              getTitle()             Returns the current record's "title" value
 * @method string              getOriginalFilename()  Returns the current record's "original_filename" value
 * @method string              getCleanFilename()     Returns the current record's "clean_filename" value
 * @method string              getFilepath()          Returns the current record's "filepath" value
 * @method date                getDate()              Returns the current record's "date" value
 * @method string              getChecksum()          Returns the current record's "checksum" value
 * @method string              getChecksumType()      Returns the current record's "checksum_type" value
 * @method Sip                 getSip()               Returns the current record's "Sip" value
 * @method Aip                 getAip()               Returns the current record's "Aip" value
 * @method Doctrine_Collection getFormats()           Returns the current record's "Formats" collection
 * @method Doctrine_Collection getFileStatusLogs()    Returns the current record's "FileStatusLogs" collection
 * @method Doctrine_Collection getFormatRole()        Returns the current record's "FormatRole" collection
 * @method File                setSipId()             Sets the current record's "sip_id" value
 * @method File                setAipId()             Sets the current record's "aip_id" value
 * @method File                setIdentifier()        Sets the current record's "identifier" value
 * @method File                setTitle()             Sets the current record's "title" value
 * @method File                setOriginalFilename()  Sets the current record's "original_filename" value
 * @method File                setCleanFilename()     Sets the current record's "clean_filename" value
 * @method File                setFilepath()          Sets the current record's "filepath" value
 * @method File                setDate()              Sets the current record's "date" value
 * @method File                setChecksum()          Sets the current record's "checksum" value
 * @method File                setChecksumType()      Sets the current record's "checksum_type" value
 * @method File                setSip()               Sets the current record's "Sip" value
 * @method File                setAip()               Sets the current record's "Aip" value
 * @method File                setFormats()           Sets the current record's "Formats" collection
 * @method File                setFileStatusLogs()    Sets the current record's "FileStatusLogs" collection
 * @method File                setFormatRole()        Sets the current record's "FormatRole" collection
 * 
 * @package    dashboard
 * @subpackage model
 * @author     Your name here
 * @version    SVN: $Id: BaseFile.class.php 163 2010-02-25 01:10:58Z peter $
 */
abstract class BaseFile extends sfDoctrineRecord
{
    public function setTableDefinition()
    {
        $this->setTableName('file');
        $this->hasColumn('sip_id', 'integer', null, array(
             'type' => 'integer',
             'notnull' => true,
             ));
        $this->hasColumn('aip_id', 'integer', null, array(
             'type' => 'integer',
             ));
        $this->hasColumn('identifier', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
        $this->hasColumn('title', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
        $this->hasColumn('original_filename', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
        $this->hasColumn('clean_filename', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
        $this->hasColumn('filepath', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
        $this->hasColumn('date', 'date', null, array(
             'type' => 'date',
             ));
        $this->hasColumn('checksum', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
        $this->hasColumn('checksum_type', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
    }

    public function setUp()
    {
        parent::setUp();
        $this->hasOne('Sip', array(
             'local' => 'sip_id',
             'foreign' => 'id',
             'onDelete' => 'CASCADE'));

        $this->hasOne('Aip', array(
             'local' => 'aip_id',
             'foreign' => 'id',
             'onDelete' => 'CASCADE'));

        $this->hasMany('Format as Formats', array(
             'refClass' => 'FormatRole',
             'local' => 'format_id',
             'foreign' => 'file_id'));

        $this->hasMany('FileStatusLog as FileStatusLogs', array(
             'local' => 'id',
             'foreign' => 'file_id'));

        $this->hasMany('FormatRole', array(
             'local' => 'id',
             'foreign' => 'file_id'));
    }
}