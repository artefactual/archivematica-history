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

function zip($source, $destination)
{
  if (extension_loaded('zip') === true)
  {
    if (file_exists($source) === true)
    {
      $zip = new ZipArchive();

      if ($zip->open($destination, ZIPARCHIVE::CREATE) === true)
      {
        $source = realpath($source);
        $parent = dirname($source);

        if (is_dir($source) === true)
        {
          $files = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($source), RecursiveIteratorIterator::SELF_FIRST);

          foreach ($files as $file)
          {
            $file = realpath($file);

            if ($parent == $file)
            {
              continue;
            }

            if (is_dir($file) === true)
            {
              $zip->addEmptyDir(str_replace($source . DIRECTORY_SEPARATOR, '', $file . DIRECTORY_SEPARATOR));
            }
            else if (is_file($file) === true)
            {
              $zip->addFromString(str_replace($source . DIRECTORY_SEPARATOR, '', $file), file_get_contents($file));
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

function help()
{
  $script_name = pathinfo($argv[0]);
  $script_name = $script_name['basename'] ? $script_name['basename'] : 'upload-qubit';

  die(<<<content

    Usage:

      1: [attached] The directory will be zipped and sent within the deposit request

         Syntax:
         \033[0;32m  $script_name attached URL USERNAME PASSWORD DIRECTORY UUID [debug]  \033[0m

         Example:
           $ $script_name attached \
             http://.../index.php/sword/deposit/foo-bar-fonds \
             foo@bar.com 12345 \
             /tmp/foobarDIP

      2. [referenced] Deposit by reference, the location is referenced

         Syntax:
         \033[0;32m  $script_name referenced URL USERNAME PASSWORD DIRECTORY UUID [debug]  \033[0m

         Example:
           $ $script_name referenced \
             http://.../index.php/sword/deposit/foo-bar-fonds \
             foo@bar.com 12345 \
             /tmp/foobarDIP

      3. [referenced-rsync] Deposit by reference, the directory will be sent using rsync

         Syntax:
         \033[0;32m  $script_name referenced URL USERNAME PASSWORD DIRECTORY UUID REMOTE_SSH REMOTE_LOCATION [debug]  \033[0m

         Example:
           $ $script_name referenced \
             http://.../index.php/sword/deposit/foo-bar-fonds \
             foo@bar.com 12345 \
             /tmp/foobarDIP \
             "ssh -l username -p 22" \
             "peanut.com:/tmp"


content
  );
}

function updateDatabase($URL = "")
{
  global $cfg;

  // TODO: Load credentials form the Archivematica configuration files or use Python db-wrapper
  $link = mysql_connect('localhost:3306', 'demo', 'demo');

  if (!$link)
  {
    fwrite(STDERR, "[!!] Database update failed: connection could not be established.\n");
    return;
  }

  $db_selected = mysql_select_db('MCP');

  if (!$db_selected)
  {
    fwrite(STDERR, "[!!] Database update failed: database not found.\n");
    return;
  }

  $sql_command = vsprintf('INSERT INTO Accesses (SIPUUID, resource) VALUES ("%s", "%s")', array(
                            mysql_real_escape_string($cfg['uuid']),
                            mysql_real_escape_string($URL)));

  if (!mysql_query($sql_command))
  {
    fwrite(STDERR, "[!!] Database update failed: $sql_command.\n");
    return;
  }
  
  echo mysql_insert_id();

  fwrite(STDIN, "[OK] Database updated!\n");
}

// Defaults
$cfg = array(
  'format' => 'http://purl.org/net/sword-types/METSArchivematicaDIP',
  'contenttype' => 'application/zip',
  'noop' => false,
  'debug' => false,
  'obo' => null);

// CLI check
if ('cli' !== php_sapi_name())
{
  die("This script was designed for php-cli.\n");
}

// Arguments check
if (6 > $argc || in_array(@$argv[1], array('--help', '-help', '-h', '-?')))
{
  help();
}

// Parse arguments
if ('attached' == $argv[1])
{
  $cfg['action'] = 'attached';

  $cfg['url'] = $argv[2];
  $cfg['username'] = $argv[3];
  $cfg['password'] = $argv[4];
  $cfg['directory'] = $argv[5];
  $cfg['uuid'] = $argv[6];
}
else if ('referenced' == $argv[1])
{
  $cfg['action'] = 'referenced';

  $cfg['url'] = $argv[2];
  $cfg['username'] = $argv[3];
  $cfg['password'] = $argv[4];
  $cfg['directory'] = $argv[5];
  $cfg['uuid'] = $argv[6];
}
else if ('referenced-rsync' == $argv[1])
{
  $cfg['action'] = 'referenced-rsync';

  $cfg['url'] = $argv[2];
  $cfg['username'] = $argv[3];
  $cfg['password'] = $argv[4];
  $cfg['directory'] = $argv[5];
  $cfg['uuid'] = $argv[6];
  $cfg['remote_ssh'] = $argv[7];
  $cfg['remote_location'] = $argv[8];
}
else
{
  help();
}

// Debug mode, last parameter and optional
if (in_array($argv[count($argv) - 1], array('debug', '--debug')))
{
  $cfg['url'] = str_replace('index.php', 'qubit_dev.php', $cfg['url']);
  $cfg['debug'] = true;

  // More PHP verbosity
  error_reporting(E_ALL);
}

// Check if directory exist
if (false == file_exists($cfg['directory']) || false == is_readable($cfg['directory']))
{
  fwrite(STDERR, "[!!] Given directory could not be found or is not readable:\n");
  fwrite(STDERR, '[!!] ' . $cfg['directory'] . "\n");
  exit(1);
}

if ('attached' == $cfg['action'])
{
  fwrite(STDOUT, "[OK] Creating ZIP file.\n");

  $file = tempnam('/tmp', 'dip');
  if (!zip($cfg['directory'], $file))
  {
    fwrite(STDERR, "[!!] Error creating zip file.\n");
    exit(1);
  }

  $cfg['file'] = $file;

  fwrite(STDOUT, "[OK] " . $file . " was generated.\n");

  // Call sword-php-library
  fwrite(STDOUT, "[OK] The package will be send within the deposit request.\n");
  $client_deposit_method = 'deposit';
  $client_deposit_parameters = array(
    $cfg['url'],
    $cfg['username'],
    $cfg['password'],
    $cfg['obo'],
    $cfg['file'],
    $cfg['format'],
    $cfg['contenttype'],
    $cfg['noop'],
    $cfg['debug']);
}
else if ('referenced' == $cfg['action'])
{
  // Call sword-php-library
  fwrite(STDOUT, "[OK] The package will be deposited by reference.\n");
  $client_deposit_method = 'depositByReference';
  $client_deposit_parameters = array(
    $cfg['url'],
    $cfg['username'],
    $cfg['password'],
    $cfg['obo'],
    'file://' . $cfg['directory'],
    $cfg['format'],
    $cfg['contenttype'],
    $cfg['noop'],
    $cfg['debug']);
}
else if ('referenced-rsync' == $cfg['action'])
{
  // Rsync
  // -a =
  //    -r = recursive
  //    -l = recreate symlinks on destination
  //    -p = set same permissions
  //    -t = transfer modification times
  //    -g = set same group owner on destination
  //    -o = set same user owner on destination (if possible, super-user)
  //    --devices = transfer character and block device files (only super-user)
  //    --specials = transfer special files like sockets and fifos
  // -z = compress
  // --partial = our best friend! resume transfers
  $command = sprintf('rsync -r -t -g -o -z --partial -e "%s" %s %s',
                      $cfg['remote_ssh'],
                      $cfg['directory'],
                      $cfg['remote_location']);

  fwrite(STDOUT, '[OK] Running rsync' . ($cfg['debug'] ? ": $command." : '.') . "\n");

  exec($command, $output, $ret);

  if (0 == $ret)
  {
    fwrite(STDOUT, "[OK] Package sent with rsync successfully.\n");
  }
  // Rsync exit code gives us some hope if we retry
  // Exit code 200
  else if (in_array($ret, array(10, 11, 12, 30)))
  {
    fwrite(STDERR, "[!!] Rsync failed, exit code $ret (retry, please).\n");
    exit(200);
  }
  else
  {
    fwrite(STDERR, "[!!] Rsync failed, exit code $ret (see rsync man page, EXIT VALUES).\n");
    exit(1);
  }

  // Call sword-php-library
  fwrite(STDOUT, "[OK] The package will be deposited by reference.\n");
  $client_deposit_method = 'depositByReference';
  $client_deposit_parameters = array(
    $cfg['url'],
    $cfg['username'],
    $cfg['password'],
    $cfg['obo'],
    'file://' . $cfg['directory'],
    $cfg['format'],
    $cfg['contenttype'],
    $cfg['noop'],
    $cfg['debug']);
}

require(dirname(__FILE__).'/HttpResponseCodes.class.php');
require(dirname(__FILE__).'/swordapp-php-library/swordappclient.php');
$client = new SWORDAPPClient();

try
{
  // Call $client->deposit() or $client->depositByReference()
  // based in $client_deposit_method value
  $deposit = call_user_func_array(
    array($client, $client_deposit_method),
    $client_deposit_parameters);
}
catch (Exception $e)
{
  fwrite(STDERR, "[!!] Exception thrown in sword-php-library:\n");
  fwrite(STDERR, "[!!] --> " . $e->getMessage() . "\n");

  fwrite(STDERR, '[!!] HTTP response status code: ' . HttpResponseCodes::getMessage($e->data['status']) . "\n");

  if (in_array($e->data['status'], array(200, 201, 302)))
  {
    fwrite(STDERR, "[!!] However, the package was deposited successfully.\n");
    fwrite(STDERR, "[!!] New deposit URL could not be found.\n");

    updateDatabase();
  }

  if ($cfg['debug'])
  {
    fwrite(STDERR, $e->data['response']);
  }

  exit(1);
}

// If attached we can remove the generated zip safely
if ('attached' == $cfg['action'] && unlink($file))
{
  fwrite(STDOUT, "[OK] " . $file . " was removed.\n");
}

if ($deposit->sac_status == 201)
{
  fwrite(STDOUT, "[OK] Package uploaded successfully (synchronous mode).\n");
  fwrite(STDOUT, "[OK] URL: " . $deposit->sac_content_src . "\n");
  updateDatabase($deposit->sac_content_src);
  exit(0);
}
// For some reason php-curl returns 302 when
// the server response status code is 202 (Accepted)
// but only if including Content-Location header
else if ($deposit->sac_status == 202 || $deposit->sac_status == 302)
{
  fwrite(STDOUT, "[OK] Package uploaded successfully (asynchronous mode).\n");
  fwrite(STDOUT, "[OK] The job was accepted by the server.\n");
  fwrite(STDOUT, "[OK] URL: " . $deposit->sac_content_src . "\n");
  updateDatabase($deposit->sac_content_src);
  exit(0);
}
else if ($deposit->sac_status == 404)
{
  fwrite(STDERR, "[!!] 404 error.\n");
  fwrite(STDERR, "[!!] - Check that qtSwordPlugin is enabled.\n");
  fwrite(STDERR, "[!!] - Exists an information object with slug value 'archivematica'.\n");
}
else
{
  fwrite(STDERR, "[!!] Package could not be uploaded.\n");
  fwrite(STDERR, "[!!] HTTP status message: $deposit->sac_statusmessage.\n");
  fwrite(STDERR, "[!!] Summary: \"$deposit->sac_summary\".\n");
}

if (true == @$cfg['debug'])
{
  var_dump($deposit);
  echo "\n";
}
else
{
  fwrite(STDERR, "[!!] You should switch on the debug mode to get a detailed error report.\n");
}

exit(1);
