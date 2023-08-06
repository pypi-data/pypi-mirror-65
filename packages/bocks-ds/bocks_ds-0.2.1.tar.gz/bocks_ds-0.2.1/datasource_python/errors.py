class DSTargetError(Exception):
    """ Incorrect API name passed into Client init
    """
    pass

class DSQueryError(Exception):
    """ Error(s) found in query to API.

    This Error is used instead of passing back full response in order to limit stack trace exposure.

    Contains attributes 'errors' and 'status_code' from response
    """
    def __init__(self, response):
        self.errors = list(error['message'] for error in response.json()['errors'])
        self.status_code = response.status_code
        super().__init__(self.message(response))

    def message(self, response):
        return f"<Response {response.status_code}> {self.get_message()}"

    def get_message(self):
        error_1 = self.errors[0]
        if 'Cannot query field' in error_1 and 'on type "Query"' in error_1:
            substring = error_1.replace('Cannot query field "', '').replace('" on type "Query".', '')
            return f"DataSource did not find table/field '{substring}'."
        else:
            return self.errors
