# Golem Bot README

## get_greeting()

Returns a greeting from content/greetings.json for all channels not serviced by GPT-3

Returns:
    _str_: _Coinflip between a funny written response and a funny glitch response._

## get_openai_API_greeting()

Take the contents of messages starting with '>hello' in certain channels and pulls a response from GPT-3

Args:
    Message (_str_): _A string of the message contents to which the bot should respond_

Returns:
    _str_: _A string response to the message taken from the GPT-3 API_

## load_dotenv()

Parse a .env file and then load all the variables found as environment variables.

- _dotenv_path_: absolute or relative path to .env file.
- _stream_: Text stream (such as `io.StringIO`) with .env content, used if
  `dotenv_path` is `None`.
- _verbose_: whether to output a warning the .env file is missing. Defaults to
  `False`.
- _override_: whether to override the system environment variables with the variables
  in `.env` file.  Defaults to `False`.
- _encoding_: encoding to be used to read the file.

If both `dotenv_path` and `stream`, `find_dotenv()` is used to find the .env file.

## on_message()

Define a bot event that waits for a message in a channel and then responds with a greeting from the openai chatbot API

Args:
    Message (_discord.Message_): _A message object sent by a user in the server._

## on_ready()

None
