
# A simple python script to look for availability of GeForce RTX 3080 and 3090.

## (Currently it can complete a purchase from newegg as well.)

It's very straightforward to use but assumes a little knowledge of python.
Download Geckodriver from here httpsgithub.commozillageckodriverreleases put it in PATH.

You need to create a [PushBullet](https://www.pushbullet.com/account) and find your API key.
Add your PushBullet API key to the script.

Now you can run multiple instances by calling Python rtx_notifier.py vendor of choice

for example:

	`Python rtx_notifier.py newegg`

The project is currently setup for RTX 3080. You need to manually change the search links in the `vendict` object.

Good luck!