Troubleshooting
===============

.. _setup_environment:

Set up a clean environment
--------------------------

Many things can cause a broken environment. You might be on an unsupported version of Python.
Another package might be installed that has a name or version conflict.
Often, the best way to guarantee a correct environment is with ``virtualenv``, like:

.. code-block:: shell

    # Install pip if it is not available:
    $ which pip || curl https://bootstrap.pypa.io/get-pip.py | python

    # Install virtualenv if it is not available:
    $ which virtualenv || pip install --upgrade virtualenv

    # *If* the above command displays an error, you can try installing as root:
    $ sudo pip install virtualenv

    # Create a virtual environment:
    $ virtualenv -p python3 ~/.venv-py3

    # Activate your new virtual environment:
    $ source ~/.venv-py3/bin/activate

    # With virtualenv active, make sure you have the latest packaging tools
    $ pip install --upgrade pip setuptools

    # Now we can install platon.py...
    $ pip install --upgrade web3

.. NOTE:: Remember that each new terminal session requires you to reactivate your virtualenv, like:
    ``$ source ~/.venv-py3/bin/activate``


.. _instance_troubleshooting:

Why can't I use a particular function?
--------------------------------------

Note that a platon.py instance must be configured before you can use most of its capabilities.
One symptom of not configuring the instance first is an error that looks something like this:
``AttributeError: type object 'Web3' has no attribute 'platon'``.

To properly configure your platon.py instance, specify which provider you're using to connect to the
Platon network. An example configuration, if you're connecting to a locally run node, might be:

.. code-block:: python

    >>> from platon import Web3
    >>> w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

    # now `w3` is available to use:
    >>> w3.isConnected()
    True
    >>> w3.platon.send_transaction(...)

Refer to the :ref:`providers` documentation for further help with configuration.


.. _use_metamask_accounts:

Why isn't my web3 instance connecting to the network?
-----------------------------------------------------
You can check that your instance is connected via the ``isConnected`` method:

.. code-block:: python

    >>> w3.isConnected()
    False

There's a variety of explanations for why you may see ``False`` here. If you're
running a local node, such as Pnode, double-check that you've indeed started the
binary and that you've started it from the intended directory - particularly if
you've specified a relative path to its ipc file.

If that does not address your issue, it's probable that you still have a
Provider configuration issue. There are several options for configuring
a Provider, detailed :ref:`here<providers>`.

How do I use my MetaMask accounts from platon.py?
-----------------------------------------------
Often you don't need to do this, just make a new account in platon.py,
and transfer funds from your MetaMask account into it. But if you must...

Export your private key from MetaMask, and use
the local private key tools in platon.py to sign and send transactions.

See `how to export your private key
<https://platon.stackexchange.com/questions/33053/what-is-a-private-key-in-an-platon-wallet-like-metamask-and-how-do-i-find-it>`_
and :ref:`platon-account`.

.. _faucets:

How do I get ether for my test network?
---------------------------------------

Test networks usually have something called a "faucet" to
help get test ether to people who want to use it. The faucet
simply sends you test ether when you visit a web page, or ping a chat bot, etc.

Each test network has its own version of test ether, so each one
must maintain its own faucet. If you're not sure which test network
to use, see :ref:`choosing_network`

Faucet mechanisms tend to come and go, so if any information here is
out of date, try the `Platon Stackexchange <https://platon.stackexchange.com/>`_.
Here are some links to testnet ether instructions (in no particular order):

- `Kovan <https://github.com/kovan-testnet/faucet>`_
- `Rinkeby <https://www.rinkeby.io/#faucet>`_
- `Ropsten <https://www.reddit.com/r/ethdev/comments/72ltwj/the_new_if_you_need_some_ropsten_testnet_ethers/>`_


.. _account_troubleshooting:

Why can't I create an account?
------------------------------

If you're seeing the error ``The method personal_newAccount does not exist/is not available``,
you may be trying to create an account while connected to a remote node provider, like Infura.
As a matter of security, remote nodes cannot create accounts.

If you are in fact running a local node, make sure that it's properly configured to accept ``personal``
methods. For Pnode, that looks something like: ``--http.api personal,platon,<etc>`` or ``--ws.api personal,platon,<etc>``
depending on your configuration. Note that the IPC configuration is most secure and includes the ``personal``
API by default.

In general, your options for accounts are:

- Run a node (e.g., Pnode) locally, connect to it via the local port, then use the ``personal`` API.
- Import a keystore file for an account and :ref:`extract the private key<extract_node_pk>`.
- Create an account via the :ref:`platon-account <platon-account>` API, e.g., ``new_acct = w3.platon.account.create()``.
- Use an external service (e.g., MyCrypto) to generate a new account, then securely import its private key.

.. Warning:: Don't store real value in an account until you are familiar with security best practices.
   If you lose your private key, you lose your account!

Making Platon JSON-RPC API access faster
------------------------------------------

Your Platon node JSON-RPC API might be slow when fetching multiple and large requests, especially when running batch jobs. Here are some tips for how to speed up your platon.py application.

- Run your client locally, e.g., `Go Platon <https://github.com/platonnetwork/platon-go>`_ or `TurboPnode <https://github.com/ledgerwatch/turbo-node>`_. The network latency and speed are the major limiting factors for fast API access.

- Use IPC communication instead of HTTP/WebSockets. See :ref:`choosing_provider`.

- Use an optimised JSON decoder. A future iteration of platon.py may change the default decoder or provide an API to configure one, but for now, you may patch the provider class to use `ujson <https://pypi.org/project/ujson/>`_.

.. code-block:: python

    """JSON-RPC decoding optimised for platon.py"""

    from typing import cast

    import ujson

    from platon.providers import JSONBaseProvider
    from platon.types import RPCResponse


    def _fast_decode_rpc_response(raw_response: bytes) -> RPCResponse:
        decoded = ujson.loads(raw_response)
        return cast(RPCResponse, decoded)


    def patch_provider(provider: JSONBaseProvider):
        """Monkey-patch platon.py provider for faster JSON decoding.

        Call this on your provider after construction.

        This greatly improves JSON-RPC API access speeds, when fetching
        multiple and large responses.
        """
        provider.decode_rpc_response = _fast_decode_rpc_response
