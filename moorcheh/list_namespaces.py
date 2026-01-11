# Debug script

from moorcheh.client import client

namespaces = client.namespaces.list()
print("Namespaces visible to this API key:")
print(namespaces)
