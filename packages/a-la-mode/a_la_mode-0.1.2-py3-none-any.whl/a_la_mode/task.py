import hashlib
import bencode
from dataclasses import dataclass, field
from toolz.dicttoolz import assoc, dissoc, merge
from toolz.itertoolz import first, drop
from toposort import toposort, toposort_flatten
import pprint
pp = pprint.PrettyPrinter(indent=2).pprint


def sha(s):
    return hashlib.sha256(s).hexdigest()


@dataclass
class Dag:
    spec: dict
    tasks: list = field(default_factory=list)

    @classmethod
    def load(cls, file):
        with file.open('rb') as f:
            return bencode.bdecode(f.read())

    def __getattr__(self, name):
        for task in self.tasks:
            if task.name == name:
                return task
        super().__getattribute__(name)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def task(self, name, spec):
        task = Task(name, spec)
        self.tasks.append(task)
        return task

    def bencode(self):
        return bencode.bencode(self.encode())

    def save(self, filename):
        with open(filename, 'wb') as f:
            bencode.bwrite(self.encode(), f)

    def encode(self):
        tasks = {task.name: encode_task(task) for task in self.tasks}
        sortable = {name: set(spec['inputs'].keys()) for name, spec in tasks.items()}
        result = {
            "tasks": tasks,
            "meta": self.spec,
            "toposort_flatten": list(toposort_flatten(sortable)),
            "toposort": [list(results) for results in toposort(sortable)]
        }
        return result


@dataclass(frozen=True)
class Task:
    name: str
    spec: dict
    deps: list = field(default_factory=list)
    inputs: dict = field(default_factory=dict)

    def add_dep(self, other_task):
        self.deps.append(other_task)


def encode_task(task):
    if not task.deps:
        result = assoc(task.spec, 'inputs', task.inputs)
        output_sha = sha(bencode.bencode(result))
        return assoc(result, 'output', output_sha)
    first_dep = task.deps[0]
    inputs = assoc(task.inputs, first_dep.name,
                   encode_task(first_dep)['output'])
    return encode_task(Task(task.name, task.spec, task.deps[1:], inputs))
