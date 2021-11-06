class WWWRedirect:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.build_absolute_uri()

        if 'www.' in path:
            new_path = path.replace('www.', '')
            return redirect(new_path)

        response = self.get_response(request)
        return response
