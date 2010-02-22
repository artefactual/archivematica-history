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
      <div id="logo">
        <?php echo link_to(image_tag('logo.png'), @homepage) ?>
      </div>
    </div>

    <?php echo get_component('menu', 'mainMenu') ?>
 
   <div id="page">

    <div id="content">
      <?php echo $sf_content ?>
    </div>

   </div>

    <div id="footer">
    </div>
  </body>
</html>
