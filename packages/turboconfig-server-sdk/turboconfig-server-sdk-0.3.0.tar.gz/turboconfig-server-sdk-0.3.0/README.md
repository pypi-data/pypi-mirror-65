# TurboConfig Server-side SDK for Python

## Supported Python versions

This SDK is compatible with Python 2.7 and 3.3 through 3.7.

## Installation

```
pip install turboconfig-server-sdk
```

## Initialization

Import `turboconfig` library

```
import turboconfig as TurboConfig
```

To initialize TurboConfig object, call

```
tc = TurboConfig.initialize("ENVIRONMENT KEY");
```

If you want to access the TurboConfig object at any time, you can call getInstance()

```
tc = TurboConfig.get_instance();
```

## Accessing Flags and Configs

To access a Flag from TurboConfig, you should first initialize the `Identity` object and then use it to fetch flags and configs.

```
identity = TurboConfig.Identity(user_id, name, email, phone_number, attributes)
```

> Note that, `user_id` is the only compulsory parameter to initialize `Identity` object.

You can set other properties to `Identity` object at any time as described below

```
identity.name = ""
identity.email = ""
identity.phone_number = ""

identity.attributes = {"KEY", "VALUE"} // If you want to reset custom attributes
identity.set_attribute("KEY", "VALUE") // If you want to update custom attributes
```

To access a Flag from TurboConfig, you call the `get_boolean_config` method.

The method accepts three arguments -- Flag's Key, `Identity` object and Default Value if the internet or old value is not available.

```
value = tc.get_boolean_config("flag-key", identity, False)

if value:
    // Do something if the Flag is ON!
else:
    // Do something else when the Flag is OFF!
```

Similarly, for String or Integer configs, you can do this

```
value = tc.get_string_config("string-config-key", identity "default"); // Returns the last stored value, or default value if the data hasn't been fetched yet

value = tc.get_integer_value("int-config-key", 0); // Returns the last stored value, or default value if the data hasn't been fetched yet
```

## Close

Close safely shuts down the client instance and releases all resources associated with the client. In most long-running applications, you should not have to call close.

```
tc.close()
```

## Configuring uWSGI

The SDK is compatible with uWSGI. However, in uWSGI environments, the SDK requires the enable-threads option to be set.

## Logging

The SDK uses Python's built-in [logging library](https://docs.python.org/2/library/logging.html). All loggers are namespaced under `turboconfig.util`.
