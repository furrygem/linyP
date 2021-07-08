# Documentation

## Progress(*self*, description, progress\_template, states=None)
* **description** - array containing initial\_message, completion\_message, error\_message, max\_value
* **progress\_template** - string describing how progress display looks. Syntax: ${MV} - max value, ${CV} - current value, ${ST} - state message, ${INF} - additional information.
* **states** - dictionary containing state names and messages that will be displayed. Default None.

### progress\_substituter(*self*) -> str
Substitutes required variables to template
**Returns**:
template with substituted variabless to it
### update\_state(*self*, newstate: string) -> int
update\_state checks if newstate presented in availible\_states if so update\_state changes current progress message by calling setmsg and passing message associated with this state
* **newstate** - string containing state name
**Returns**:
0 if newstate was in availible_states and 1 if not.

### add(*self*, count: int) -> bool
Add value to completed value. Recalculates and updates percentage.
* **count** - value to add to progress.
**Returns:**
Will return False while max_val not reached.
### setmsg(*self*, newmsg: string)
Sets progress message directly without using states inteface.
* **newmsg** - new message string
### setinf(*self*, newinfo: string)
Sets additional information to be displayed.
* **newinfo** - new info string
### clear\_line(*self*)
Just clears current line.
### display(*self*)
Updated progress bar.

### update_percentage(*self*)
Updates percentage based on current progress and max value.

### set_percentage(*self*, new_percentage: int)
Format and sets new percentage to be displayed
* **new_percentage** - new percentage int

## LinyProgresses(*self*, initial_progress: int, descriptions: int, progress_templates: tuple, states=None)
### append_progress(*self*, description: list)
Add new progress with provided description
* description - array containing initial_message, completion_message, error_message, max_val

### up(*self*)
Move cursor up 1
### down(*self*)
Move cursor down 1

### set_msg(*self*, progress_id: int, newmsg: str)
Set message to progress id.
* **progress_id** - progress id
* **newmsg** - new message to set
### update_state(*self*, progress_id: int, newmsg: str)
Update state of progress with progress_id
* **progress_id** - progress id
* **newstate** - new state to set
### add(*self*, progress_id, val)
Add value to progress with progress_id
### setinf(*self*, progress_id, newinfo)
Set info of progress with progress id
* **progress_id** - progress id
* **newinfo** - new info to set
### checkIfDone(*self*)
Check if all progresses completed
**Returns:**
True if all Progresses have isdone set to true
### display_all(*self*)
Display all progresses
### prepare(*self*)
prepare screen for displaing progresses by moving cursor down *n* lines.
