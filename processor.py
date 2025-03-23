import copy
from typing import Dict, Any, List
from models import AllocationState
from allocation_manager import AllocationManager
from optimizer import Optimizer

class RoundProcessor:
    def __init__(self):
        self.state = AllocationState()
        self.manager = AllocationManager(self.state)
        self.optimizer = Optimizer(self.state, self.manager)

    def process_round(self, input_data: Dict[str, Any], is_first_round: bool) -> Dict[str, Any]:
        prev_vm_host = copy.deepcopy(self.state.vm_host_map)
        migrations = {}

        if is_first_round:
            self._process_first_round(input_data)
        else:
            self._process_diff(input_data.get('diff', {}))

        failures = self._place_new_vms(input_data, is_first_round)
        migrations.update(self.optimizer.optimize())
        return self._build_output(prev_vm_host, failures, migrations)

    def _process_first_round(self, input_data: Dict[str, Any]):
        self.state.hosts = input_data['hosts']
        self.state.vms = input_data['virtual_machines']
        self.state.allocations = {}
        self.state.vm_host_map = {}

    def _process_diff(self, diff: Dict[str, Any]):
        for vm in diff.get('remove', {}).get('virtual_machines', []):
            self.state.vms.pop(vm, None)
            self.manager.remove_vm(vm)

        added_vms = diff.get('add', {}).get('virtual_machines', {})
        for vm, spec in added_vms.items():
            self.state.vms[vm] = spec

    def _place_new_vms(self, input_data, is_first_round: bool) -> List[str]:
        failures = []
        if is_first_round:
            for vm in input_data['virtual_machines']:
                if not self.manager.try_place_vm(vm):
                    failures.append(vm)
        else:
            added_vms = input_data.get('diff', {}).get('add', {}).get('virtual_machines', {})
            for vm in added_vms:
                if not self.manager.try_place_vm(vm):
                    failures.append(vm)
        return failures

    def _build_output(self, prev_vm_host: Dict, failures: List[str], migrations: Dict) -> Dict:
        current_migrations = {
            vm: {'from': prev, 'to': self.state.vm_host_map[vm]}
            for vm, prev in prev_vm_host.items()
            if vm in self.state.vm_host_map and prev != self.state.vm_host_map[vm]
        }

        filtered_migrations = {
            vm: migration
            for vm, migration in migrations.items()
            if vm not in prev_vm_host or prev_vm_host[vm] != migration["to"]
        }

        current_migrations.update(filtered_migrations)

        return {
            "$schema": "resources/output.schema.json",
            "allocations": {h: sorted(vms) for h, vms in self.state.allocations.items() if vms},
            "allocation_failures": sorted(failures),
            "migrations": current_migrations
        }