# Introduction
Connects with a Honeywell Lyric thermostat through Honeywell API and writes temperature to InfluxDB.
The indoor temperature and temperature set point are collected and written per thermostat.  
For docker check: https://hub.docker.com/repository/docker/thijswm/lyric2influx

# Connect with Honeywell API
To be able to let this image connect with the thermostat you need to have a token from the Honeywell API.
This token can be entered in the LYRIC_TOKEN field

1. Sign up at the honeywell developer home: https://developer.honeywellhome.com
2. Create a new app (eg influx), use as callback url: 'none'
3. Click on the app name to see the generated consumer key and consumer secret
4. Open a browser and visit the following url after replacing the CONSUMERKEY in the url  
`https://api.honeywell.com/oauth2/authorize?response_type=code&client_id=[[CONSUMERKEY]]&redirect_uri=none`
5. Login with the credentials you have used to register the Honeywell device. After giving permissions to read out the thermostat device your browser will be redirected to the non-existing 'none' website.
6.  Take a closer look at the address bar of your browser.  
The url in the address bar should be like: http://api.honeywell.com/oauth2/app/none?code=CODEVALUE&scope=  
Copy paste the code value as you will need this code in step 8.
7. Base64 encode the following string (without quotes) "[[CONSUMERKEY]]:[[CONSUMERSECRET]]" . This can be done from the Linux command line by using  
`echo -n "[[CONSUMERKEY]]:[[CONSUMERSECRET]]" | base64`  
Or use an online website like: https://www.base64encode.org/
8. Finally make the last webrequest to the Honeywell API to retrieve the Access Token and Refresh Token. Make sure to replace the Base64 encoded string and the CODE:  
`curl -X POST -H 'Authorization: Basic [[BASE64-ENCODED-STRING]]' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: application/json' -d 'grant_type=authorization_code&code=[[CODE]]&redirect_uri=none' https://api.honeywell.com/oauth2/token`  
You can also use a site like: https://reqbin.com/curl
9. If everything is ok, the server will return a response similar as:  
`{"access_token":"494aiudfheuhdfi84949de","refresh_token":"jdaoijodfoUHdud13532","expires_in":"1799", "token_type":"Bearer"}`

# Description of the Environment Variables
This image has the following environment variables 
- LYRIC_CLIENT_ID  - The honeywell API consumer key for your registered application
- LYRIC_CLIENT_SECRET - The honeywell API consumer key for your registered application
- LYRIC_APP_NAME - The honeywell API application name for your registered application
- LYRIC_REDIRECT_UI - The honeywell API redirect uri for your registered application (When the above steps are followed: `none`)
- LYRIC_TOKEN - The honewell API token as collected with the above `Connect with Honeywell API` steps

- INFLUX_URL - The influx db url (Example: http://hostname:8086)
- INFLUX_DB - The influx db database or bucket
- INFLUX_USERNAME - The influx db username
- INFLUX_PASSWORD - The influx db password

- POLL_INTERVAL - Poll interval in seconds (Default: `120`)
- DEBUG_MODE - Set logging level to debug (Default: `False`)
