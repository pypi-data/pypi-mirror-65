=========
Spade-BDI
=========


.. image:: https://img.shields.io/pypi/v/spade_bdi.svg
        :target: https://pypi.python.org/pypi/spade_bdi

.. image:: https://img.shields.io/travis/sfp932705/spade_bdi.svg
        :target: https://travis-ci.org/javipalanca/spade_bdi

.. image:: https://readthedocs.org/projects/spade-bdi/badge/?version=latest
        :target: https://spade-bdi.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



Create hybrid agents with a BDI layer for the SPADE MAS Platform.


* Free software: GNU General Public License v3
* Documentation: https://spade-bdi.readthedocs.io. (to be done)


Features
--------

* Create agents that parse and execute an ASL file written in AgentSpeak.
* Supports Agentspeak-like BDI behaviours.
* Add custom actions and functions.
* Send TELL, UNTELL and ACHIEVE  KQML performatives.
* Create agents that parse and execute an ASL file written in AgentSpeak.

Examples
--------

basic.py::

    import argparse
    from spade_bdi.bdi import BDIAgent

    parser = argparse.ArgumentParser(description='spade bdi master-server example')
    parser.add_argument('--server', type=str, default="localhost", help='XMPP server address.')
    parser.add_argument('--password', type=str, default="bdipassword", help='XMPP password for the agents.')
    args = parser.parse_args()

    a = BDIAgent("BasicAgent@" + args.server, args.password, "basic.asl")
    a.start()

    a.bdi.set_belief("car", "blue", "big")
    a.bdi.print_beliefs()

    print(a.bdi.get_belief("car"))
    a.bdi.print_beliefs()

    a.bdi.remove_belief("car", 'blue', "big")
    a.bdi.print_beliefs()

    print(a.bdi.get_beliefs())
    a.bdi.set_belief("car", 'yellow')


basic.asl::

    !start.

    +!start <-
        +car(red);
        .a_function(3,W);
        .print("w =", W);
        literal_function(red,Y);
        .print("Y =", Y);
        .custom_action(8);
        +truck(blue).

    +car(Color)
     <- .print("The car is ",Color).


Examples
--------

basic.py::

    import argparse
    from spade_bdi.bdi import BDIAgent

    parser = argparse.ArgumentParser(description='spade bdi master-server example')
    parser.add_argument('--server', type=str, default="localhost", help='XMPP server address.')
    parser.add_argument('--password', type=str, default="bdipassword", help='XMPP password for the agents.')
    args = parser.parse_args()

    a = BDIAgent("BasicAgent@" + args.server, args.password, "basic.asl")
    a.start()

    a.bdi.set_belief("car", "blue", "big")
    a.bdi.print_beliefs()

    print(a.bdi.get_belief("car"))
    a.bdi.print_beliefs()
    
    a.bdi.remove_belief("car", 'blue', "big")
    a.bdi.print_beliefs()
    
    print(a.bdi.get_beliefs())
    a.bdi.set_belief("car", 'yellow')


basic.asl::

    !start.

    +!start <-
        +car(red);
        .a_function(3,W);
        .print("w =", W);
        literal_function(red,Y);
        .print("Y =", Y);
        .custom_action(8);
        +truck(blue).

    +car(Color) 
     <- .print("The car is ",Color).


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
