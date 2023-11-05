import clr
from System import String
from System.Net import WebClient, WebRequest
from System.Text import Encoding
from System.IO import StreamReader
from helper import clean_code_snippet, ContextData
clr.AddReference('System')
clr.AddReference('System.Net')


input_string = 'From the selected elements, list their lengths by family name'


def clean_response_string(response):
    # Define the allowed characters
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~"

    # Use a list comprehension to filter out unwanted characters
    cleaned_string = ''.join(c for c in response if c in allowed_chars)

    return cleaned_string


def main(input_string):
    max_attempts = 5
    # Set the context
    context_data.context = ""

    # The server's URL
    url = ' http://127.0.0.1:8080/'

    # The string you want to send

    # Create a web client
    client = WebClient()

    # Set the header so the server knows to expect JSON
    client.Headers.Add("Content-Type", "application/json")

    # Serialize the data to a JSON string
    print("Input string: {}".format(input_string))
    data = Encoding.UTF8.GetBytes(String.Format('{{"client": "{0}"}}', input_string))

    # Use a while loop to try the function up to max_attempts times
    while context_data.counter < max_attempts:
        try:
            responseBytes = client.UploadData(url, "POST", data)
            responseString = Encoding.UTF8.GetString(responseBytes)
            clean_code = clean_code_snippet(responseString)
            print("Code response: ", clean_code)
            exec(clean_code)
            break  # Exit the loop if exec is successful
        except Exception as e:
            response_exception = str(e)  # Assuming you want to convert the exception to a string
            print(response_exception)
            context = "Consider this error: {}.".format(response_exception)
            input_string = "{} {}".format(input_string, context)
            context_data.increment_counter()
            print(context_data.counter)
            if context_data.counter >= max_attempts:
                print("Maximum attempts reached. Exiting.")
                break  # Exit the loop if max attempts have been reached
            main(input_string) 



# Create an instance of ContextData
context_data = ContextData()
context_data.counter = 1
main(input_string)
# # Initialize a counter for the number of attempts
# attempts = 0

# # Define the maximum number of attempts
# max_attempts = 5

# # Use a while loop to try the function up to max_attempts times
# while attempts < max_attempts:
#     try:
#         # Try to call the risky function
#         main()
#         print("Function succeeded.")
#         break  # Exit the loop if the function succeeds
#     except Exception as e:
#         # If an exception occurs, print the error and increment the attempt counter
#         print("Attempt {} failed with error: {}".format(attempts + 1, e))
#         attempts += 1
#         if attempts == max_attempts:
#             print("Function failed after maximum number of attempts.")

