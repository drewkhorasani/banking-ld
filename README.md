# banking-ld

# Install Python Dependencies

This has been tested with `python 3.13` in a Windows venv. However, instructions for running are similar in other OS as long as the python version matches.

We must install the python dependencies defined in `requirements.txt`

Example using pip and venv virtual environment on Windows:  
`.venv/Scripts/activate`  
`pip install -r requirements.txt`  

# LaunchDarkly setup

## SDK key
1. Create SDK Key as explained here: https://docs.launchdarkly.com/home/account/environment/settings#copy-sdk-credentials-for-an-environment
2. Set SDK key variable towards top of `main.py` or use environment variable LDKEY and uncomment line 10.

## Feature Flags

### Missile flag

To create a feature flag in LaunchyDarkly after logging in to https://app.launchdarkly.com:  
(Sign up for free trial here: https://app.launchdarkly.com/signup)  
  
1. Click Create and choose Flag. The “Create new flag” page appears.  

Enter 'missile' as the Name.  
  
(Optional) Update the flag Key. You’ll use this key to reference the flag in your code.  

2. Choose the 'custom' type and mimic the following settings:  
    -Temporary=yes  
    -Flag Type=Boolean  
    -Variation with Value=true:  
        -Name=Enabled  
    -Variation with Value=false:  
        -Name=Disabled  
    -Default variations  
        -Serve when targeting is ON=false  
        -Serve when targeting is OFF=false  

3. Click Create Flag. This flag will be used for individual and rule based targeting which allows us to choose how different features are served. On the flag screen, be sure the 'Production' environment is selected towards the top.  

4. Click 'Add rule' and select 'Target Individuals'  

5. Under the 'Serve true'->user section, we will add the `superadmin` user  

6. Click 'Review and Save', enter a comment for the change, and type the environment name before clicking 'Save changes'  

7. On the same 'missile' feature flag, click 'Add rule' again and select 'Build a custom rule'  

8. Give the rule a name  

9. Your first 'IF' statement should look as follows:
    Context kind=user
    Attribute=country
    Operator=is one of
    Values=United States

10. Add another 'IF' statement by clicking the '+' and choosing 'Custom'  

11. The new 'IF' statement should look as follows:  
    Context kind=user  
    Attribute=name  
    Operator=is one of  
    Values=superadmin  

12. Click 'Review and Save', enter a comment for the change, and type the environment name before clicking 'Save changes'.  

13. On the 'missile' feature flag screen, flip the 'Enable targeting rules for Production' switch from 'Off' to 'On'.  


### World Domination Flag

1. Click Create and choose Flag. The “Create new flag” page appears.  

Enter 'worldDomination' as the Name.  
  
(Optional) Update the flag Key. You’ll use this key to reference the flag in your code.  

2. Choose the 'custom' type and mimic the following settings:  
    -Temporary=yes  
    -Flag Type=Boolean  
    -Variation with Value=true:  
        -Name=Enabled  
    -Variation with Value=false:  
        -Name=Disabled  
    -Default variations  
        -Serve when targeting is ON=true  
        -Serve when targeting is OFF=false  

3. Click Create Flag. This flag will simply be an 'On'/'Off' switch for being able to log into the application.

#### Testing enabling/disabling the login feature
Follow the instructions here to create two Generic triggers for the 'worldDomination' flag in the production environment: https://launchdarkly.com/docs/home/releases/triggers-create

We will have one trigger update the flag targeting to 'On' and one trigger update the flag targeting to 'Off'.

Once you have your 'ON'/'OFF' endpoints after creating the triggers, you can toggle the flag by posting an empty body to each respective endpoint. Example using curl:
`curl -X POST "https://app.launchdarkly.com/webhook/triggers/1234567890"`  
  
  
# Run the Application
1. Navigate to the root directory and run main.py `python main.py` 
2. If browser does not automatically open, navigate to http://127.0.0.1:8080

# Navigating the Application
Toggling the targeting switch on the the 'worldDomination' flag enables/disables the ability to "log into" the application.  

Because we set up a feature flag to look for the 'superadmin' user, entering 'superadmin' as the user brings the user to a unique screen with the ability to launch a missile as long as they're logged in from the US. All other users are brought to a 'banking' page.
