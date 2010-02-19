<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>Archivematica Dashboard</title>
    <?php include_http_metas() ?>
    <?php include_metas() ?>
    <?php include_title() ?>
    <link rel="shortcut icon" href="/favicon.ico" />
    <?php include_stylesheets() ?>
    <?php include_javascripts() ?>
  </head>
  <body>
    <div id="header">
      <?php echo link_to(image_tag('logo.png'), @homepage) ?>
    </div>

    <div id="main-menu">
      <ul>
        <li><?php echo link_to('Receive SIP', array('module' => 'sip', 'action' => 'index')) ?></li>
        <li><?php echo link_to('Prepare AIP', array('module' => 'aip', 'action' => 'index')) ?></li>
        <li>Store AIP</li>
        <li>Prepare DIP</li>
        <li>Monitor Preservation</li>
      </ul>
    <div>
    

    <div id="content">
      <?php echo $sf_content ?>
    </div>

    <div id="footer">
    </div>
  </body>
</html>
