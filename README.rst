MatMat 
======

Intelligent Web Application for practicing mathematics.

Deployment
----------

Currently the only supported database is MySQL.
Here are the steps necessary for creating a database:

.. code-block:: sql

    CREATE DATABASE matmat; 
    GRANT ALL PRIVILEGES ON matmat.* TO 'matmat'@'localhost' IDENTIFIED BY 'poklop'; 
    FLUSH PRIVILEGES; 
    ALTER DATABASE matmat CHARACTER SET utf8 COLLATE utf8_general_ci;

Note that the last line is important to avoid UTF-8 errors.
