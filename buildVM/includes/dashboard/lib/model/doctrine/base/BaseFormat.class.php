<?php

/**
 * BaseFormat
 * 
 * This class has been auto-generated by the Doctrine ORM Framework
 * 
 * @property string $name
 * @property string $extension
 * @property string $mime_type
 * @property string $registry_uri
 * @property Doctrine_Collection $Files
 * @property Doctrine_Collection $FormatRole
 * 
 * @method string              getName()         Returns the current record's "name" value
 * @method string              getExtension()    Returns the current record's "extension" value
 * @method string              getMimeType()     Returns the current record's "mime_type" value
 * @method string              getRegistryUri()  Returns the current record's "registry_uri" value
 * @method Doctrine_Collection getFiles()        Returns the current record's "Files" collection
 * @method Doctrine_Collection getFormatRole()   Returns the current record's "FormatRole" collection
 * @method Format              setName()         Sets the current record's "name" value
 * @method Format              setExtension()    Sets the current record's "extension" value
 * @method Format              setMimeType()     Sets the current record's "mime_type" value
 * @method Format              setRegistryUri()  Sets the current record's "registry_uri" value
 * @method Format              setFiles()        Sets the current record's "Files" collection
 * @method Format              setFormatRole()   Sets the current record's "FormatRole" collection
 * 
 * @package    dashboard
 * @subpackage model
 * @author     Your name here
 * @version    SVN: $Id$
 */
abstract class BaseFormat extends sfDoctrineRecord
{
    public function setTableDefinition()
    {
        $this->setTableName('format');
        $this->hasColumn('name', 'string', 255, array(
             'type' => 'string',
             'notnull' => true,
             'unique' => true,
             'length' => '255',
             ));
        $this->hasColumn('extension', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
        $this->hasColumn('mime_type', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
        $this->hasColumn('registry_uri', 'string', 255, array(
             'type' => 'string',
             'length' => '255',
             ));
    }

    public function setUp()
    {
        parent::setUp();
        $this->hasMany('File as Files', array(
             'refClass' => 'FormatRole',
             'local' => 'format_id',
             'foreign' => 'file_id'));

        $this->hasMany('FormatRole', array(
             'local' => 'id',
             'foreign' => 'format_id'));
    }
}