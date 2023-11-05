import clr
from helper import clean_code_snippet, ContextData
clr.AddReference('System')
clr.AddReference('System.Net')

from System import String
from System.Net import WebClient, WebRequest
from System.Text import Encoding
from System.IO import StreamReader

input_string = 'From the selected elements, list their lengths by family name'


def main(input_string):
    # Create an instance of ContextData
    context_data = ContextData()

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
    data = Encoding.UTF8.GetBytes(String.Format('{{"client": "{0}"}}', input_string))

    # Send the POST request
    for i in range(5):
        try:
            responseBytes = client.UploadData(url, "POST", data)
            responseString = Encoding.UTF8.GetString(responseBytes)
            clean_code = clean_code_snippet(responseString)
            print("Code response:/n", clean_code)
            exec(clean_code)
        except Exception as e:
            print(e)
            main()
        pass


# Initialize a counter for the number of attempts
attempts = 0

# Define the maximum number of attempts
max_attempts = 5

# Use a while loop to try the function up to max_attempts times
while attempts < max_attempts:
    try:
        # Try to call the risky function
        main()
        print("Function succeeded.")
        break  # Exit the loop if the function succeeds
    except Exception as e:
        # If an exception occurs, print the error and increment the attempt counter
        print("Attempt {} failed with error: {}".format(attempts + 1, e))
        attempts += 1
        if attempts == max_attempts:
            print("Function failed after maximum number of attempts.")

