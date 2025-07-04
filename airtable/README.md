# Getting Started

### Airtable AI POC Chat

This web application allows you to interact with an LLM (Large Language Model) and the Airtable API to retrieve candidate information based on specific queried skill sets. The application is built using Next.js and leverages the Ollama model through function tools to facilitate communication between the app, the Llama model, and the Airtable API.

## Overview

In this application, you can:

- Query the Airtable database for candidates with specific skills.
- Use an LLM model (powered by Ollama) to interpret natural language queries and translate them into Airtable API calls.
- Easily retrieve candidate data based on skills, experience, certifications, and more.

The stack includes:

- **Python + fastapi**
- **LLM:** Ollama 
- **Datasource:** Airtable API

## Prerequisites

Before you begin, ensure you have the following prerequisites installed:

- **Python3** (for running the Next.js application)
- **Ollama + langchain** (for AI model interaction)
- **Airtable API Key** (for accessing your Airtable database)

## Installing Ollama

To install Ollama, follow these steps:

1. **Download the Installer**  
   Visit the [Ollama website](https://ollama.com) and download the installer for your operating system.

2. **Run the Installer**  
   Open the downloaded file and follow the on-screen instructions to complete the installation process.

3. **Verify Installation**  
   After installation, open a terminal and run the following command to verify that Ollama is installed correctly:

   ```bash
   ollama --version
   ```

## Installing Ollama Model

1. **Choose the model**

    Refer to the [Ollama Model Library](https://ollama.com/library) to find the model you want to install.

2. **Run and Install Model**

    To run the llama3.2 model, for instance, execute the following command:

    ```bash
    ollama run llama3.2
    ```

## Installation of Web Application 


1. **Clone the Repository**

    To get the latest code for this project, follow the instructions below

    Use the following command to clone the repository:

    ```bash
    git clone https://github.com/nalliappancandt/ai-poc-python.git
    ```

2. **Configuring Airtable API KEY and Other Table configurations**

    Please update following environment variables into .env file.

   

3. **Running the Application**

    First, run the development server:

    ```bash
    # cd airtable
    # fastapi run main.py
    ```

    The application will now be running locally. Open your browser and go to:

    http://localhost:8000/client_example

    http://localhost:8000/docs (API Document)


    You should now see the chat window where you can interact with the system and query candidates based on different skill sets.

## Testing the Application

    Once the application is running, you can test the functionality by entering queries in the query window such as:

        1. Who has Next.js and Python experience with 4 years and 3 years respectively?
        2. How much experience does Manikant Upadhyay has on Next.js?
        3. What was the Manikant Upadhyay Role?
        4. List the people who have AWS certifications?
        5. How many people who have AWS certifications and list out the names?
        6. How many people who have Salesforce certifications and list out the names?
        7. How many people who have Machine Learning certifications and list out the names?
        8. List out the skills and experience having by Shwetha Talapalli?
        9. Find the people who have react.js skill with rating more than 3

## Screen Shots

![alt text](image.png)