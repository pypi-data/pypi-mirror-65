import logging
from os import path
from typing import Dict, List, TYPE_CHECKING

from ..common import chdir
from ..process_assignment.process_assignment import process_assignment
from ..process_assignment.record_result import RecordResult
from ..process_assignment.warning_unmerged_branches import find_unmerged_branches
from ..toolkit import global_vars

if TYPE_CHECKING:
    from ..specs.spec import Spec
    from ..student.student_result import StudentResult


def record_student(*,
                   student: 'StudentResult',
                   specs: Dict[str, 'Spec'],
                   assignments: List[str],
                   basedir: str,
                   interact: bool,
                   skip_web_compile: bool):
    results = []
    if assignments:
        directory = student.name if not global_vars.CI else '.'
        with chdir(directory):
            find_unmerged_branches(student)

            for _, spec in specs.items():
                if spec.id in assignments:
                    logging.debug("Recording {}'s {}".format(student.name, spec.id))
                    if path.exists(spec.folder):
                        with chdir(spec.folder):
                            assignment_result = process_assignment(student=student,
                                                                   spec=spec,
                                                                   basedir=basedir,
                                                                   interact=interact,
                                                                   skip_web_compile=skip_web_compile)
                    else:
                        assignment_result = RecordResult(spec_id=spec.id,
                                                         student=student.name)
                        assignment_result.warnings.assignment_missing = True

                    results.append(assignment_result)

    student.results = results
