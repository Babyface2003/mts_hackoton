from typing import TypedDict, Dict, List

class HostSpec(TypedDict):
    cpu: int
    ram: int

class VMSpec(TypedDict):
    cpu: int
    ram: int

class AllocationState:
    def __init__(self):
        self.hosts: Dict[str, HostSpec] = {}
        self.vms: Dict[str, VMSpec] = {}
        self.allocations: Dict[str, List[str]] = {}
        self.vm_host_map: Dict[str, str] = {}