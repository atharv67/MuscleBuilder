# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_videos(exercise_name):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    api_key="AIzaSyCtw7UruANrsQAAzvLe-M6Ke9y19z7VScY"
    youtube=googleapiclient.discovery.build('youtube','v3',developerKey=api_key)
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    # api_service_name = "youtube"
    # api_version = "v3"
    # client_secrets_file = "Client_Secret.json"

    # Get credentials and create an API client
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #     client_secrets_file, scopes)
    # credentials = flow.run_console()
    # youtube = googleapiclient.discovery.build(
        # api_service_name, api_version)

    request = youtube.search().list(
        q=exercise_name,
        type="video",
        part="snippet"
    )
    response = request.execute()

    return response['items']

if __name__ == "__main__":
    main()