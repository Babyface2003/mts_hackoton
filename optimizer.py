from typing import Dict
from models import AllocationState
from allocation_manager import AllocationManager


class Optimizer:
    def __init__(self, state: AllocationState, manager: AllocationManager):
        self.state = state
        self.manager = manager

    def calculate_utilization(self, host: str) -> float:
        used_cpu = sum(self.state.vms[vm]['cpu'] for vm in self.state.allocations.get(host, []))
        used_ram = sum(self.state.vms[vm]['ram'] for vm in self.state.allocations.get(host, []))
        host_spec = self.state.hosts[host]
        cpu_util = used_cpu / host_spec['cpu'] if host_spec['cpu'] > 0 else 0
        ram_util = used_ram / host_spec['ram'] if host_spec['ram'] > 0 else 0
        return (cpu_util + ram_util) / 2

    def optimize(self) -> Dict[str, Dict]:
        migrations = {}
        sorted_hosts = sorted(
            self.state.hosts.keys(),
            key=lambda h: self.calculate_utilization(h),
            reverse=True
        )

        for src_host in sorted_hosts:
            vms_on_host = sorted(
                self.state.allocations.get(src_host, []),
                key=lambda vm: self.state.vms[vm]['cpu'] + self.state.vms[vm]['ram'],
                reverse=True
            )

            for vm in vms_on_host:
                best_host = None
                best_utilization = float('inf')

                for dst_host in self.state.hosts:
                    if dst_host == src_host:
                        continue

                    if self.manager.can_place_vm(dst_host, vm):
                        current_util = self.calculate_utilization(dst_host)
                        if current_util < best_utilization:
                            best_host = dst_host
                            best_utilization = current_util

                if best_host and best_utilization < 0.8:
                    self.manager.remove_vm(vm)
                    self.manager.place_vm(best_host, vm)
                    migrations[vm] = {'from': src_host, 'to': best_host}
                    break

        return migrations