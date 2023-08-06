=====
Usage
=====

To use avro-to-python in a project, place your avro avsc files in a target directory. They must be VALID Avro avsc files.

Things to Note
^^^^^^^^^^^^^^

- avro-to-python compiled classes Enforce data types as defined in avro schemas
- Enum types use the python Enum Library
- Compiled python classes should are vanilla python and require no external packages

CLI (without --pip)
^^^^^^^^^^^^^^^^^
To use the cli, here is the available cli commands:

.. code-block:: bash

    avro-to-python [source] [target]
        Options:
            --pip TEXT              make package pip installable using this name
            --author TEXT           author name of the pip installable package
            --package_version TEXT  version of the pip intallable package  [default: 0.1.0]
            --help                  Show this message and exit


The above will compile the avsc files and convert the to python classes found in [path_to_target_directory]

An example of doing this is the following:

.. code-block:: bash

    avro-to-python [path_to_source_avsc_files] [path_to_target_directory]


If you run the above on a valid avro avsc file, you should then be able to import them as you would in the avro idl namespace Here is an example of a single avsc record from the namespace: *name.space* and name: *RecordClass*:

.. code-block:: python

    from name.space import RecordClass

    record = RecordClass({'foo': True, 'bar': 'true', 'baz': 10, 'food': 'CHOCOLATE'})


CLI (with --pip)
^^^^^^^^^^^^^^^^^
You can also choose to make compiled avro packages ***pip installable*** by adding the "--pip" flags. An example of this is the following:
.. highlight::
    avro-to-python [path_to_source_avsc_files] [path_to_target_directory] --pip test_avro

By running this, you should be able to pip install the above package you created from the target directory you specified by running:

.. code-block:: bash

    pip install -e path_to_target_directory

Now that you have the package installed, you can import it by it's package name and namespace. Here is the same example of the same avsc from above, only with a pip package of *test_avro*:

.. code-block:: python

    from test_avro.name.space import RecordClass

    record = RecordClass({'foo': True, 'bar': 'true', 'baz': 10, 'food': 'CHOCOLATE'})


Using avro-to-python in a Script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can also use the reader and writer packages in avro-to-python as you would any other python package. Avro to python is split between a *reader* and *writer* classes. avro-to-python treates namespaces as acyclic trees and uses depth first search to ensure no duplication or namespace collisions on read and write. An example useage is below:

.. code-block:: python

    from avro_to_python.reader import AvscReader
    from avro_to_python.writer import AvroWriter

    # initialize the reader object
    reader = AvscReader(directory='tests/avsc/records/')

    # generate the acyclic tree object
    reader.read()

    # initialize the writer object
    writer = AvroWriter(reader.file_tree, pip='test_pip')

    # compile python files using 'tests/test_records as the namespace root'
    writer.write(root_dir='tests/test_records')
