#!/usr/bin/env php
<?php

# This file is part of Archivematica.
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Archivematica is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.

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
  'obo' => null);

if ('cli' !== php_sapi_name())
{
  die("This script was designed for php-cli.\n");
}

if (5 > $argc || in_array(@$argv[1], array('--help', '-help', '-h', '-?')))
{
   die(<<<content
    Usage:
      $argv[0] TYPE URL USERNAME PASSWORD DIRECTORY

    Example:
      $argv[0] attached http://localhost/ica-atom/index.php/;sword/deposit/foo-bar-fonds foo@bar.com 12345 ~/foobarDIP

content
  );
}

$cfg['url'] = $argv[1];
$cfg['username'] = $argv[2];
$cfg['password'] = $argv[3];

$directory = $argv[4];

if ('debug' == @$argv[5])
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
    require(dirname(__FILE__).'/HttpResponseCodes.class.php');
    fwrite(STDERR, '[!!] HTTP response status code: ' . HttpResponseCodes::getMessage($e->data['status']) . "\n");

    if ('404' == $e->data['status'])
    {
      fwrite(STDERR, "[!!] Please check that qtSwordPlugin is enabled.\n");
      fwrite(STDERR, "[!!] Please check that the next resource exists: " . $cfg['url'] . "\n");
    }
    else if ('401' == $e->data['status'])
    {
      fwrite(STDERR, "[!!] Bad username/password?\n");
    }
  }

  if (isset($e->data['response']) && 0 < strlen($e->data['response']))
  {
    fwrite(STDERR, "[!!] ----- Server response -----\n");
    fwrite(STDERR, $e->data['response']);
  }
  else
  {
    fwrite(STDERR, "[!!] You should switch on the debug mode to get a detailed error report.\n");
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
  fwrite(STDOUT, "[OK] URL: " . $deposit->sac_content_src . "\n");
  exit(0);
}
// For some reason php-curl returns 302 when
// the server response status code is 202 (Accepted)
// but only if including Content-Location header
else if ($deposit->sac_status == 202 || $deposit->sac_status == 302)
{
  fwrite(STDOUT, "[OK] Package uploaded successfully.\n");
  fwrite(STDOUT, "[OK] The job was accepted by the server.\n");
  fwrite(STDOUT, "[OK] URL: " . $deposit->sac_content_src . "\n");
  exit(0);
}
else
{
  fwrite(STDERR, "[!!] Package could not be uploaded (" . $deposit->sac_status . ").\n");
  fwrite(STDERR, "[!!] You should switch on the debug mode to get a detailed error report.\n");
  exit(1);
}
