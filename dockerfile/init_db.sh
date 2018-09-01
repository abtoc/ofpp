#!/bin/bash

mysql -u root -p <<EOF
CREATE DATABASE ofpp DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
GRANT ALL ON ofpp.* TO ofpp@localhost  IDENTIFIED BY '#ofpp#';
FLUSH PRIVILEGES;
EOF
