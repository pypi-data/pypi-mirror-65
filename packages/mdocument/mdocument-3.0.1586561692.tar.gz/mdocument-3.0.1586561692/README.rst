MDocument
=========

|pipeline status| |coverage report| |pypi link|

.. |pipeline status| image:: https://git.yurzs.dev/yurzs/mdocument/badges/master/pipeline.svg
   :target: https://git.yurzs.dev/yurzs/mdocument/-/commits/master

.. |coverage report| image:: https://git.yurzs.dev/yurzs/mdocument/badges/master/coverage.svg
   :target: https://git.yurzs.dev/yurzs/mdocument/-/commits/master

.. |pypi link| image:: https://badge.fury.io/py/mdocument.svg
   :target: https://pypi.org/project/mdocument

Simple DRM for async mongo motor client

Usage
-----

.. code-block:: python

    import asyncio

    from mdocument import Document

    import motor.motor_asyncio

    client = motor.motor_asyncio.AsyncIOMotorClient()

    class Comment(Document):
        collection = "comments"
        database = "mdocument"
        client = client


    class Video(Document):
        collection = "videos"
        database = "mdocument"
        client = client

        @Document.related(self_field="_id", other_field="video")
        def comments(self):
            pass

    async def main():
        video = await Video.create(
            title="Test",
        )

        comment1 = await Comment.create(
            video=video._id,
            message="First!",
        )

        comment2 = await Comment.create(
            video=video._id,
            message="Second!"
        )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

Now we can easily access our comments using our related documents

.. code-block:: python

    print(await video.comments)
    [
        Comment(_id=5e7533d55eb6a8c6d24d3cc7, video=5e7533d55eb6a8c6d24d3cc6, message=First!),
        Comment(_id=5e7533d55eb6a8c6d24d3cc8, video=5e7533d55eb6a8c6d24d3cc6, message=Second!)
    ]

Document methods
================

Here is a list of Document basic methods

@related
--------

Decorator for defining related documents. Made for easily managing deletion of related documents.

.. code-block:: python

    def related(self_path, other_path, multiple=True, parent=True):

Example:

.. code-block:: python

    from mdocument import Document, DeleteDocument

    import motor.motor_asyncio

    client = motor.motor_asyncio.AsyncIOMotorClient()

    class Artist(Document):
        collection = "artists"
        database = "mdocument"
        client = client

        @Document.related("Artist._id", "Album._id")
        def albums(self):
            pass

    class Album(Document):
        collection = "albums"
        database = "mdocument"
        client = client

        @Document.related("Album._id", "Song._id")
        def songs(self):
            pass


    class Song(Document):
        collection = "songs"
        database = "abc"
        client = client

As we set our relations. Now we have next actions:
Album deleted -> all songs related to this album are deleted
Author deleted -> all albums related to author are deleted -> each song related to deleted albums deleted

.create
-------
.. code-block:: python

    @classmethod
    async def create(cls, **kwargs):

If you want to create a new document you can do it easily with .create method.
Example:

.. code-block:: python

    import asyncio

    from mdocument import Document

    import motor.motor_asyncio

    client = motor.motor_asyncio.AsyncIOMotorClient()

    class Message(Document):
        collection = "messages"
        database = "mdocument"
        client = client


    loop.run_until_complete(
        Message.create(from_user="admin", text="Test message!")
    )

This will create document in database:

.. code-block:: python

    {
        '_id': ObjectId('5e75373e5eb6a8c6d14d3ccd'),
        'from_user': 'admin',
        'text': "Test message!"
    }

.push_update
------------

Updates document and all @related fields.

.. code-block:: python

    await Message.push_update()

.delete
-------

Deletion of document from database. Based on your set @related rules all related documents will be modified too.

.. code-block:: python

    message = await Message.one(from_user="admin")

    await message.delete()
