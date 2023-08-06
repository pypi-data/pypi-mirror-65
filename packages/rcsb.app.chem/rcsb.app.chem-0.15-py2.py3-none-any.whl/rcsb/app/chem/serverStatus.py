##
# File: serverStatus.py
# Date: 14-Mar-2020
#
##
# pylint: skip-file
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"

import logging
from fastapi import APIRouter

logger = logging.getLogger("app_chem")

router = APIRouter()


@router.get("/status", tags=["status"])
def serverStatus():
    return {"msg": "Sevice is up!"}


@router.get("/", tags=["status"])
def rootServerStatus():
    return {"msg": "Sevice is up!"}
