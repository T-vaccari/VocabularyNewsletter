# Daily Vocabulary Newsletter

Welcome to the Daily Vocabulary Newsletter application! This project is designed to send daily vocabulary emails to recipients based on data stored in Google Sheets and Google Docs. The email includes vocabulary words and their meanings, formatted in HTML.

## Overview

This application performs the following tasks:

1. **Reads Data from Google Sheets**: Fetches recipient details and preferences.
2. **Retrieves Vocabulary from Google Docs**: Extracts vocabulary words and their meanings.
3. **Generates HTML Email**: Formats the vocabulary list into an email-friendly HTML layout.
4. **Sends Emails**: Sends the formatted vocabulary emails to the recipients.

## Features

- Fetches vocabulary data from Google Docs.
- Sends HTML-formatted emails to multiple recipients.
- Updates vocabulary counts in Google Sheets based on email content.

## Prerequisites

- Python 3.x
- Google Cloud Project with Sheets and Docs API enabled
- Gmail account for sending emails

## Setup

1. Inserting in the code the mail sender and the password.
2. Inserting the ID of the google sheet used as backend for importing the subscribers of the newsletter and their personal vocabulary.
3. Deploy the script on github action and set the worflow at a specified hour.

## More information
Soon you are going to find an article on my website about this project and how to setup it!

