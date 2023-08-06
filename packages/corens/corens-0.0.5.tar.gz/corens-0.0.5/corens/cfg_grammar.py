import fs
from fs.opener import open_fs
import fs.errors
from corens.ns import *
from textx import metamodel_from_str
import textx.exceptions

BUND_GRAMMAR = """
Model: s*=ScriptDef i*=ImportDef n*=NameSpaceDef;

NameSpaceDef:
    "[" name=NSID ">"
        ns*=NameSpaceDef
        statements*=AssignmentDef
    ";;"
;

ImportDef:
    "(" name=STRING ">"
;

ScriptDef:
    words *= ScriptElements
;

AssignmentDef:
    DirectAssignmentDef | ReverseAssignmentDef
;

DirectAssignmentDef:
    name=NameDef  DirectDataAssignmentOp data=DataDef
;

ReverseAssignmentDef:
    data=DataDef  ReverseDataAssignmentOp name=NameDef
;

NameDef:
    ID
;

NSID:
    "/" ID ("/" ID)*
;

DirectDataAssignmentOp:
    "is" | "<-"
;

ReverseDataAssignmentOp:
    "->" | "as"
;

REF_TYPE:
    "`" data=DataDef
;

LAMBDA_TYPE:
    "(" words+= DataDef ")"
;

CURRY_TYPE:
    "(" name=CODEWORD_REF_TYPE "." value=DataDef ")"
;

CODEWORD_REF_TYPE:
    ID | NSID |  LAMBDA_TYPE | CURRY_TYPE | SPECIAL_TYPE
;

DO_EXECUTE_TYPE:
    ";"
;

PRELIMENARY_EXECUTE_TYPE:
    ":" name=CODEWORD_REF_TYPE
;



SPECIAL_TYPE:
    /[-+*<>=!?%^~]+/
;

LIST_TYPE:
    "[" data *= DataDef[","] "]"
;

KV_TYPE:
    name=NameDef ":" data=DataDef
;

DICT_TYPE:
    "{" data *= KV_TYPE[","] "}"
;


DataDef:
    ID | BASETYPE | LIST_TYPE | DICT_TYPE | REF_TYPE | LAMBDA_TYPE | CURRY_TYPE | PRELIMENARY_EXECUTE_TYPE | DO_EXECUTE_TYPE | NSID | SPECIAL_TYPE
;

ScriptDef:
    DataDef
;

Comment:
    /\\/\\*(.|\n)*?\\*\\//
;
"""

def nsCfgGrammar(ns):
    bund_mm = metamodel_from_str(BUND_GRAMMAR, memoization=True, )
    V(ns, "/sys/metamodel", bund_mm)
    return ns

def nsCfgLoad(ns, cfg):
    model = V(ns, "/sys/metamodel").model_from_str(cfg)
    return nsCfgVM(ns, model)

def nsCfgVMData(ns, data):
    if isinstance(data, int) is True:
        return data
    elif isinstance(data, float) is True:
        return data
    elif isinstance(data, str) is True:
        return data
    elif data.__class__.__name__ == 'LIST_TYPE':
        out = []
        for d in data.data:
            out.append(nsCfgVMData(ns, d))
        return out
    elif data.__class__.__name__ == 'DICT_TYPE':
        out = {}
        for d in data.data:
            key = d.name
            _data = nsCfgVMData(ns, d.data)
            out[key] = _data
        return out
    else:
        pass
    return None

def nsCfgVMNS(ns, _n):
    namespace = nsMkdir(ns, _n.name)
    for a in _n.statements:
        name = a.name
        data = nsCfgVMData(ns, a.data)
        path = "{}/{}".format(_n.name, name)
        nsSet(ns, path, data)
    for n in _n.ns:
        ns = nsCfgVMNS(ns, n)
    return ns

def nsCfgVM(ns, model):
    for inc in model.i:
        data = nsCfgFSLoad(ns, inc.name)
    for n in model.n:
        ns = nsCfgVMNS(ns, n)
    return ns

def _nsCfgFSLoad(ns, name):
    lfs = nsGet(ns, "/config/cfg.fs")
    for _fs in lfs:
        try:
            f = _fs.open(name)
            return f.read()
        except fs.errors.ResourceNotFound:
            continue
    return None

def nsCfgFSLoad(ns, name):
    data = _nsCfgFSLoad(ns, name)
    if data is None:
        nsGlobalError(ns, "Configuration file {} not found".format(name))
        return ns
    nsCfgLoad(ns, data)
    return ns
