from typing import Optional
from models import AllocationState

class AllocationManager:
    def __init__(self, state: AllocationState):
        self.state = state

    def can_place_vm(self, host: str, vm_name: str) -> bool:
        vm = self.state.vms[vm_name]
        used_cpu = sum(self.state.vms[v]['cpu'] for v in self.state.allocations.get(host, []))
        used_ram = sum(self.state.vms[v]['ram'] for v in self.state.allocations.get(host, []))
        return (used_cpu + vm['cpu'] <= self.state.hosts[host]['cpu'] and
                used_ram + vm['ram'] <= self.state.hosts[host]['ram'])

    def place_vm(self, host: str, vm_name: str) -> None:
        self.state.allocations.setdefault(host, []).append(vm_name)
        self.state.vm_host_map[vm_name] = host

    def remove_vm(self, vm_name: str) -> Optional[str]:
        host = self.state.vm_host_map.get(vm_name)
        if host:
            self.state.allocations[host].remove(vm_name)
            if not self.state.allocations[host]:
                del self.state.allocations[host]
            del self.state.vm_host_map[vm_name]
        return host

    def try_place_vm(self, vm_name: str) -> bool:
        sorted_hosts = sorted(
            self.state.hosts.keys(),
            key=lambda h: (
                sum(self.state.vms[v]['cpu'] for v in self.state.allocations.get(h, [])),
                sum(self.state.vms[v]['ram'] for v in self.state.allocations.get(h, []))
            ),
            reverse=False
        )

        for host in sorted_hosts:
            if self.can_place_vm(host, vm_name):
                self.place_vm(host, vm_name)
                return True
        return False