import json
import jsonschema
import sys

from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.libraries.OperatingSystem import OperatingSystem
from robot.api.deco import keyword

class ApiLibKeywords(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self.collections = Collections()
        self.builtin = BuiltIn()
        self.operatingsystem = OperatingSystem()

    @keyword
    def response_content_is_valid_json(self, response):
        """
        Verifies that response content is a valid JSON

        ``response`` is either the Response object from RequestsLibrary or
        the DotDict created by RequestsExtension after a request
        """
        if "is_valid_json" in response:
            if not (response["is_valid_json"]):
                raise Exception('Response content is not a valid json')
        else:
            try:
                content = self._to_json(content=response.content)
            except:
                raise Exception('Response content is not a valid json')
    
    @keyword
    def response_content_should_contain_keys(self, content, *keys):
        """          
        Verifies that response content (a valid dictionary) contains certain keys

        ``content`` is the response content dict

        ``*keys`` are the dictionary keys to be found in response content
        """
        if isinstance(content, (str, bytes, bytearray)):
            content = self._to_json(content)
        self.collections.list_should_contain_sub_list(dict(content).keys(), keys)
    
    @keyword
    def response_headers_should_contain_keys(self, headers, *keys):
        """
        Verifies that response headers (a valid dictionary) contains certain keys

        ``headers`` is the response headers dict\n\n``*keys`` are the
        dictionary keys to be found in response headers
        """
        self.response_content_should_contain_keys(headers, *keys)
    
    @keyword
    def each_response_element_should_contain_keys(self, content, *keys):
        """
        Verifies that each element of response content (a valid list) 
        contains certain keys

        ``content`` is the response content dict

        ``*keys`` are the dictionary keys to be found in response content
        """
        content = self._format_list_content(content)
        for item in content:
            self.collections.list_should_contain_sub_list(item.keys(), keys)
    
    @keyword
    def each_response_element_of_key_should_be_contained_in_list(self, content, key, *_list):
        """
        Checks that each element of a ``content``, having a certain ``key``,
        has a value contained in a ``*_list``

        ``content`` is the response content (a valid JSON) that represents a list

        ``key`` is the key whose value is to be obtained, it can be
        specified via dot-notation

        ``*_list`` should contain the retrieved value
        """
        content = self._format_list_content(content)
        key = key.split(".")
        errors = []
        for item in content:
            for k in key:
                item = item.get(k)
            try:
                self.collections.list_should_contain_value(_list, item)
            except Exception as e:
                errors.append(str(e))
        if len(errors) > 0:
            self.builtin.fail("\n".join(errors))
    
    @keyword
    def response_content_should_be_a_list(self, content):
        """
        Verifies that ``content`` (a valid JSON) represents a list
        """
        content = self._format_list_content(content)
    
    @keyword
    def validate_json_with_schema(self, instance, schema):
        """ 
        Verifies that a JSON ``instance`` is validated by a ``schema``
        """
        jsonschema.validate(instance=instance, schema=schema)
    
    @keyword
    def get_request_formatted(self, *args, **kwargs):
        """
        Send a GET request on the session object found using the given alias
        This keyword returns two variables, the first is the request response, 
        the second is a dictionary containing ``headers`` and ``json`` keys
        having as values dotdict objects and a boolean ``is_valid_json``

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the GET request to

        ``params`` url parameters to append to the uri

        ``headers`` a dictionary of headers to use with the request

        ``data`` a dictionary of key-value pairs that will be urlencoded and 
        sent as GET data or binary data that is sent as the raw body content

        ``json`` a value that will be json encoded and sent as GET data if data 
        s not specified

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect
        following is allowed.

        ``timeout`` connection timeout
        """
        requests_library = BuiltIn().get_library_instance('RequestsLibrary')
        response = requests_library.get_request(*args, **kwargs)
        return self._format_response(response)
    
    @keyword
    def post_request_formatted(self, *args, **kwargs):
        """
        Send a POST request on the session object found using the given alias
        This keyword returns two variables, the first is the request response,
        the second is a dictionary containing ``headers`` and ``json`` keys having
        as values dotdict objects and a boolean ``is_valid_json``

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the POST request to

        ``data`` a dictionary of key-value pairs that will be urlencoded and sent
        as POST data or binary data that is sent as the raw body content or passed
        as such for multipart form data if files is also defined

        ``json`` a value that will be json encoded and sent as POST data if 
        files or data is not specified

        ``params`` url parameters to append to the uri

        ``headers`` a dictionary of headers to use with the request

        ``files`` a dictionary of file names containing file data to POST to the server

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.

        ``timeout`` connection timeout
        """
        requests_library = BuiltIn().get_library_instance('RequestsLibrary')
        response = requests_library.post_request(*args, **kwargs)
        return self._format_response(response)
          
    @keyword  
    def put_request_formatted(self, *args, **kwargs):
        """
        Send a PUT request on the session object found using the given alias
        This keyword returns two variables, the first is the request response,
        the second is a dictionary containing ``headers`` and ``json`` keys having
        as values dotdict objects and a boolean ``is_valid_json``

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the PUT request to

        ``data`` a dictionary of key-value pairs that will be urlencoded and sent as
        PUT data or binary data that is sent as the raw body content or passed as such
        for multipart form data if files is also defined

        ``json`` a value that will be json encoded and sent as PUT data if files or data
        is not specified

        ``params`` url parameters to append to the uri

        ``headers`` a dictionary of headers to use with the request

        ``files`` a dictionary of file names containing file data to PUT to the server

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.

        ``timeout`` connection timeout
        """
        requests_library = BuiltIn().get_library_instance('RequestsLibrary')
        response = requests_library.put_request(self, *args, **kwargs)
        return self._format_response(response)
    
    @keyword
    def options_request_formatted(self, *args, **kwargs):
        """
        Send a OPTIONS request on the session object found using the given alias
        This keyword returns two variables, the first is the request response, the second
        is a dictionary containing ``headers`` and ``json`` keys having as values dotdict 
        objects and a boolean ``is_valid_json``

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the OPTIONS request to

        ``headers`` a dictionary of headers to use with the request

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.

        ``timeout`` connection timeout
        """
        requests_library = BuiltIn().get_library_instance('RequestsLibrary')
        response = requests_library.options_request(self, *args, **kwargs)
        return self._format_response(response)
    
    @keyword
    def patch_request_formatted(self, *args, **kwargs):
        """
        Send a PATCH request on the session object found using the given alias
        This keyword returns two variables, the first is the request response, 
        the second is a dictionary containing ``headers`` and ``json`` keys having
        as values dotdict objects and a boolean ``is_valid_json``

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the PATCH request to
        
        ``data`` a dictionary of key-value pairs that will be urlencoded and sent as
        PATCH data or binary data that is sent as the raw body content or passed 
        as such for multipart form data if files is also defined

        ``json`` a value that will be json encoded and sent as PATCH data if files
        or data is not specified

        ``params`` url parameters to append to the uri

        ``headers`` a dictionary of headers to use with the request

        ``files`` a dictionary of file names containing file data to PATCH to the server

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.

        ``timeout`` connection timeout
        """
        requests_library = BuiltIn().get_library_instance('RequestsLibrary')
        response = requests_library.patch_request(self, *args, **kwargs)
        return self._format_response(response)
    
    @keyword
    def head_request_formatted(self, *args, **kwargs):
        """
        Send a HEAD request on the session object found using the given alias
        This keyword returns two variables, the first is the request response,
        the second is a dictionary containing ``headers`` and ``json`` keys
        having as values dotdict objects and a boolean ``is_valid_json``

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the HEAD request to

        ``headers`` a dictionary of headers to use with the request

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect 
        following is allowed.

        ``timeout`` connection timeout
        """
        requests_library = BuiltIn().get_library_instance('RequestsLibrary')
        response = requests_library.head_request(self, *args, **kwargs)
        return self._format_response(response)
    
    @keyword
    def delete_request_formatted(self, *args, **kwargs):
        """
        Send a DELETE request on the session object found using the given alias
        This keyword returns two variables, the first is the request response, 
        the second is a dictionary containing ``headers`` and ``json`` keys having
        as values dotdict objects and a boolean ``is_valid_json``
        alias that will be used to identify the Session object in the cache

        ``uri`` to send the DELETE request to

        ``json`` a value that will be json encoded and sent as request data if data
        is not specified

        ``headers`` a dictionary of headers to use with the request

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.

        ``timeout`` connection timeout
        """
        requests_library = BuiltIn().get_library_instance('RequestsLibrary')
        response = requests_library.delete_request(self, *args, **kwargs)
        return self._format_response(response)


    def _format_response(self, response):
        response_dict = {}
        try:
            content_to_json = response.json()
            if not isinstance(content_to_json, list):
                self.builtin.set_test_variable("${current_response_content}", content_to_json)
                response_dict['json'] = self.builtin.create_dictionary("&{current_response_content}")
            else:
                response_dict['json'] = content_to_json
            response_dict['is_valid_json'] = True
        except:
            response_dict['json'] = response.text
            response_dict['is_valid_json'] = False

        try:
            self.builtin.set_test_variable("${current_response_headers}", response.headers)
            response_dict['headers'] = self.builtin.create_dictionary("&{current_response_headers}")
        except:
            response_dict['headers'] = response.headers
        self.builtin.set_test_variable("${current_response}", response_dict)
        return response, self.builtin.create_dictionary("&{current_response}")

    def _to_json(self, content):
        PY3 = sys.version_info > (3,)
        """ Convert a string to a JSON object
        ``content`` String content to convert into JSON
        """
        if PY3 and isinstance(content, bytes):
            content = content.decode(encoding='utf-8')
        json_ = json.loads(content)
        return json_
    
    @keyword
    def each_response_element_should_contain_dictionary(self, content, **dictionary):
        """
        Verifies that each element of response content (a valid list)
        contains a dictionary recursively (See Subdictionary is Contained
        in Dictionary Recursive kw)

        ``content`` is the response content dict
        
        ``**dictionary`` is the dictionary that is part of each
        element of response content
        """
        content = self._format_list_content(content)
        for item in content:
            self.subdictionary_is_contained_in_dictionary_recursive(dictionary, item)
    
    @keyword
    def response_headers_should_contain_dictionary(self, headers, **dictionary):
        """
        Verifies that response ``headers``recursively contains a

        ``**dictionary`` (See `Subdictionary is Contained in Dictionary
        Recursive` keyword)
        """
        self.subdictionary_is_contained_in_dictionary_recursive(dictionary, headers)
    
    @keyword
    def response_content_should_contain_dictionary(self, content, **dictionary):
        """
        Verifies that response ``content``recursively contains a

        ``**dictionary`` (See `Subdictionary is Contained in Dictionary
        Recursive` keyword)
        """
        self.subdictionary_is_contained_in_dictionary_recursive(dictionary, content)

    def _format_list_content(self, content):
        try:
            if not isinstance(content, list):
                return self._to_json(content)
        except:
            raise Exception("Response is not a list")
        return content
    
    @keyword
    def format_uri_with_params(self, uri, *args, **kwargs):
        """
        Gets a string that specifies a ``uri`` and formats

        ordinal or named braces with ``*args`` or ``**kwargs``
        """
        uri = uri.format(*args, **kwargs)
        return uri
    
    @keyword
    def subdictionary_is_contained_in_dictionary_recursive(self, dict_a, dict_b):
        """
        Verifies that ``subdictionary`` in recursively contained
        in ``dictionary``, namely it checks that items of ``subdictionary``
        and all its subdictionaries and lists are contained in ``dictionary``

        ``subdictionary`` is the dict that needs to be contained
        
        ``dictionary`` is the container dict
        """ 
        self.errori = []
        if dict_a != dict_b:
            self._dict_compare_rec(dict_a, dict_b)
            if len(self.errori) > 0:
                raise Exception("\n".join(self.errori))

    def _dict_compare_rec(self, dict_a, dict_b):
        for key_a in dict_a.keys():
            value_a = dict_a.get(key_a)

            if key_a not in dict_b:
                self.errori.append("Key: %s not in dict_b" % key_a)
            else:
                value_b = dict_b.get(key_a)
                if value_a != value_b:
                    if not (isinstance(value_a, type(value_b))):
                        self.errori.append("Key: %s, Type: %s - Key %s, Type: %s, DIFFERENT TYPES"
                                           % (key_a, type(value_a), key_a, type(value_b)))
                    else:
                        if isinstance(value_a, dict):
                            self._dict_compare_rec(value_a, value_b)
                        elif isinstance(value_a, list):
                            result = all(elem in value_b for elem in value_a)
                            if result: self.errori.append("List: %s is not contained in list: %s" % (value_a, value_b))
                        elif value_a != value_b:
                            self.errori.append(
                                "Key: %s, Value: %s != Key %s, Value: %s" % (key_a, value_a, key_a, value_b))
        
    @keyword
    def get_dotdict_from_file(self, file_path):
        """
        Reads the content of a JSON file specified by a ``file_path``
        and converts it to a Robot Framework dictionary, accessible via dot-notation
        """
        json_file = self.operatingsystem.get_file(file_path)
        json_file = self._to_json(json_file)
        self.builtin.set_test_variable("${json_file_python}", json_file)
        json_file = self.builtin.create_dictionary("&{json_file_python}")
        return json_file
    
    @keyword
    def check_response_length_limit(self, content, limit):
        """
        Checks that the response ``content`` (a valid JSON that represents a list)
        has a maximum length, defined by ``limit``
        """
        if isinstance(content, (str, bytes, bytearray)):
            content = self._to_json(content)
        l = len(content)
        if l > int(limit):
            raise Exception('Length is {}, limit is {}'.format(l, limit))