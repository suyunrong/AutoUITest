from execute import driver_action
import platform
from datetime import datetime

def run_test(driver, testcase_list):
    for script_dict in testcase_list:
        page_oper = script_dict.get('page_oper')
        driver_func = getattr(driver_action, page_oper)
        driver_func(driver, **script_dict)


def get_summary(result):
    """ get summary from test result
    """
    summary = {
        "success": result.wasSuccessful(),
        "stat": {
            'testsRun': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped),
            'expectedFailures': len(result.expectedFailures),
            'unexpectedSuccesses': len(result.unexpectedSuccesses)
        },
        "platform": get_platform()
    }
    summary["stat"]["successes"] = summary["stat"]["testsRun"] \
        - summary["stat"]["failures"] \
        - summary["stat"]["errors"] \
        - summary["stat"]["skipped"] \
        - summary["stat"]["expectedFailures"] \
        - summary["stat"]["unexpectedSuccesses"]

    if getattr(result, "records", None):
        summary["time"] = {
            'start_at': datetime.fromtimestamp(result.start_at),
            'duration': result.duration
        }
        summary["records"] = result.records
    else:
        summary["records"] = []

    return summary


def get_platform():
    return {
        "python_version": "{} {}".format(
            platform.python_implementation(),
            platform.python_version()
        ),
        "platform": platform.platform()
    }