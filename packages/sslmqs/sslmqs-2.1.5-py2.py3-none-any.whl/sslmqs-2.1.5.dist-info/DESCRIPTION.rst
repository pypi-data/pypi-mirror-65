sslmqs is an abstraction layer above pika, used to connect to RabbitMQ cluster with SSL.

Its purpose is to manage the underlying connection, reconnect when a node of a cluster goes down, and provide the defaults for a situation where downtime should be minimized at all costs.

See also: `my article <https://blog.pelicandd.com/article/151/>`_ explaining the reason for this abstraction layer.

Contributing
------------

The `source code <http://source.pelicandd.com/codebase/sslmqs>`_ is available. The package is distributed under `MIT License <https://opensource.org/licenses/MIT>`_.

If you want to have SVN access to the official repository in order to contribute to the project, contact me at `arseni.mourzenko@pelicandd.com <mailto:arseni.mourzenko@pelicandd.com>`_. If you find it more convinient to clone the source to GitHub, you can do that too.


