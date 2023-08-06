from enum import Enum


class ExecutionType(Enum):
    PROCESS_PER_ROW = "process_per_row"
    PROCESS_ONCE = "process_once"

    @staticmethod
    def get_all_types():
        return [exec_type.name for exec_type in ExecutionType]

