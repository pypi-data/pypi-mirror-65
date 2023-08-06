aiojson
=======

Simple json template verifier for ``aiohttp``

Usage
-----

Simple example:

.. code-block:: python

    from aiohttp import JsonTemplate


    @JsonTemplate({
        "messages": [{
            "id": int,
            "text": str
    }])
    async def received_message(request, validated_data):
        pass
