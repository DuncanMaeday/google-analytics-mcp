import os                                                                                                                                                                                                 
  import sys                                                                                                                                                                                                
  import tempfile                                                                                                                                                                                           
                                                                                                                                                                                                            
  # Write JSON credentials to a temp file so ga4_mcp can find them                                                                                                                                          
  creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")                                                                                                                                             
  if creds_json:  
      tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
      tmp.write(creds_json)                                                                                                                                                                                 
      tmp.close()
      os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = tmp.name                                                                                                                                               
                  
  from ga4_mcp.coordinator import mcp                                                                                                                                                                       
  from ga4_mcp.tools import metadata, reporting
                                                                                                                                                                                                            
  property_id = os.getenv("GA4_PROPERTY_ID")
  if not property_id:
      print("ERROR: GA4_PROPERTY_ID not set", file=sys.stderr)
      sys.exit(1)                                                                                                                                                                                           
   
  schema = metadata.get_property_schema_uncached(property_id)                                                                                                                                               
  metadata.PROPERTY_SCHEMA = schema
  reporting.PROPERTY_SCHEMA = schema

  port = int(os.environ.get("PORT", 8080))                                                                                                                                                                  
  mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
