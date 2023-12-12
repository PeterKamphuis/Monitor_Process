# -*- coding: future_fstrings -*-
from omegaconf import OmegaConf

from Monitor_Process.functions import Monitor
from Monitor_Process.defaults import defaults


def main(argv):


    help_message = '''
    Use Monitor_Process in this way:

        Monitor_Process input.pid=['pid1','pid2'] process id to monitor

    to monitor a specific process.

        Monitor_Process input.spid=['sid1','sid2'] slurm process id to monitor

    to monitor a specific slurm process.

        Monitor_Process input.programs_to_track= ['program1','program2']

    to monitor a specific program.
    '''
    if '-h' in argv or '--help' in argv:
        print(help_message)
        sys.exit()


    cfg = OmegaConf.structured(defaults)
    input_cfg = OmegaConf.from_cli(argv)
    cfg_input = OmegaConf.merge(cfg,input_cfg)

    try:
        system_monitor = Monitor(cfg_input)
        system_monitor.start_monitoring()
        #t = threading.Thread(target=system_monitor.start_monitoring)
        #t.start()
    except KeyboardInterrupt:
        system_monitor.stop_monitoring(cfg_input.input.file_name)
        #t.join()
        pass
