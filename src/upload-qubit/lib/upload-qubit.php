#!/usr/bin/env php
<?php

error_reporting(E_ALL ^ E_NOTICE);

$cfg = array(
  'format' => 'http://purl.org/net/sword-types/METSArchivematicaDIP',
  'contenttype' => 'application/zip',
  'obo' => null,
  // Use qubit_dev.php instead of index.php if you want to switch on the debug mode
  'url' => 'http://localhost/ica-atom/index.php/sword/deposit/archivematica');

if ('cli' !== php_sapi_name())
{
  die("This script was designed for php-cli.\n");
}

if (4 > $argc || in_array(@$argv[1], array('--help', '-help', '-h', '-?')))
{
   die(<<<content
    Usage:
      $argv[0] USERNAME PASSWORD DIRECTORY

content
  );
}

$cfg['username'] = $argv[1];
$cfg['password'] = $argv[2];

$directory = $argv[3];

if (false == file_exists($directory) || false == is_readable($directory))
{
  die("Given directory could not be found or is not readable.\n");
}

$zip = new ZipArchive;
$file = tempnam('/tmp', 'dip');
$zip->open($file, ZipArchive::CREATE);
$zip->addFile($directory.'/METS.xml', 'METS.xml');
if ($handle = opendir($directory.'/objects'))
{
  while (false !== ($item = readdir($handle)))
  {
    if ($item == '.' || $item == '..')
    {
      continue;
    }

    $zip->addFile($directory.'/objects/'.$item, 'objects/'.$item);
  }
}
$zip->close();
$cfg['file'] = $file;

echo $file . " was generated. Sending to ICA-AtoM.\n";

require(dirname(__FILE__).'/swordapp-php-library/swordappclient.php');
$client = new SWORDAPPClient();

try
{
  $deposit = $client->deposit(
    $cfg['url'],
    $cfg['username'],
    $cfg['password'],
    $cfg['obo'],
    $cfg['file'],
    $cfg['format'],
    $cfg['contenttype']);
}
catch (Exception $e)
{
  echo "[!!] Package could not be deposited:\n";
  echo "[!!] " . $e->getMessage() . "\n";

  if (isset($e->data['status']))
  {
    echo "[!!] HTTP response status code: " . $e->data['status'] . "\n";
  }

  if (isset($e->data['response']) && 0 < strlen($e->data['response']))
  {
    echo "[!!] ----- Server response -----\n";
    echo $e->data['response'];
  }
  else
  {
    echo "[**] You should switch on the debug mode to get a detailed error report.\n";
  }

  exit(1);
}

if (unlink($file))
{
  echo $file . " was removed.\n";
}

if ($deposit->sac_status == 201)
{
  echo "Package uploaded successfully.\n";
  exit(0);
}
else
{
  echo "Package could not be uploaded.\n";
  exit(1);
}
