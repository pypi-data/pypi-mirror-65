import datetime
import platform
import sys

_VERSION = "1.6.5"


class col:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Logger:
    """A class for logging data to a file"""

    def __init__(self, filename="log.txt", context="", verbose=True, autosave=False):
        """
        Example for a log in file 'filename' (verbose == False):

        [context] [12:34:56] Hello World!

        (verbose == True)

        [DEBUG] [context] [12:34:56] Hello World!
        """
        self.autosave = autosave
        self.filename = filename
        self._lines = []
        self.context = context
        self.verbose = verbose
        self._progress: Progress = None

    @property
    def autosave(self):
        return self._is_autosave

    @property
    def context(self):
        return self._context

    @property
    def verbose(self):
        return self._verbose

    @autosave.setter
    def autosave(self, autosave):
        if type(autosave) == bool:
            self._is_autosave = autosave
        else:
            raise TypeError("Expected autosave to be of type bool.")

    @context.setter
    def context(self, context):
        """specifies context which will be added to all outputs (file & terminal) in front."""
        if type(context) != str:
            raise TypeError("Context expected to be of type str.")
        if not "[" in context and not "] " in context:
            if (context == "" or context == " "):
                self._context = ""
            else:
                self._context = f"[{context}] "
        else:
            self._context = context

    @verbose.setter
    def verbose(self, set_verbose: bool):
        """set verbose mode to 'set_verbose'."""
        if type(set_verbose) == bool:
            self._verbose = set_verbose
        else:
            raise TypeError("'verbose' argument expected to be of type bool")

    # TODO: v1.7.0: remove function (deprecated since 1.6.0)
    def set_context(self, context):
        """Deprecated. Use the property 'context' instead."""
        self.context = context
        try:
            raise DeprecationWarning(
                "set_context() deprecated. Use the property 'context' instead.")
        except Exception as e:
            self.handle_exception(e)

    # TODO: v1.7.0: remove function (deprecated since 1.6.0)
    def set_verbose(self, verbose, is_verbose):
        """Deprecated. Use the property 'verbose' instead."""
        self.verbose = verbose
        if is_verbose:
            if verbose:
                self.debug("Fileloghelper now in verbose mode.")
            else:
                self.debug("Fileloghelper no longer in verbose mode.")
        try:
            raise DeprecationWarning(
                "set_verbose() deprecated. Use the property 'verbose' instead.")
        except Exception as e:
            self.handle_exception(e)

    def save(self):
        """save file under default/at declaration specified filename."""
        self.file = open(self.filename, "w")
        self.file.writelines(self._lines)
        self.file.close()

    def _autosave(self):
        """Automatically saves log if autosave mode is on"""
        if self.autosave:
            self.save()

    def get_version(self, long=False):
        if long:
            return f"This is fileloghelper on v{_VERSION}!"
        else:
            return _VERSION

    def _timestamp_now_(self, extra_long=False):
        now = datetime.datetime.now()
        ex = "%H:%M:%S"
        if extra_long:
            ex += ":%f"
        string = "[" + now.strftime(ex) + "]"
        return string

    def _get_success_(self, text, display=True):
        if display:
            print(col.OKGREEN + self._context + self._timestamp_now_() +
                  col.ENDC + " " + text)
        string = self._context
        string += "[SUCCESS] " if self._verbose else ""
        string += self._timestamp_now_() + " " + text
        return string

    def _get_debug_(self, text, display=False):
        if display:
            print(col.OKBLUE + self._context + self._timestamp_now_() +
                  col.ENDC + " " + text)
        string = self._context
        string += "[DEBUG] " if self._verbose else ""
        string += self._timestamp_now_() + " " + text
        return string

    def _get_warning_(self, text, display=True, extra_context=""):
        if display:
            print(col.WARNING + self._context + self._timestamp_now_() +
                  col.ENDC + " " + extra_context + ": " + text)
        string = self._context
        string += "[" + extra_context + "] " if self._verbose else ""
        string += self._timestamp_now_() + " " + text
        return string

    def _get_error_(self, text, display=True, extra_context=""):
        if display:
            print(col.FAIL + self._context + self._timestamp_now_() +
                  col.ENDC + " " + extra_context + ": " + text)
        string = self._context
        string += "[" + extra_context + "] " if self._verbose else ""
        string += self._timestamp_now_() + " " + text
        return string

    def _get_plain_(self, text, display=True, extra_long=False):
        string = self._context + self._timestamp_now_(extra_long) + " " + text
        if display:
            print(string)
        return string

    def success(self, text, display=True):
        string = self._get_success_(str(text), display)
        string += "\n"
        self._lines.append(string)
        self._autosave()

    def debug(self, text, display=False):
        string = self._get_debug_(str(text), display)
        string += "\n"
        self._lines.append(string)
        self._autosave()

    def warning(self, text, display=True, extra_context=""):
        """writes text to file and optionally with yellow indication in console(if display == True)"""
        string = self._get_warning_(
            str(text), display, extra_context)
        string += "\n"
        self._lines.append(string)
        self._autosave()

    def error(self, text, display=True, extra_context=""):
        """writes text to file and optionally with red indication in console (if display==True)"""
        string = self._get_error_(
            str(text), display, extra_context)
        string += "\n"
        self._lines.append(string)
        self._autosave()

    def show_warning(self, warning, display=True):
        tb = sys.exc_info()[2]
        self.warning(f"({tb.tb_frame.f_code.co_filename}, line {tb.tb_lineno}) {str(warning)}", display,
                     extra_context=type(warning).__name__)

    def show_error(self, error, display=True):
        tb = sys.exc_info()[2]
        self.error(f"({tb.tb_frame.f_code.co_filename}, line {tb.tb_lineno}) {str(error)}", display,
                   extra_context=type(error).__name__)

    def handle_exception(self, exception):
        """pass any subclass/instance of 'Exception' and this will handle printing it appropriately formatted"""
        if issubclass(exception.__class__, Warning):
            self.show_warning(exception)
        else:
            self.show_error(exception)

    def plain(self, text, display=False, extra_long=False, very_plain=False):
        """write and optionally display text to file. extra_long specifies time format (12:34:56; 12:34:56:123456). If very_plain==True, no timestamp or somethings similar will be outputted"""
        if not very_plain:
            string = self._get_plain_(str(text), display, extra_long)
        else:
            string = text
            if display:
                print(string)
        string += "\n"
        self._lines.append(string)
        self._autosave()

    def header(self, sys_stat=False, date=False, description="", display=0, fileloghelper_version=True, program_version=None):
        """
        Display options:

        0 (standard): nothing, only log

        1: only description

        2: only date

        3: only sys_stat

        4: description & date

        5: description & sys_stat

        6: date & sys_stat

        7: description, date and sys_stat

        8: as 7, but with fileloghelper version

        9: as 7, but also prints program_version

        If 'fileloghelper_version', also the version of fileloghelper will be displayed/logged
        'program_version' can be specified to be displayed/logged as well

        Note: 'version' is the same as 'fileloghelper_version' but is depreciated and will be removed in a future release (1.6)
        """
        now = datetime.datetime.now()
        systemstrin = f"{platform.system()} ({platform.machine()})\n{platform.version()}\n{platform.platform()}\n{platform.processor()}\n"
        date_string = f"{now.strftime('%A, %d %B %Y %H:%M:%S')}\n"
        # yes, this is kinda awfull, but it does the job reliably
        if display == 0:
            if sys_stat:
                self.plain(systemstrin, very_plain=True, display=False)
            if date:
                self.plain(date_string, very_plain=True, display=False)
            if description:
                self.plain(description, very_plain=True, display=False)
        elif display == 1:
            if sys_stat:
                self.plain(systemstrin, very_plain=True, display=False)
            if date:
                self.plain(date_string, very_plain=True, display=False)
            if description:
                self.plain(description, very_plain=True, display=True)
        elif display == 2:
            if sys_stat:
                self.plain(systemstrin, very_plain=True, display=False)
            if date:
                self.plain(date_string, very_plain=True, display=True)
            if description:
                self.plain(description, very_plain=True, display=False)
        elif display == 3:
            if sys_stat:
                self.plain(systemstrin, very_plain=True, display=True)
            if date:
                self.plain(date_string, very_plain=True, display=False)
            if description:
                self.plain(description, very_plain=True, display=False)
        elif display == 4:
            if sys_stat:
                self.plain(systemstrin, very_plain=True, display=False)
            if date:
                self.plain(date_string, very_plain=True, display=True)
            if description:
                self.plain(description, very_plain=True, display=True)
        elif display == 5:
            if sys_stat:
                self.plain(systemstrin, very_plain=True, display=True)
            if date:
                self.plain(date_string, very_plain=True, display=False)
            if description:
                self.plain(description, very_plain=True, display=True)
        elif display == 6:
            if sys_stat:
                self.plain(systemstrin, very_plain=True, display=True)
            if date:
                self.plain(date_string, very_plain=True, display=True)
            if description:
                self.plain(description, very_plain=True, display=False)
        elif display == 7:
            if sys_stat:
                self.plain(systemstrin, very_plain=True, display=True)
            if date:
                self.plain(date_string, very_plain=True, display=True)
            if description:
                self.plain(description, very_plain=True, display=True)
        if program_version != None:
            if type(program_version) == str or type(program_version) == int or type(program_version) == float:
                self.plain("version: " + str(program_version),
                           very_plain=True, display=display == 9)
            else:
                raise TypeError(
                    "program_version not of type (str, int, float)")
        if fileloghelper_version:
            self.plain(self.get_version(long=True),
                       very_plain=True, display=display == 8)

    def clear(self):
        """Clear all lines"""
        self._lines = []
        self._autosave()

    def progress(self, x=0, description="", startx=0, maxx=100, mode="=", scale=10):
        """Show a progress bar. Depending on x"""
        if not self._progress == None:
            self._progress.update(x)
        else:
            self._progress = Progress(
                description=description, startx=startx, maxx=maxx, mode=mode, scale=scale, logger=self)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.save()


class Progress:
    """internal class"""

    def __init__(self, description: str, startx: int, maxx: int, mode: str, scale: int, logger: Logger):
        self.x = startx
        self.description = description
        self.maxx = maxx
        self.decimal = round(startx / maxx, 2)
        self.mode = mode
        self.scale = scale
        self.update(startx)
        self.logger = logger
        if description != "":
            self.name = f"{description} "
        else:
            self.name = ""
        self.logger.debug(f"progress {self.name}started")

    def update(self, x):
        self.x = x
        self.decimal = round(x / self.maxx, 3)
        self._backline()
        print(self._get_str(), end="", flush=True)
        if self.decimal == 1.0:
            self._backline()
            print("\033[92m" + self._get_str() + "\033[0m", end="", flush=True)
            print()
            self.logger.success(f"progress {self.name}finished", False)

    def _get_str(self):
        if self.description != "":
            str_ = self.description + ": " + self._percent()
        else:
            str_ = self._percent()
        if self.mode == "#":
            return str_ + self._hashtag()
        else:
            return str_ + self._equal_sign()

    def _hashtag(self):
        inner = "#" * int(self.decimal * self.scale) + " " * \
            int((1 - self.decimal) * self.scale)
        return "<" + inner + ">"

    def _equal_sign(self):
        inner = "=" * int(self.decimal * self.scale - 1) + ">" + " " * \
            int((1 - self.decimal) * self.scale)
        return "[" + inner + "]"

    def _backline(self):
        print("\r", end="")

    def _percent(self):
        return str(round(self.decimal * 100, 3)) + "% "


class VariableObserver:
    """Wrapper for variable with functions pre/post changing the variables's value and (for int and float) a history (a list, e.g. to plot with matplotlib)"""

    def __init__(self, value, pre_change_func=lambda x: x, post_change_func=lambda x: x):
        self.value = value
        self.pre_change_func = pre_change_func
        self.post_change_func = post_change_func
        if type(value) == int or type(value) == float:
            self._history = [self.value]
        else:
            self._history = None

    def set_value(self, new_value):
        self.pre_change_func(self.value)
        self.value = new_value
        if self._history != None:
            self._history.append(new_value)
        self.post_change_func(self.value)

    def get_history(self):
        return self._history

    def __nonzero__(self):
        return self.value.__nonzero__()

    def __repr__(self):
        return self.value.__repr__()

    def __bool__(self):
        return self.value.__bool__()


class VarSet:
    """A set/collection of VariableObservers to make it easier to print larger streams of data to the console"""

    def __init__(self, variables: dict):
        self.variables: dict[str, VariableObserver] = {}
        for name in variables:
            self.variables[name] = VariableObserver(variables[name])

    def set(self, varname, value):
        self.variables[varname].set_value(value)

    @property
    def head(self):
        return list(self.variables.keys())

    @property
    def keys(self):
        return self.head

    @property
    def values(self):
        return list(self.variables.values())

    def print_head(self, delimiter=","):
        s = ""
        for i in self.head:
            s += i + delimiter + " "
        print(s[:-2])

    def print_variables(self):
        out = ""
        for key in self.variables:
            out += str(self.variables[key].value) + ", "
        out = out[:-2]
        print("\r", end="")
        print(out, end="", flush=True)

    def get_history(self):
        histories = {}
        for varname in self.variables:
            histories[varname] = self.variables[varname].get_history()
        return histories

    def history_to_csv(self, filename: str):
        csv = ""
        for k in self.variables.keys():
            csv += str(k) + ","
        csv = csv[:-1] + "\n"
        l = []
        for k, v in self.variables.items():
            l.append(v.get_history())
        values = zip(*l)
        for row in values:
            for v in row:
                csv += str(v) + ","
            csv = csv[:-1]
            csv += "\n"
        with open(filename, "w") as f:
            f.write(csv)

    def __nonzero__(self):
        return self.variables

    def __bool__(self):
        return len(self.variables) > 0

    def __repr__(self):
        return self.variables

    def __getitem__(self, item):
        return self.variables[item]

    def __str__(self):
        return str(self.variables)
