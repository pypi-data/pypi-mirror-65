#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from chime_frb_api.core import API
from chime_frb_api.modules import (
    swarm,
    events,
    parameters,
    calibration,
    metrics,
    mimic,
    sources,
)

log = logging.getLogger(__name__)


class FRBMaster(object):
    """
    CHIME/FRB Master Backend
    """

    def __init__(self, **kwargs):
        # Instantiate FRB/Master Core API
        self.API = API(**kwargs)
        # Instantiate FRB Master Components
        self.swarm = swarm.Swarm(self.API)
        self.events = events.Events(self.API)
        self.parameters = parameters.Parameters(self.API)
        self.calibration = calibration.Calibration(self.API)
        self.metrics = metrics.Metrics(self.API)
        self.mimic = mimic.Mimic(self.API)
        self.sources = sources.Sources(self.API)

    def version(self) -> str:
        # Version of the frb-master API client is connected to
        try:
            return self.API.get("/version").get("version", "unknown")
        except Exception as e:
            log.warning(e)
            return "unknown"
