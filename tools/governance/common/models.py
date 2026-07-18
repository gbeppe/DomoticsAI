from dataclasses import dataclass,asdict,field
from typing import Any
@dataclass(frozen=True)
class FileEntry:
 path:str; size_bytes:int; sha256:str; extension:str; category:str; domain:str; is_text:bool; line_count:int|None=None
@dataclass(frozen=True)
class Issue:
 rule_id:str; severity:str; message:str; path:str|None=None; metadata:dict[str,Any]=field(default_factory=dict)
@dataclass
class Inventory:
 root:str; files:list[FileEntry]; issues:list[Issue]; statistics:dict[str,Any]
 def to_dict(self): return asdict(self)
@dataclass
class CommandResult:
 ok:bool; message:str; details:dict[str,Any]=field(default_factory=dict); exit_code:int=0
 def to_dict(self): return asdict(self)
