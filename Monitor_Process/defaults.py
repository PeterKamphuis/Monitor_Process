# -*- coding: future_fstrings -*-

from dataclasses import dataclass, field
from omegaconf import MISSING
from typing import List, Optional


@dataclass
class Input:
    pid: Optional[List] = [None]
    spid: Optional[List] = [None]
    monitor_interval: int = 60
    programs_to_track:  List = field(default_factory=lambda: [
                                    'pyFAT','sofia','tirific'])
    directory: str =  f'{os.getcwd()}/Monitor/'

@dataclass
class Output:
    plot_name: str = 'Monitor_Results'
    file_name: str = 'Usage_Statistics.txt'
  
@dataclass
class defaults:
    ncpu: int = 1
    input: Input = Input()
    output: Output = Output()