from .lambda_function import LambdaFunction
import json
import re


class APIFunction(LambdaFunction):
    def run(self, event, context):
        # Get the calling method and route appropriately.
        method = event["httpMethod"].lower()

        # Get get query params to pass in.
        params = self._get_url_params()
        args = [event["pathParameters"][p] for p in params]

        # TODO: Should use a more elegent method of routing here.
        if method == "post":
            response = self.post(event, context, *args)

        elif method == "get":
            response = self.get(event, context, *args)

        elif method == "put":
            response = self.put(event, context, *args)

        elif method == "options":
            print("Returning options payload:")
            response = self.create_return()
            print(response)

        else:
            raise Exception(f"Triggered with unexpected HTTP method {method}.")

        return response

    def create_return(self, status_code=200, body=None):
        return_obj = {"statusCode": status_code}
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Authorization,Content-Type",
            "Access-Control-Allow-Methods": "*",
        }
        return_obj["headers"] = headers
        if body:
            return_obj["body"] = json.dumps(body)
        return return_obj

    def get_methods(self):
        methods = []
        # Check post method.
        post = getattr(self, "post", None)
        if callable(post):
            methods.append("POST")

        # Check get method.
        get = getattr(self, "get", None)
        if callable(get):
            methods.append("GET")

        # Check put method.
        put = getattr(self, "put", None)
        if callable(put):
            methods.append("PUT")

        return methods

    def _get_url_params(self):
        if not self.endpoint.endswith("/"):
            self.endpoint = self.endpoint + "/"
        regex = re.compile("/{(.*?)}/")
        params = regex.findall(self.endpoint)
        return params
