import requests

from .errors import DSQueryError, DSTargetError


URLS = {
    "starfinder": "https://sfdatasource.com",
    "pathfinder": "https://pfdatasource.com",
}

class Client():
    def __init__(self, api_name):
        """ Base client for datasource_python, encapsulates all necessary logic

        Parameters
        ----------
        api_name : string
            Name of API, used to get the corresponding URL for the API
        """
        self.url = self.get_url(api_name)

    def __getattribute__(self, name):
        """ Extends default attribute checker to create queries for non-existing attributes.

        Parameters
        ----------
        name
            Attribute being requested
        
        Raises
        ------
        DSQueryError
            Will throw an error if an attribute is accessed that doesn't exist and doesn't successfully fetch data.
        """
        try:
            return object.__getattribute__(self, name)
        except:
            object.__setattr__(self, name, Type(name, self.url))
            return object.__getattribute__(self, name)

    def get_url(self, api_name):
        """ Object used for new/unknown attributes of Client

        Parameters
        ----------
        api_name : string
            Name of API, used to get the corresponding URL for the API

        Raises
        ------
        DSTargetError
            Gives verbose error message if api_name does not have corresponding URL
        """
        if api_name in URLS:
            return URLS[api_name]
        else:
            raise DSTargetError(f"The target '{api_name}' provided in Client initialization is not in available target names:\n {list(URLS.keys())}")

class Type():
    def __init__(self, name, url):
        """ Object used for new/unknown attributes of Client

        Parameters
        ----------
        name : string
            Name of new attribute. Used as table/type in GraphQL query.
        url : string
            Url passed in from Client object
        """
        self.name = name
        self.url = url
        self.args = []
    
    def get(self, fields):
        """ Get entries for the specified type, limited by arguments if set

        Parameters
        ----------
        fields : list
            Fields to include from the returned objects. `Client.xyz.get(['name'])` will be transformed into `{ query { xyz { name } } }`. Required field. 

        Raises
        ------
        DSQueryError
            This error is raised if any errors are returned by GraphQL.

        Returns
        -------
        response : dict
            Object returned by requests.post
        """
        if self.args:
            self.args = " ".join([
                (key + ":" + f'"{value}"') if type(value) is str else f"{key}:{value}"
                for key, value in self.args.items()
            ])
        self.table = self.name + f"({self.args})" if self.args else self.name
        query = "{" + self.table + "{" + ' '.join(fields) + "} }"
        response = requests.post(self.url, json={'query': query})
        self.args = []
        if "errors" in response.json():
            raise DSQueryError(response)
        return response

    def set_arguments(self, arguments):
        """ Prepare for upcoming 'get' call to use these arguments

        Parameters
        ----------
        arguments : dict
            Key-value pairs to use in refining a query.

        Returns
        -------
        bool
            Specifies whether arguments were provided, for use in debugging
        """
        self.args = arguments
        return True if self.args else False
