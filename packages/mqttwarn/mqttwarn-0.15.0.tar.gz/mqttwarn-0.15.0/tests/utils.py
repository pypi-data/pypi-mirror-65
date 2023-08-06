# -*- coding: utf-8 -*-
# (c) 2018 The mqttwarn developers
from builtins import object
import os
from lovely.testlayers.util import asbool
#from lovely.testlayers.mongodb import MongoLayer


class ServerLayerMixin(object):
    """
    A test class mixin for controlling server layers from ``lovely.testlayers``.

    Even when wired, just runs them conditionally as they can be
    easily disabled before runtime using ``export SERVERLAYERS=false``.

    """

    @classmethod
    def setup_serverlayers(cls):

        if asbool(os.environ.get('SERVERLAYERS', True)):

            # Spin up a MongoDB instance
            cls.mongolayer = MongoLayer('mongodb.single', storage_port=27017)
            cls.mongolayer.setUp()

    @classmethod
    def teardown_serverlayers(cls):

        if asbool(os.environ.get('SERVERLAYERS', True)):

            # Shut down the MongoDB instance
            cls.mongolayer.tearDown()

    @classmethod
    def setup_class(cls):
        """Setup any state specific to the execution of the whole class"""

        # Setup base infrastructure (MongoDB, etc.)
        cls.setup_serverlayers()

    @classmethod
    def teardown_class(cls):
        """Teardown any state specific to the execution of the whole class"""

        # Tear down base infrastructure (MongoDB, etc.)
        cls.teardown_serverlayers()
