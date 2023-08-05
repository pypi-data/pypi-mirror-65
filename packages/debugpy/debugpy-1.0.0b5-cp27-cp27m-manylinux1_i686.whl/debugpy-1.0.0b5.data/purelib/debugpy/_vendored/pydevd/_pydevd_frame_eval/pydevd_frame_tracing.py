import sys

from _pydev_bundle import pydev_log
from _pydev_imps._pydev_saved_modules import threading
from _pydevd_bundle.pydevd_comm import get_global_debugger
from pydevd_file_utils import get_abs_path_real_path_and_base_from_frame, NORM_PATHS_AND_BASE_CONTAINER


class DummyTracingHolder:
    dummy_trace_func = None

    def set_trace_func(self, trace_func):
        self.dummy_trace_func = trace_func


dummy_tracing_holder = DummyTracingHolder()


def update_globals_dict(globals_dict):
    new_globals = {'_pydev_stop_at_break': _pydev_stop_at_break}
    globals_dict.update(new_globals)


def _get_line_for_frame(frame):
    # it's absolutely necessary to reset tracing function for frame in order to get the real line number
    tracing_func = frame.f_trace
    frame.f_trace = None
    line = frame.f_lineno
    frame.f_trace = tracing_func
    return line


def _pydev_stop_at_break(line):
    frame = sys._getframe(1)
    t = threading.currentThread()
    if t.additional_info.is_tracing:
        return False

    t.additional_info.is_tracing += 1
    try:
        py_db = get_global_debugger()
        if py_db is None:
            return

        try:
            abs_path_real_path_and_base = NORM_PATHS_AND_BASE_CONTAINER[frame.f_code.co_filename]
        except:
            abs_path_real_path_and_base = get_abs_path_real_path_and_base_from_frame(frame)
        filename = abs_path_real_path_and_base[1]

        try:
            python_breakpoint = py_db.breakpoints[filename][line]
        except:
            # print("Couldn't find breakpoint in the file %s on line %s" % (frame.f_code.co_filename, line))
            # Could be KeyError if line is not there or TypeError if breakpoints_for_file is None.
            # Note: using catch-all exception for performance reasons (if the user adds a breakpoint
            # and then removes it after hitting it once, this method added for the programmatic
            # breakpoint will keep on being called and one of those exceptions will always be raised
            # here).
            return

        if python_breakpoint:
            pydev_log.debug("Suspending at breakpoint in file: {} on line {}".format(frame.f_code.co_filename, line))
            t.additional_info.trace_suspend_type = 'frame_eval'

            pydevd_frame_eval_cython_wrapper = sys.modules['_pydevd_frame_eval.pydevd_frame_eval_cython_wrapper']
            thread_info = pydevd_frame_eval_cython_wrapper.get_thread_info_py()
            if thread_info.thread_trace_func is not None:
                frame.f_trace = thread_info.thread_trace_func
            else:
                frame.f_trace = py_db.get_thread_local_trace_func()

    finally:
        t.additional_info.is_tracing -= 1


def create_pydev_trace_code_wrapper(line):
    pydev_trace_code_wrapper_code = compile('''
# Note: _pydev_stop_at_break must be added to the frame locals.
global _pydev_stop_at_break
_pydev_stop_at_break(%s)
''' % (line,), '<pydev_trace_code>', 'exec')
    return pydev_trace_code_wrapper_code

