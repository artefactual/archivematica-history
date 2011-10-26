<?php

$cfg = array(
  'format' => 'http://purl.org/net/sword-types/METSArchivematicaDIP',
  'contenttype' => 'application/zip',
  'obo' => null,
  'url' => 'http://localhost/ica-atom/index.php/sword/deposit/archivematica');

if ('cli' !== php_sapi_name())
{
  die('This script was designed for php-cli.');
}

if (in_array($argv[1], array('--help', '-help', '-h', '-?')))
{
   die(<<<content
    Usage:
      $argv[0] USERNAME PASSWORD FILENAME

content
  );
}

$cfg['username'] = $argv[1];
$cfg['password'] = $argv[2];

$directory = $argv[3];
$a = new ZipArchive;


require(dirname(__FILE__).'/swordapp-php-library/swordappclient.php');
$client = new SWORDAPPClient();

$deposit = $client->deposit(
  $cfg['url'],
  $cfg['username'],
  $cfg['password'],
  $cfg['obo'],
  $cfg['file'],
  $cfg['format'],
  $cfg['contenttype']);

if ($client->sac_status == 201)
{
  echo $client->sac_status;
  exit(0);
}
else
{
  echo $client->sac_status;
  exit(1);
}
