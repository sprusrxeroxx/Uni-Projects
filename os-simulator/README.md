# BICT112 OS Simulator - Interactive Shell
Minimal operating-system simulator with a project-specific interactive shell.

## Current scope
- Dynamic memory allocation and deallocation
- First-Fit and Best-Fit memory strategies
- Waiting-job admission after memory is freed
- FCFS CPU scheduling
- Round Robin CPU scheduling
- Gantt timeline and waiting/turnaround metrics
- One simulated device: Printer
- Printer busy/free state
- FIFO printer waiting queue
- Process state changes for printer I/O
- External fragmentation detection and allocation failure explanation
- Event log
- Interactive simulator shell using `shlex`

### Run
```text
python main.py
```
The simulator starts with the prompt:
```text
user@sim_os:$
```
Type `help` to see the available simulator commands.
Example commands
```text
add J1 200 5 0
show jobs
show memory
run
end J1
show devices
request printer J1
release printer
set memory best-fit
set cpu rr 2
show gantt
exit
```
The shell is intentionally limited to OS-simulator commands. It is not a general-purpose Linux shell.

Tests
```text
python -m unittest discover -v
```