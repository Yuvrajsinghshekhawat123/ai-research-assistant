# Configuration means things that may change without changing your code.
'''Examples:

API Key
Model Name
Temperature
Max Tokens


Instead of writing:
    API_KEY = "abcd1234"

inside your code,
we keep it in:
.env

Then config.py loads it.







# Why Separate config.py?

Imagine later you add:

"Database URL
Model name
Temperature
Max tokens"

Instead of scattering these values throughout your code, you keep them in one place.

Later, config.py might look like this:

GEMINI_API_KEY = ...
MODEL_NAME = ...
TEMPERATURE = ...
MAX_TOKENS = ...

Now every file can simply import the configuration.
'''


from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY");
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")
