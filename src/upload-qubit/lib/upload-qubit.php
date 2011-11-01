#!/usr/bin/env php
<?php

error_reporting(E_ALL ^ E_NOTICE);

function zip ($source, $destination)
{
  if (extension_loaded('zip') === true)
  {
    if (file_exists($source) === true)
    {
      $zip = new ZipArchive();

      if ($zip->open($destination, ZIPARCHIVE::CREATE) === true)
      {
        $source = realpath($source);

        if (is_dir($source) === true)
        {
          $files = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($source), RecursiveIteratorIterator::SELF_FIRST);

          foreach ($files as $file)
          {
            $file = realpath($file);

            if (is_dir($file) === true)
            {
              $zip->addEmptyDir(str_replace($source . '/', '', $file . '/'));
            }
            else if (is_file($file) === true)
            {
              $zip->addFromString(str_replace($source . '/', '', $file), file_get_contents($file));
            }
          }
        }
        else if (is_file($source) === true)
        {
          $zip->addFromString(basename($source), file_get_contents($source));
        }
      }

      return $zip->close();
    }
  }

  return false;
}

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

if ('debug' == @$argv[4])
{
  $cfg['url'] = str_replace('index.php', 'qubit_dev.php', $cfg['url']);
}

if (false == file_exists($directory) || false == is_readable($directory))
{
  fwrite(STDERR, "Given directory could not be found or is not readable.\n");
  exit(1);
}

$file = tempnam('/tmp', 'dip');

if (!zip($directory, $file))
{
  fwrite(STDOUT, "[!!] Error creating zip file.\n");
  exit(1);
}

$cfg['file'] = $file;

fwrite(STDOUT, "[OK] " . $file . " was generated. Sending to ICA-AtoM.\n");

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
  fwrite(STDERR, "[!!] Package could not be deposited:\n");
  fwrite(STDERR, "[!!] " . $e->getMessage() . "\n");

  if (isset($e->data['status']))
  {
    fwrite(STDERR, "[!!] HTTP response status code: " . $e->data['status'] . "\n");
  }

  if (isset($e->data['response']) && 0 < strlen($e->data['response']))
  {
    fwrite(STDERR, "[!!] ----- Server response -----\n");
    fwrite(STDERR, $e->data['response']);
  }
  else
  {
    fwrite(STDERR, "[**] You should switch on the debug mode to get a detailed error report.\n");
  }

  exit(1);
}

if (unlink($file))
{
  fwrite(STDOUT, "[OK] " . $file . " was removed.\n");
}

if ($deposit->sac_status == 201)
{
  fwrite(STDOUT, "[OK] Package uploaded successfully.\n");
  exit(0);
}
else
{
  fwrite(STDERR, "[!!] Package could not be uploaded (" . $deposit->sac_status . ").\n");
  fwrite(STDERR, "[!!] You should switch on the debug mode to get a detailed error report.\n");
  exit(1);
}
