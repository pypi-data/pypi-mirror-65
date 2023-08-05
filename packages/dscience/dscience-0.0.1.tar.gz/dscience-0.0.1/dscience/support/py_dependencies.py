from __future__ import annotations
import re
from dataclasses import dataclass
from copy import copy
from pathlib import Path
from functools import total_ordering
from typing import Optional, Sequence, Mapping


@total_ordering
@dataclass
class Dep:
	name: str
	version: str
	component: Optional[str]
	source: str

	def to_req_line(self, pad: Optional[int] = None) -> str:
		if pad is None and self.component is None:
			return "{} {}".format(self.name, self.version)
		elif pad is None:
			return "{}[{}] {}".format(self.name, self.component, self.version)
		elif self.component is None:
			return "{} {}".format(self.name.ljust(pad), self.version)
		else:
			return "{} {}".format((self.name+'['+self.component+']').ljust(pad), self.version)

	def to_setup_line(self, pad: Optional[int] = None) -> str:
		name = self.name if pad is None else self.name.ljust(pad)
		if self.name == 'python':
			return "\tpython_requires='{}'".format(self.version)
		elif self.component is None:
			return "\t\t'{} {}'".format(name, self.version)
		else:
			return "\t\t\t'{} {}'".format(name, self.version)

	def to_env_line(self, pad: Optional[int] = None) -> str:
		name = self.name if pad is None else self.name.ljust(pad)
		if self.source == '':
			return "\t- {}{}".format(name, self.version)
		elif self.source == 'pip':
			return "\t\t- {}{}".format(name, self.version)
		else:
			return "\t- {}::{}{}".format(name, self.source, self.version)

	def __lt__(self, other):
		return (
				(self.source, '' if self.component is None else self.component, self.name, self.version)
				< (other.source, '' if other.component is None else other.component, other.name, other.version)
		)


class DepList:
	def __init__(self, lst: Sequence[Dep]):
		self.deps = lst

	def sorted(self) -> DepList:
		return DepList(sorted(self.deps))

	@classmethod
	def from_requirements(cls, lines: Sequence[str]) -> DepList:
		pat = re.compile(r'^([A-Za-z0-9_-]+) *(?:\[([a-z0-9]+)\])? *(.+)$')
		deps = []
		for line in lines:
			if not line.startswith('#') and not line.strip()=='':
				m = pat.fullmatch(line)
				deps.append(Dep(m.group(1), m.group(3), m.group(2), 'pip'))
		return DepList(deps)

	def to_requirements(self) -> Sequence[str]:
		pad = (
			0 if len(self.deps)==0
			else 1 + max(
				len(dep.name)+(0 if dep.component is None else 2+len(dep.component))
				for dep in self.deps
			)
		)
		return [
			'',
			*[dep.to_req_line(pad) for dep in self.deps]
		]

	def to_env(self, name: str, channels: Sequence[str]) -> Sequence[str]:
		if isinstance(channels, str): channels = [channels]
		lst = sorted(self.deps)
		pad = 0 if len(self.deps)==0 else max(len(dep.name) for dep in lst) + 1
		nonpips = [dep for dep in lst if dep.source!='pip']
		pips = [dep for dep in lst if dep.source=='pip']
		lines = []
		last = ''
		for dep in nonpips:
			if dep.component != last:
				if last != '':
					lines.append('\t# @ {}'.format(dep.component))
				last = dep.component
			lines.append(dep.to_env_line(pad))
		lines.append('\tpip:')
		last = ''
		for dep in pips:
			if dep.component != last:
				if last != '':
					lines.append('\t\t# @ {}'.format(dep.component))
				last = dep.component
			lines.append(dep.to_env_line(pad))
		return [
			'',
			'name: ' + str(name),
			'channels:',
			*['\t- '+c for c in channels],
			'dependencies:',
			*lines
		]

	def to_setup(self) -> Sequence[str]:
		lst = copy(self.deps)
		python = [dep for dep in lst if dep.name == 'python']
		if len(python) == 1:
			python = python[0]
		elif len(python) == 0:
			python = None
		else:
			raise ValueError("Multiple python versions?")
		pad = 0 if len(self.deps)==0 else max(len(dep.name) for dep in lst) + 1
		required = [dep for dep in lst if dep.component is None and dep.name != 'python']
		optional = {
			comp: [dep for dep in lst if dep.component==comp]
			for comp in {dep.component for dep in lst if dep.name != 'python' and dep.component is not None}
		}
		reqlines = [dep.to_setup_line(pad)+',' for dep in required]
		if len(reqlines) > 0:
			reqlines[-1] = reqlines[-1].rstrip(',')
		optlines = []
		for comp in optional.keys():
			q = [dep.to_setup_line(pad)+',' for dep in optional[comp]]
			q[-1] = q[-1].rstrip(',')
			optlines.extend([
				"\t\t'{}': [".format(comp),
				*q,
				'\t\t],'
			])
		return [
			'',
			*([] if python is None else ['\t' + python.to_setup_line()+',']),
			'\tinstall_requires=[',
			*reqlines,
			'\t],',
			'\textras_require={',
			*optlines,
			'\t}'
		]


class Deps(DepList):

	@classmethod
	def read_req_file(cls, path: Path):
		lines = Path(path).read_text(encoding='utf8').splitlines()
		return cls.from_requirements(lines).sorted()

	def write_req_file(self, path: Path):
		lines = '\n'.join(self.to_requirements())
		Path(path).write_text(lines, encoding='utf8')

	def write_env_file(self, path: Path, name: str, channels: Sequence[str]):
		lines = '\n'.join(self.to_env(name, channels))
		Path(path).write_text(lines, encoding='utf8')

	def write_setup_file_partial(self, path: Path):
		lines = '\n'.join(self.to_setup())
		Path(path).write_text(lines, encoding='utf8')


__all__ = ['Dep', 'DepList', 'Deps']
