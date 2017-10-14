# THIO

## Getting started

### Twilio
The python Twilio library can be installed with `pip install twilio` or `easy_install twilio`.
You can test the twilio installation by running `python test_sms.py` with your phone number.
You will need to set the following environmental variables:
1. TWILIO_ACCOUNT_SID
2. TWILIO_AUTH_TOKEN
3. RECIPIENT_TELEPHONE (your own)
4. SENDER_TELEPHONE 
(see below for more on setting up environmental variables)

### AWS
Install the Amazon SDK for python
`pip install boto3`

#### Install AWS CLI (for setting up DB config)
`pip3 install awscli --upgrade --user`
Add AWS CLI to your path.
[AWS Guide for CLI intallation](http://docs.aws.amazon.com/cli/latest/userguide/cli-install-macos.html)
Set up the profile and private keys for the AWS DynamoDB:
Create your THIO profile (you can call it something other than THIO if you prefer):
`aws configure --profile THIO`
In the following prompts you have to enter the access keys, resion, and format. Get these from a peer.

#### Set up your AWS_PROFILE as an environmental variable
Set your project to use the new profile `AWS_PROFILE=THIO`. 
This can be passed before a command, eg `AWS_PROFILE=THIO python test_db.py`, or you can run `export AWS_PROFILE=THIO` to apply it to all future commands in the tab. Add `export AWS_PROFILE=THIO` to your bash_profile to apply it all of the time. 

You can test your AWS DB connection by running `python test_db.py`. You will need to set the DATABASE_NAME environmental variable.
### Troubleshooting
If you are having permission issues intalling things with `pip`, try adding the --user flag.
