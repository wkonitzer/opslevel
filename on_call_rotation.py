"""
This script automates the retrieval of escalation policies from PagerDuty and
subsequently posts this data to OpsLevel. It utilizes environment variables to
manage API tokens and logging configurations based on the deployment environment
(development vs. production).

The script handles common HTTP errors and logs different levels of output
depending on whether it's run in a production environment or a development
setting. In production, only errors are logged to a file to minimize noise and
disk usage, whereas in development, more verbose logging is used for debugging
purposes.

Dependencies:
    - requests: Used for HTTP requests to the PagerDuty and OpsLevel APIs.
    - os: Used to access environment variables.
    - logging: Used for logging messages and errors.

Environment Variables:
    - PAGERDUTY_API_TOKEN: API token for PagerDuty.
    - OPSLEVEL_API_TOKEN: API token for OpsLevel.
    - ENVIRONMENT: Specifies the current running environment
                   ('production' or other).

Setup:
    - Ensure that the required environment variables are set before running the
      script.
    - Install the necessary Python packages: requests.
"""
import logging
import os
import requests


def main():
    """
    Main function that orchestrates the retrieval and posting of escalation
    policies. It first retrieves escalation policies from the PagerDuty API and
    then posts this data to OpsLevel. This function includes error handling to
    manage potential HTTP and network-related exceptions during API interactions.

    Steps:
    1. Makes an HTTP GET request to PagerDuty's escalation policies endpoint.
    2. If the request is successful, it extracts the JSON response containing the
       escalation policies.
    3. Logs the successful retrieval of data.
    4. Makes an HTTP POST request to OpsLevel's custom event endpoint to post the
       retrieved policies.
    5. Logs the successful posting of data to OpsLevel.
    
    Exceptions:
    - Handles broad exceptions during the HTTP requests by calling the
      `handle_request_errors` function, which logs errors related to timeouts,
      HTTP errors, network-related issues, or JSON decoding problems.
    """
    # Setup environment variables
    pd_api_token = os.getenv("PAGERDUTY_API_TOKEN")
    opslevel_api_token = os.getenv("OPSLEVEL_API_TOKEN")

    # Configure logging based on environment
    if os.getenv("ENVIRONMENT") == "production":
        logging.basicConfig(filename='app.log', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    # Opslevel endpoint URL
    ol_cec_endpoint = f"https://app.opslevel.com/integrations/custom_event/{opslevel_api_token}"

    # Headers for PagerDuty API request
    headers_pd = {
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': f'Token token={pd_api_token}'
    }

    # Headers for OpsLevel API request
    headers_ol = {
        'Content-Type': 'application/json'
    }
    
    pd_escalation_policies = None

    try:
        # Get escalation policies from PagerDuty with a timeout
        response_pd = requests.get(
            'https://api.pagerduty.com/escalation_policies',
            headers=headers_pd, timeout=5
        )
        response_pd.raise_for_status()
        pd_escalation_policies = response_pd.json()
        logging.info("Escalation policies retrieved successfully.")
    except Exception as error: # pylint: disable=broad-except
        handle_request_errors(error)

    try:
        # Send the obtained data to OpsLevel with a timeout
        response_ol = requests.post(
            ol_cec_endpoint, headers=headers_ol, json=pd_escalation_policies,
                             timeout=5
        )
        response_ol.raise_for_status()
        logging.info("Data posted to OpsLevel successfully.")
    except Exception as error: # pylint: disable=broad-except
        handle_request_errors(error)


def handle_request_errors(exc):
    """
    Handles common HTTP and network-related errors by logging appropriate error
    messages. This function is designed to centralize error handling for HTTP
    requests made within the script, simplifying the management of different
    types of exceptions that might occur during these requests.

    Args:
    exc (Exception): The exception instance caught during HTTP requests.

    Handles:
    - requests.exceptions.Timeout: Logs a timeout error indicating network or
      response issues.
    - requests.exceptions.HTTPError: Logs detailed HTTP error information
      provided by the server.
    - requests.exceptions.RequestException: Logs other network-related errors
      that occurred.
    - ValueError: Logs errors related to JSON decoding issues.

    No return value; this function operates by side effect (logging).
    """
    if isinstance(exc, requests.exceptions.Timeout):
        logging.error("Request timed out. Check your network connection or the URL.")
    elif isinstance(exc, requests.exceptions.HTTPError):
        logging.error("HTTP error occurred: %s", exc)
    elif isinstance(exc, requests.exceptions.RequestException):
        logging.error("A network error occurred: %s", exc)
    elif isinstance(exc, ValueError):
        logging.error("Error decoding JSON")


if __name__ == "__main__":
    main()
