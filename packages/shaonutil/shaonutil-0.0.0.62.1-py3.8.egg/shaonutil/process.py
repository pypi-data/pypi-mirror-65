"""Process"""
import psutil
import wmi

import os
import subprocess


"""
To Resolve mysql problems:
go to mysql folder > aria_chk -r
delete araia_log.### files in mysql data folder
change the port=3306 to anything else in line 20,28 in my.ini in mysql data folder
if anything didn't recover then, go to mysqsl/backup, copy everything and go to mysql/data folder , delete everything and past here.
"""

def is_process_exist(process_name):
	pids = []
	processes = list_processes()
	for process_id_,process_name_ in processes:
		if process_name_ == process_name:
			pids.append(process_id_)

	if len(pids) == 0:
		return False
	else:
		return pids

def kill_duplicate_process(process_name,log):
	"""Kill a process if there is more than one instance is running."""
	if log: print("Killing duplicate processes")
	pids = is_process_exist(process_name)
	if len(pids) > 1:
		for pid in pids[1:]:
			killProcess_ByPid(pid)
	


def killProcess_ByAll(PROCNAME): 
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()

def killProcess_ByPid(pid):
    p = psutil.Process(pid)
    p.terminate() 

def list_processes(sort='name',save_file=False,log=False):
    # sort - name/pid
    processes = []

    c = wmi.WMI ()
    
    #print(process.ProcessId, process.Name)
    
    if sort == 'pid':
        processes_pid = {}
        for process in c.Win32_Process():
            processes_pid[process.ProcessId] = process

        for pid in sorted(processes_pid.keys()):
            processes.append(  processes_pid[pid] )

    elif sort == 'name':
        processes_name = {}
        process_strings = []

        for process in c.Win32_Process():
            processes_name[process.Name] = process
            process_strings.append( process.Name )

        process_strings.sort()
        processes = [processes_name[process_name] for process_name in process_strings]

        
    processes_ = []
    if save_file: file_ = open('running_list.txt','w+')
    for process in processes:
        if log: print(process.ProcessId, process.Name)
        processes_.append((process.ProcessId, process.Name))
        if save_file: file_.write(f'{process.ProcessId} {process.Name}\n')

        #process.__dict__
        """

        instance of Win32_Process
        {
            Caption = "System Idle Process";
            CreationClassName = "Win32_Process";
            CreationDate = "20200206235942.060650+360";
            CSCreationClassName = "Win32_ComputerSystem";
            CSName = "DESKTOP-LC92I9N";
            Description = "System Idle Process";
            Handle = "0";
            HandleCount = 0;
            KernelModeTime = "2248239062500";
            Name = "System Idle Process";
            OSCreationClassName = "Win32_OperatingSystem";
            OSName = "Microsoft Windows 10 Pro|C:\\Windows|\\Device\\Harddisk0\\Partition4";
            OtherOperationCount = "0";
            OtherTransferCount = "0";
            PageFaults = 2;
            PageFileUsage = 0;
            ParentProcessId = 0;
            PeakPageFileUsage = 0;
            PeakVirtualSize = "65536";
            PeakWorkingSetSize = 4;
            Priority = 0;
            PrivatePageCount = "0";
            ProcessId = 0;
            QuotaNonPagedPoolUsage = 0;
            QuotaPagedPoolUsage = 0;
            QuotaPeakNonPagedPoolUsage = 0;
            QuotaPeakPagedPoolUsage = 0;
            ReadOperationCount = "0";
            ReadTransferCount = "0";
            SessionId = 0;
            ThreadCount = 4;
            UserModeTime = "0";
            VirtualSize = "65536";
            WindowsVersion = "10.0.14393";
            WorkingSetSize = "4096";
            WriteOperationCount = "0";
            WriteTransferCount = "0";
        };
        """
    if save_file: file_.close()

    return processes_



#myNowMYSQL = MySQL(config._sections['DB_INITIALIZE'])
#{'host': 'localhost', 'user': 'root', 'password': ''}
#myNowMYSQL.config = config._sections['DB_AUTHENTICATION']



def computer_idle_mode():
    kill_running_app_list = ['kited.exe','sublime_text.exe','AoE2DE_s.exe','BattleServer.exe','conhost.exe','python.exe']



def obj_details_dump(obj):
	"""check dump"""
	#obj_details_dump(shaonutil)
	for attr in dir(obj):
	    print("obj.%s = %r" % (attr, getattr(obj, attr)))

#list_processes(log=True)


