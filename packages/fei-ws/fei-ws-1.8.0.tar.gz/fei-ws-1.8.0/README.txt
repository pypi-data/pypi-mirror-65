======
fei-ws
======

Wrapper for the federation Equestre Internationale(FEI) Results Provider Web Service.
Works both with and without Django.

Only the new versions of the FEI web services are implemented.
It is known as FEIWSClient.
To use the clients supply your username and password when initializing the object or set FEI_WS_USERNAME and FEI_WS_PASSWORD in django config.
Data is returned, as is. No interpretation except for minor exception handling is used on the responses.

You can now access entries from the FEI online entry system. The XML from this service is converted to dictionaries.
The new FEI Entry System V3 API is now also supported via the FEIEntrySystem3Client.
Only a subset of all calls are implemented.