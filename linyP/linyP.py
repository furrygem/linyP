import sys
import re

__all__ = ["Progress", "LinyProgresses"]

class Progress:
    # description - array containing initial_message, completion_message, error_message, max_val
    # progress_template - string describes progress display. Syntax: ${MV} - max value, ${CV} - current value, ${ST} - state message, ${INF} - additional information
    # states=None - dictionary containing state names and messages that will be displayed.
    def __init__(self, description, progress_template, states=None, percentage_format="%.2f"):
        """Init new progress display

        Args:
            description (list): description - array containing initial_message, completion_message, error_message, max_val.
            progress_template (tuple): string describes progress display. Syntax: ${MV} - max value, ${CV} - current value, ${ST} - state message, ${INF} - additional information, ${PRC} - Percentage
            states (dict, optional): dictionary containing state names and messages that will be displayed.. Defaults to None.
        """
        self.initial_message, self.completion_message, self.error_message, self.max_val = (
            description
        )  # unpack description
        self.percentage_format = percentage_format
        self.completed = 0  # set progress to 0
        self.isdone = False  # sets to true when progress completes
        self.message = ""
        self.info = ""
        self.percentage = self.percentage_format % 0
        self.availible_states = {
            "initial": self.initial_message,
            "complete": self.completion_message,
            "error": self.error_message,
        }  # declare default availible states
        self.variables_types = {
            "MV": self.max_val,
            "CV": self.completed,
            "ST": self.message,
            "INF": self.info,
            "PRC": self.percentage,
        }  # variables_types - dictionary containing varibles name for progress display substituter
        self.update_state("initial")  # sets state to "initial"
        if states:  # check if user passed additional states as keyword argument
            self.availible_states.update(
                states
            )  # add additional states to default ones
        self.progress_template = progress_template

    # Substitutes required varibles to template
    def progress_substituter(self) -> str:
        """Substitutes required varibles to template

        Returns:
            str: template with substituted varibles to it
        """
        strToSubstitute = re.sub(r"\$\{(MV|CV|ST|INF|PRC)\}", "%s", self.progress_template)
        vals_sequence = tuple(
            [
                self.variables_types.get(val)
                for val in re.findall(r"\$\{(MV|CV|ST|INF|PRC)\}", self.progress_template)
            ]
        )

        return strToSubstitute % vals_sequence

    # newstate - string containing state name
    # update_state checks if newstate presented in availible_states if so
    # update_state changes current progress message by calling setmsg and passing
    # message associated with this state
    def update_state(self, newstate: str):
        """update_state checks if newstate presented in availible_states if so update_state changes current progress message by calling setmsg and passing message associated with this state

        Args:
            newstate (str): string containing state name

        Returns:
            int: 0 if newstate was in availible_states and 1 if not.
        """
        if newstate in self.availible_states:
            self.state = newstate
            self.setmsg(self.availible_states[newstate])
            return 0
        else:
            return 1

    # count - value to add to progress
    # add will return false while max_max val is not reached
    def add(self, count: int) -> bool:
        """Add value to completed value.

        Args:
            count (int): value to add to progress

        Returns:
            bool: Will return False while max_val not reached.
        """
        self.completed += count
        self.update_percentage()
        self.variables_types[
            "CV"
        ] = self.completed  # update completed in varibles dictionary
        if self.completed < self.max_val:
            return False
        self.update_state("complete")
        self.display()
        self.isdone = True
        return True

    # sets progress message directly without using states inteface
    # newmsg - new message string
    def setmsg(self, newmsg: str):
        """Sets progress message directly without using states interface.

        Args:
            newmsg (str): newmsg
        """
        self.message = newmsg
        self.variables_types[
            "ST"
        ] = self.message  # update message in varibles dictionary

    # sets additional information to be displayed
    def setinf(self, newinfo: str) -> None:
        """Sets additional information to be displayed

        Args:
            newinfo (str): new info string.
        """
        self.info = newinfo
        self.variables_types["INF"] = self.info  # update info in varibles dictionary

    def update_percentage(self) -> None:
        """Calculate and update percentage using current progress and max percentage
        """
        current_progress = self.completed
        max_progress = self.max_val
        percentage = current_progress / max_progress * 100
        self.set_percentage(percentage)

    def set_percentage(self, new_percentage: int) -> None:
        """Sets percentage

        Args:
            new_percentage (int): new_percentage
        """
        self.percentage = self.percentage_format % new_percentage + "%"
        self.variables_types[
            "PRC"
        ] = self.percentage
    
    def clear_line(self) -> None:
        """Just cleares current line.
        """
        sys.stdout.write("\033[K")

    # updates progress bar
    def display(self) -> None:
        """updates progress bar
        """
        self.clear_line()
        display = self.progress_substituter()
        sys.stdout.write("\r%s" % (display))
        sys.stdout.flush()



class LinyProgresses:
    # initial_progresses - number of progress display to be spawn at init
    # descriptions - arrays in count of initial_progresses containing initial_message, completion_message, error_message, max_val
    # progress_template - array of strings in count of initial_progresses describes progress display. Syntax: ${MV} - max value, ${CV} - current value, ${ST} - state message, ${INF} - additional information
    # states=None - dictionary containing state names and messages that will be displayed.
    def __init__(
        self, initial_progresses, descriptions, progress_template, states=None
    ):
        """Initialize multiline progress

        Args:
            initial_progresses (int): number of progress display to be spawn at init
            descriptions (list): arrays in count of initial_progresses containing initial_message, completion_message, error_message, max_val
            progress_template (tuple): array of strings in count of initial_progresses describes progress display. Syntax: ${MV} - max value, ${CV} - current value, ${ST} - state message, ${INF} - additional information
            states (dict, optional): dictionary containing state names and messages that will be displayed. Defaults to None.
        """
        self.progresses = []
        self.progress_template = progress_template
        for i in range(initial_progresses):
            self.progresses.append(Progress(descriptions[i], progress_template, states))

    # add new progress with provided description
    def append_progress(self, description):
        """add new progress with provided description

        Args:
            description (list): array containing initial_message, completion_message, error_message, max_val
        """
        self.progresses.append(Progress(description, self.progress_template))

    # move cursor up 1
    def up(self):
        """move cursor up 1
        """
        sys.stdout.write("\x1b[1A")
        sys.stdout.flush()

    # move cursor down 1
    def down(self):
        """move cursor down 1
        """
        sys.stdout.write("\n")
        sys.stdout.flush()

    # set message to progress_id
    def set_msg(self, progress_id, newmsg):
        """set message to progress_id

        Args:
            progress_id (int): progress id
            newmsg (str): new message to set
        """
        self.progresses[progress_id].setmsg(newmsg)

    def update_state(self, progress_id, newstate):
        """update state of progress with progress_id

        Args:
            progress_id (int): progress_id
            newstate (str): new state to set
        """        
        self.progresses[progress_id].update_state(newstate)

    # add value to progress
    def add(self, progress_id, val):
        """Add value to progress with progress id

        Args:
            progress_id (int): progress id
            val (int): value to add
        """        
        self.progresses[progress_id].add(val)

    def setinf(self, progress_id, newinfo):
        """set info of progress with progress id

        Args:
            progress_id (int): progress id
            newinfo (str): new info
        """              
        self.progresses[progress_id].setinf(newinfo)

    # Returns true if all Progresses have isdone set to true
    def checkIfDone(self):
        """Check if all progresses completed

        Returns:
            bool: True if all Progresses have isdone set to true
        """        
        return all([p.isdone for p in self.progresses])

    # display all progresses
    def display_all(self):
        """display all progresses
        """        
        for i in range(len(self.progresses)):
            self.up()
        for i, progress in enumerate(self.progresses):
            self.down()
            progress.display()

    # prepare screen for displaing progresses
    def prepare(self):
        """prepare screen for displaing progresses
        """        
        for i in range(len(self.progresses) - 1):
            self.down()
