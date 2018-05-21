from django.http import HttpResponse


def process(request, **kwargs):
    app = kwargs.pop('app', None)
    fun = kwargs.pop('function', None)
    index = kwargs.pop('id', None)

    if app == 'api':
        app = 'DataServer'
    try:
        app = __import__("%s.views" % app)
        view = getattr(app, 'views')
        fun = getattr(view, fun)

        # 执行view.py中的函数，并获取其返回值
        result = fun(request, index) if index else fun(request)
        print(result)
    except (ImportError, AttributeError):
        return HttpResponse('404 Not Found')

    return result
