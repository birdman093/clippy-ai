import clr
from System import String
from System.Net import WebClient, WebRequest
from System.Text import Encoding
from System.IO import StreamReader
from helper import clean_code_snippet, ContextData
from System.Net import WebException
clr.AddReference('System')
clr.AddReference('System.Net')

# Instantiate ContextData
context_data = ContextData()

input_string = 'From the selected elements, list their lengths by family name'


def clean_response_string(response):
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~ "
    cleaned_string = ''.join(c for c in response if c in allowed_chars)
    return cleaned_string


def main(input_string, context_data):
    max_attempts = 10
    counter = 1
    url = 'http://127.0.0.1:8080/'

    client = WebClient()
    client.Headers.Add("Content-Type", "application/json; charset=utf-8")

    while context_data.counter <= max_attempts:
        json_data = '{{"client": "{0}. {1}"}}'.format(input_string, context_data.context)
        data = Encoding.UTF8.GetBytes(json_data)
        print("Sending data to server: {}".format(json_data))  # Check the JSON structure

        try:
            responseBytes = client.UploadData(url, "POST", data)
            responseString = Encoding.UTF8.GetString(responseBytes)
            clean_code = clean_code_snippet(responseString)
            print("Code response: ", clean_code)
            exec(clean_code)
            return
        except WebException as webEx:
            if webEx.Response is not None:
                responseStream = webEx.Response.GetResponseStream()
                if responseStream is not None:
                    reader = StreamReader(responseStream)
                    errorMessage = reader.ReadToEnd()
                    response_exception = clean_response_string(errorMessage)
                    print("Server error response: ", response_exception)
            else:
                print("WebException without response: ", webEx.Message)
        except Exception as e:
            response_exception = clean_response_string(str(e))
            print("Exception: ", response_exception)
        finally:
            context_data.context = "Consider this error: {}".format(response_exception)
            context_data.increment_counter()
            counter = context_data.counter
            print("Attempt: {}".format(counter))

        if counter > max_attempts:
            print("Maximum attempts reached. Exiting.")
            return


main(input_string, context_data)
