print("Code was moved to other button")

'''
import clr
from System import String
from System.Net import WebClient, WebRequest
from System.Text import Encoding
from System.IO import StreamReader
from System.Threading import Thread
from helper import clean_code_snippet
from System.Net import WebException

clr.AddReference('System')
clr.AddReference('System.Net')
clr.AddReference('System.Threading')

input_string = 'From the selected elements, list their lengths by family name'


def clean_response_string(response):
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789- "
    cleaned_string = ''.join(c for c in response if c in allowed_chars)
    return cleaned_string


def main(window, input_string):
    max_attempts = 10
    counter = 1
    context = ""
    url = 'http://127.0.0.1:8080/'

    client = WebClient()

    state = window.state()

    while counter <= max_attempts:
        json_data = '{{"client": "{0}. {1}."}}'.format(input_string, context)
        data = Encoding.UTF8.GetBytes(json_data)
        client.Headers.Add("Content-Type", "application/json; charset=utf-8")
        print("Sending data to server: {}".format(json_data))  # Check the JSON structure

        try:
            responseBytes = client.UploadData(url, "POST", data)
            responseString = Encoding.UTF8.GetString(responseBytes)
            if "MISSING" in responseString:
                x = ('missing', responseString.split("MISSING-")[1])
                state['data'].append(x)
                window.update_state(state)

            clean_code = clean_code_snippet(responseString)
            print("Code response: ", clean_code)
            exec(clean_code)

            x = ('successful', '')
            state['data'].append(x)
            window.update_state(state)
            return  # Successful execution, exit the loop
        except WebException as webEx:
            if webEx.Response is not None:
                responseStream = webEx.Response.GetResponseStream()
                if responseStream is not None:
                    reader = StreamReader(responseStream)
                    errorMessage = reader.ReadToEnd()
                    response_exception = clean_response_string(errorMessage)
                    x = ('exception', f"Server error response: {response_exception}")
                    state['data'].append(x)
                    window.update_state(state)
            else:
                x = ('exception', f"WebException without response: : {webEx.Message}")
                state['data'].append(x)
                window.update_state(state)
        except Exception as e:
            response_exception = clean_response_string(str(e))
            print("Exception: ", response_exception)
            x = ('exception', f"Exception: {response_exception}")
            state['data'].append(x)
            window.update_state(state)
        finally:
            context = "Consider this error: {}".format(response_exception)
            counter += 1
            x = ('attempt', "Attempt: {}".format(counter))
            state['data'].append(x)
            window.update_state(state)
            if counter > max_attempts:
                print("Maximum attempts reached. Exiting.")
                x = ('failure', "Maximum attempts reached. Exiting.")
                state['data'].append(x)
                break  # Ensure to break out of the loop
'''
        