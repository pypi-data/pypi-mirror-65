
from apminsight import constants
from apminsight.instrumentation.wrapper import wsgi_wrapper, args_wrapper

module_info = {
    'flask' : [
        {
            constants.class_str : 'Flask',
            constants.method_str : 'wsgi_app',
            constants.wrapper_str : wsgi_wrapper,
            constants.component_str : constants.flask_comp
        },
        {
            constants.class_str : 'Flask',
            constants.method_str : 'add_url_rule',
            constants.wrap_args : 3
        }
    ]
}


