<?php

class SWORDAPPException extends Exception {

  // Redefine the exception so message isn't optional
  public function __construct($message, $code = 0, Exception $previous = null) {

    if (!is_int($code)) {

      $this->data = $code;

    }

    // make sure everything is assigned properly
    parent::__construct($message, 0, $previous);

  }
}
