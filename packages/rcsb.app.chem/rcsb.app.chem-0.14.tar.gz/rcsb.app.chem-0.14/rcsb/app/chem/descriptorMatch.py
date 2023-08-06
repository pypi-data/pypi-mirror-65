##
# File: descriptionMatch.py
# Date: 13-Mar-2020 jdw
#
##
# pylint: skip-file

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"

import logging

from collections import namedtuple, OrderedDict
from enum import Enum
from typing import List
from fastapi import APIRouter, Path, Query
from fastapi.encoders import jsonable_encoder

# pylint disable=no-name-in-module
from pydantic import BaseModel, Field

from rcsb.utils.chem.ChemCompSearchWrapper import ChemCompSearchWrapper

logger = logging.getLogger("app_chem")

MatchResults = namedtuple("MatchResults", "ccId oeMol searchType matchOpts screenType fpType fpScore oeIdx formula", defaults=(None,) * 9)

router = APIRouter()


class DescriptorType(str, Enum):
    smiles = "SMILES"
    inchi = "InChI"


class DescriptorMatchType(str, Enum):
    relaxed = "graph-relaxed"
    relaxedStereo = "graph-relaxed-stereo"
    strict = "graph-strict"
    fuzzy = "fingerprint-similarity"


class DescriptorQuery(BaseModel):
    query: str = Field(None, title="Descriptor string", description="SMILES or InChI chemical descriptor", example="c1ccc(cc1)[C@@H](C(=O)O)N")
    # generator: str = Field(None, title="Descriptor generator", description="Program or agent generating the descriptor", example="OpenEye Toolkit")
    matchType: DescriptorMatchType = Field(
        None, title="Query match type", description="Qualitative graph matching comparison or fingerprint comparison criteria", example="graph-relaxed"
    )


class DescriptorQueryResult(BaseModel):
    query: str = Field(None, title="Descriptor query string", description="SMILES or InChI chemical descriptor", example="c1ccc(cc1)[C@@H](C(=O)O)N")
    descriptorType: DescriptorType = Field(None, title="Descriptor type", description="SMILES or InChI", example="SMILES")
    matchedIdList: List[str] = Field(None, title="Matched identifiers", description="Matched chemical component or BIRD identifier codes", example=["004"])


@router.get("/{descriptorType}", response_model=DescriptorQueryResult, tags=["descriptor"])
def matchGetQuery(
    query: str = Query(None, title="Descriptor string", description="SMILES or InChI chemical descriptor", example="c1ccc(cc1)[C@@H](C(=O)O)N"),
    matchType: DescriptorMatchType = Query(
        "graph-relaxed", title="Query match type", description="Qualitative graph matching or fingerprint comparison criteria", example="graph-relaxed"
    ),
    descriptorType: DescriptorType = Path(..., title="Descriptor type", description="Type of chemical descriptor (SMILES or InChI)", example="SMILES"),
):
    matchType = matchType if matchType else "graph-relaxed"
    logger.info("Got %r %r %r", descriptorType, query, matchType)
    # ---
    ccsw = ChemCompSearchWrapper()
    retStatus, ssL, fpL = ccsw.matchByDescriptor(query, descriptorType, matchOpts=matchType)
    logger.info("Results (%r) ssL (%d) fpL (%d)", retStatus, len(ssL), len(fpL))
    if matchType in ["fingerprint-similarity"]:
        rL = list(OrderedDict.fromkeys([mr.ccId.split("|")[0] for mr in fpL]))
        # rL = [mr.ccId for mr in fpL]
    else:
        # rL = [mr.ccId for mr in ssL]
        rL = list(OrderedDict.fromkeys([mr.ccId.split("|")[0] for mr in ssL]))
    # ---
    return {"query": query, "descriptorType": descriptorType, "matchedIdList": rL}


@router.post("/{descriptorType}", response_model=DescriptorQueryResult, tags=["descriptor"])
def matchPostQuery(
    query: DescriptorQuery, descriptorType: DescriptorType = Path(..., title="Descriptor type", description="Type of chemical descriptor (SMILES or InChI)", example="SMILES"),
):

    logger.info("Got %r %r", descriptorType, query)
    qD = jsonable_encoder(query)
    logger.debug("qD %r", qD)
    matchType = qD["matchType"] if "matchType" in qD and qD["matchType"] else "graph-relaxed"
    # ---
    ccsw = ChemCompSearchWrapper()
    retStatus, ssL, fpL = ccsw.matchByDescriptor(qD["query"], descriptorType, matchOpts=matchType)
    logger.info("Results (%r) ssL (%d) fpL (%d)", retStatus, len(ssL), len(fpL))
    #
    if matchType in ["fingerprint-similarity"]:
        # filter remove search index extensions
        # rL = [mr.ccId for mr in fpL]
        rL = list(OrderedDict.fromkeys([mr.ccId.split("|")[0] for mr in fpL]))
    else:
        rL = list(OrderedDict.fromkeys([mr.ccId.split("|")[0] for mr in ssL]))
    # ---
    return {"query": query.query, "descriptorType": descriptorType, "matchedIdList": rL}
