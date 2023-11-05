import clr
from System import Array, Byte
from System.Net import WebClient, WebRequest, WebException
from System.Text import Encoding
from System.IO import StreamReader
from System.Threading import Thread
from helper import clean_code_snippet, ContextData

# Add references to the .NET assemblies needed
clr.AddReference('System')
clr.AddReference('System.Net')
clr.AddReference('System.Threading')


# Instantiate ContextData
context_data = ContextData()

input_string = 'From the selected elements, list their lengths by family name'

# Function to clean the response string
def clean_response_string(response):
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
    cleaned_string = ''.join(c for c in response if c in allowed_chars)
    return cleaned_string

# Main function to send data to the server and handle the response
def main(input_string, context_data):
    max_attempts = 10
    context_data.counter = 1
    url = 'http://127.0.0.1:8080/'
    delay_between_requests = 10000  # Delay in milliseconds

    # Create a WebClient instance
    client = WebClient()
    client.Headers.Add("Content-Type", "application/json; charset=utf-8")

    while context_data.counter <= max_attempts:
        json_data = '{{"client": "{0}"}}'.format(input_string, context_data.context)
        bytes_data = Encoding.UTF8.GetBytes(json_data)
        print("Sending data to server: {}".format(json_data))  # Check the JSON structure

        try:
            # Send the data to the server
            responseBytes = client.UploadData(url, "POST", bytes_data)
            responseString = Encoding.UTF8.GetString(responseBytes)
            clean_code = clean_code_snippet(responseString)
            print("Code response: ", clean_code)
            exec(clean_code)
            return  # Successful execution, exit the loop
        except WebException as webEx:
            if webEx.Response is not None:
                with webEx.Response.GetResponseStream() as responseStream:
                    if responseStream is not None:
                        reader = StreamReader(responseStream)
                        errorMessage = reader.ReadToEnd()
                        response_exception = clean_response_string(errorMessage)
                        print("Server error response: ", response_exception)
                        if "400 Bad Request" in response_exception:
                            print("Client error, will not retry.")
                            break  # Break out of the loop on client error
                        reader.Close()
            else:
                print("WebException without response: ", webEx.Message)
        except Exception as e:
            response_exception = clean_response_string(str(e))
            print("Exception: ", response_exception)
        finally:
            context_data.context = "Consider this error: {}".format(response_exception)
            context_data.increment_counter()
            print("Attempt: {}".format(context_data.counter))
            if context_data.counter > max_attempts:
                print("Maximum attempts reached. Exiting.")
                break  # Ensure to break out of the loop
            Thread.Sleep(delay_between_requests)  # Sleep before the next request


# Call the main function with the input string and context data
main(input_string, context_data)
