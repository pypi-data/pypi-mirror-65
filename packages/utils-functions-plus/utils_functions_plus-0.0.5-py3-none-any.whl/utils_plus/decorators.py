REPORT_ERROR = lambda message: print(message)

NOTIFY = lambda args, result, argument: print(result)


def init_decorator(report_error, notify):
    global REPORT_ERROR, NOTIFY
    REPORT_ERROR = report_error
    NOTIFY = notify


class lazy_property(object):
    def __init__(self, function):
        self.function = function
        functools.update_wrapper(self, function)

    def __get__(self, obj, type_):
        if obj and self.function.__name__ in obj.__dict__:
            return obj.__dict__[self.function.__name__]
        val = __function_execution(lambda: self.function(obj), func_name=self.function.__name__)
        obj.__dict__[self.function.__name__] = val
        return val


def __function_execution(function, func_name="function_execution"):
    try:
        result = function()
    except Exception as exc:
        REPORT_ERROR(func_name, exc)

    return result



def notify_thread(argument):
    def decorator(function):
        def wrapper(*args, **kwargs):
            result = __function_execution(lambda: function(*args, **kwargs), func_name=function.__name__)
            NOTIFY(args, result, argument)
            return result

        return wrapper

    return decorator


def timeout(time_count):
    def decorator(function):
        def wrapper(*args, **kwargs):
            response = {"result": None}

            def process(resp):
                resp["result"] = __function_execution(lambda: function(*args, **kwargs), func_name=function.__name__)

            task = threading.Thread(target=process, args=(response,), daemon=True)
            task.start()
            task.join(time_count)

            return response["result"]

        return wrapper

    return decorator



def measure_time(callback):
    def decorator(function):
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            result = function(*args, **kwargs)
            end_time = datetime.now()
            delta_in_minutes = (end_time - start_time).seconds / 60
            callback("Delta({0})".format(round(delta_in_minutes, 2)))
            return result

        return wrapper

    return decorator




def prevent_exception(function):
    def wrapper(*args, **kwargs):
        result = __function_execution(lambda: function(*args, **kwargs), func_name=function.__name__)
        return result

    return wrapper