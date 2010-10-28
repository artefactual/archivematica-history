<div class="menu" id="mainMenu">
<h2 class="element-invisible">Main menu</h2>
      <ul>
        <li><?php echo link_to(__('Ingest SIP'), array('module' => 'sip', 'action' => 'index'), array('class' => $option1)) ?></li>
        <li><?php echo link_to(__('Store AIP'), array('module' => 'aip', 'action' => 'index'), array('class' => $option2)) ?></li>
        <li><?php echo link_to(__('Create DIP'), array('module' => 'dip', 'action' => 'index'), array('class' => $option3)) ?></li>
        <li><?php echo link_to(__('Monitor Preservation'), array('module' => 'preservation', 'action' => 'index'), array('class' => $option4)) ?></li>
      </ul>
</div>
