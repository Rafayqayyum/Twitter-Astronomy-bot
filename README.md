# Twitter Astronomy Bot

This is a Twitter bot that posts tweets about astronomy-related topics, such as planets, stars, galaxies, and more. It uses the [Astronomy Picture of the Day](https://apod.nasa.gov/apod/astropix.html) to get images and information about astronomy, and posts them to Twitter.
The bot is written in Python. You can find the bot on Twitter at [@AstroMindbot](https://twitter.com/AstroMindbot).

## How to use
To use this bot, you will need to create a Twitter account and a developer account on the [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard). You will also need to register for an API key on the [NASA Open API website](https://api.nasa.gov/).
After you have created your Twitter account and developer account, you will need to create a new app on the Twitter Developer Portal. You will need to create a new app for the bot to use. Once you have created the app, you will need to create a new access token for the app.
After you have created your Twitter app and access token, you will need to setup your environment variables. 

```
API_KEY
API_SECRET_KEY
RESOURCE_OWNER_KEY
RESOURCE_OWNER_SECRET
```

If you're using the developer account as your bot account then your RESOURCE_OWNER_KEY and RESOURCE_OWNER_SECRET will be the same as your Access Token and Secret. If you're using a separate account for the bot, then you will need to run oauth.py to get the RESOURCE_OWNER_KEY and RESOURCE_OWNER_SECRET.

## How to run   
To run the bot, you will need to install the dependencies. You can do this by running the following command:

```
pip install -r requirements.txt
```

After you have installed the dependencies, you can run the bot by running the following command:

```
python twitter.py
```

## Additional Information
The app.py file is used to run the bot as free web service on [Render](https://render.com/). Using [Cron-jobs](https://cron-job.org/en/), the bot will run twice a day at 12:00 AM and 12:00 PM. The oauth.py file is used to get the RESOURCE_OWNER_KEY and RESOURCE_OWNER_SECRET. The twitter.py file is used to run the bot. The nasa_apod.py file is used to get the image and information from the NASA Picture of the Day API.