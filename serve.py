"""Streamable-HTTP entrypoint for the GA4 MCP server on Railway."""

import os
import tempfile

# Write the service-account JSON from env into a file so google-auth can find it.
creds_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if creds_json:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tf:
        tf.write(creds_json)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = tf.name

from ga4_mcp.coordinator import mcp
from ga4_mcp.tools import metadata, reporting

property_id = os.environ.get("GA4_PROPERTY_ID")
if property_id:
    schema = metadata.get_property_schema_uncached(property_id)
    metadata.PROPERTY_SCHEMA = schema
    reporting.PROPERTY_SCHEMA = schema

mcp.settings.host = "0.0.0.0"
mcp.settings.port = int(os.environ.get("PORT", "8080"))
mcp.settings.transport_security.enable_dns_rebinding_protection = False

mcp.run(transport="streamable-http")
