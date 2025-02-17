# banking-ld

# Install Python Dependencies
Defined in requirements.txt.

Example using pip and venv virtual environment on Windows:
`.venv/Scripts/activate`
`pip install -r requirements.txt`

# LaunchDarkly setup

## SDK key
1. Create SDK Key as explained here: https://docs.launchdarkly.com/home/account/environment/settings#copy-sdk-credentials-for-an-environment
2. Set SDK key variable towards top of `main.py` or use environment variable LDKEY and uncomment line 10.

## Feature Flags
1. Create two feature flags named 'missile' and 'worldDomination' (or modify main.py per your liking)
2. 'worldDomination' flag is used for showing the ability to trigger a feature on/off remotely
    a. Create trigger per https://docsps.launchdarkly.com/home/releases/triggers
    b. Use curl to post to trigger specific on/off url with empty body `curl -X POST "https://app.launchdarkly.com/webhook/triggers/1234567890"`
    c. Default rule serves `Disabled`
3. 'missile' flag is used for individual and rule based targeting
    a. Create one individual targeting rule looking for `user` is `superadmin`
    b. Create a custom rule with the following criteria:
        `If user country is one of United States`
        `And if user name is one of superadmin`
    b. Default rule serves `Disabled`

# Run the Application
1. Navigate to the root directory and run main.py `python main.py` 
2. If browser does not automatically open, navigate to http://127.0.0.1:8080

# Navigating the Application
Triggering the 'worldDomination' flag enables/disables the ability to "log into" the application. 'superadmin' has the ability to launch a missile as long as they're logged in from the US. All other users are brought to a 'banking' page.