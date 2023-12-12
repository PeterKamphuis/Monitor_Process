
# -*- coding: future_fstrings -*-
import traceback
import threading
import warnings


class Monitor:
    def __init__(self,Configuration):
        initialize_monitor(self,Configuration)
    def __str__(self):
        return f"Currently monitoring pid: {self.pid}, spid: {self.sid} and the programs {self.programs}"
     
    def start_monitoring(self):
        while not self.stop:
            try:
                do_monitor(self)
               
            except Exception as e:
                #We do not care if something goes wrong once. We don't want the monitor to crash
                #but we would like to know what went wrong
                traceback.print_exception(type(e),e,e.__traceback__)
                pass
            time.sleep(self.interval)

    def add_process(self, pid = None, spid = None, program = None):
        if pid != None:
            self.pid.append(pid)
        if spid != None:
            self.spid.append(spid)
        if program != None:
            self.program.append(program)
            
    def pause(self):
        self.stop = True
        with open(self.file,'a') as resources:
            resources.write(f"Pausing {self} at {time_str}")
    
    def restart(self):
        self.stop = True
        with open(self.file,'a') as resources:
            resources.write(f"Restart {self} at {time_str}")
        self.start_monitoring()
      
    def remove_process(self, pid = None, spid = None, program = None):
        if pid != None:
            self.pid.remove(pid)
        if spid != None:
            self.spid.remove(spid)
        if program != None:
            self.program.remove(program)
            

    def stop_monitoring(self):
        self.stop = True
        loads = {'Time':[]}
        keys=['SCPU','SRAM','FCPU','FRAM']
        for key in keys:
            loads[key]  = []
        with open(self.file) as file:
            lines = file.readlines()
        startdate = 0
        #load data from file into dictionary
        for line in lines:
            line = line.split()
            if line[0] == '#':
                continue
            else:
                date = extract_date(f"{line[0]} {line[1]}")
            if startdate == 0:
                startdate = date
            diff = date - startdate
            time = diff.total_seconds()/(3600.)
            loads['Time'].append(time)
            for i,key in enumerate(keys):
                loads[key].append(float(line[int(2+i)]))
        #Plot the parameters
        try:
            mpl_fm.fontManager.addfont(self.font_file)
            font_name = mpl_fm.FontProperties(fname=self.font_file).get_name()
        except FileNotFoundError:
            font_name = 'DejaVu Sans'
        labelfont = {'family': font_name,
                 'weight': 'normal',
                 'size': 4}
        fig, ax1 = plt.subplots(figsize = (8,6))
        fig.subplots_adjust(left = 0.1, right = 0.9, bottom = 0.3, top = 0.7)
        ax1.plot(loads['Time'],loads['SRAM'],'b--',lw=0.5,alpha=0.5, label='System RAM')
        ax1.plot(loads['Time'],loads['FRAM'],'b-',lw=0.5,alpha=1.0, label='pyFAT RAM')
        ax1.set_ylim(0,np.max(np.array(loads['SRAM']+loads['FRAM'],dtype=float))*1.1)
        ax1.set_ylabel('RAM (Gb) ', color='b')
        ax1.tick_params(axis='y', labelcolor='b')
        ax1.set_xlabel('Run Duration (h)', color='k',zorder=5)
        ax2 = ax1.twinx()
        ax2.plot(loads['Time'],loads['SCPU'],'r--',lw=0.5,alpha=0.5, label='System CPU')
        ax2.plot(loads['Time'],loads['FCPU'],'r-',lw=0.5,alpha=1.0, label='pyFAT CPU')
        ax2.set_ylim(0,np.max(np.array(loads['SCPU']+loads['FCPU'],dtype=float))*1.1)
        ax2.set_ylabel('CPUs (%)',color='r')
        ax2.tick_params(axis='y', labelcolor='r')
        fig.savefig(self.plot_name)
        plt.close()



def initialize_monitor(self,cfg):
    self.stop = False

    self.pid = os.getpid()
    self.main_pyFAT = psu.Process(self.pid)
    self.user = self.main_pyFAT.username()
    self.python = self.main_pyFAT.name()
    self.tirific = Configuration['TIRIFIC']
    self.font_file = Configuration['FONT_FILE']
    self.sofia = Configuration['SOFIA2']
    self.file = f"{Configuration['MAIN_DIRECTORY']}FAT_Resources_Used.txt"
    self.plot_name= f"{Configuration['MAIN_DIRECTORY']}pyFAT_Resources_Monitor.pdf"
    self.cpus= psu.cpu_count()
    with open(self.file,'w') as resources:
        resources.write("# This file contains an estimate of all resources used for a pyFAT run. \n")
        resources.write(f"# {'Time':20s} {'Sys CPU':>10s} {'Sys RAM':>10s} {'FAT CPU':>10s} {'FAT RAM':>10s} \n")
        resources.write(f"# {'YYYY-MM-DD hh:mm:ss':20s} {'%':>10s} {'Gb':>10s} {'%':>10s} {'Gb':>10s} \n")
    self.interval = 60 # amount of second when to do new monitor        


def do_monitor(self):
    self.sys_cpu= psu.cpu_percent(interval=1)
    self.sys_ram= psu.virtual_memory().used/2**30.
    self.CPU = 0.
    self.RAM = 0.
    for proc in psu.process_iter():
        if proc.username() == self.user \
            and proc.status() == 'running'\
            and (proc.name() == self.python or\
                proc.name() == self.tirific or\
                proc.name() == self.sofia or\
                proc.name() == 'python3'):
            try:
                self.CPU += proc.cpu_percent(interval=0.5)/self.cpus
                self.RAM += (proc.memory_info()[0])/2**30.
            except:
                pass
    #file.write(f"{datetime.now()} CPU = {CPU} % Mem = {mem} Gb for TiRiFiC \n")
    with open(self.file,'a') as resources:
        resources.write(f"{time_str()} {self.sys_cpu:>10.1f} {self.sys_ram:>10.2f} {self.CPU:>10.1f} {self.RAM:>10.2f} \n")

def time_str():
    return f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S'):20s}"