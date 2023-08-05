# Python Utils

Library for user's payload encryption used with Sitejabber.

## Installation

Installation is easy using pip. Just run the following on the command line:

```
pip install sitejabber-utils
```

# Usage

- Get your API keys on https://biz.sitejabber.com/account
- JSON encode your user data
- Call the encrypt method
- URL-encode the result
- Redirect the user to the feedback link

```
from json import dumps
from sitejabber import utils
try:
	from urllib.parse import quote_plus  # Python 3+
except ImportError:
	from urllib import quote_plus  # Python 2.X

userData = {
	"email":	"janedoe@gmail.com",
	"order_date":	"06-13-2013",
	"order_id":	"1234",
	"first_name":	"Jane",
	"last_name":	"Doe"
}

encryptedData = utils.encrypt(dumps(userData), 'lkjashdlanhsdjasd092390239023902')
feedbackLink = "https://www.sitejabber.com/biz-review?key=API_KEY&payload=" + quote_plus(encryptedData);
print(feedbackLink)

```
