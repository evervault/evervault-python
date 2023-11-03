---
"evervault-python": major
---

Migrated Function run requests to new API.

We have released a new API for Function run requests which is more robust, more extensible, and which provides more useful error messages when Function runs fail. This change migrates all Function run requests to the new API. In addition, we have removed async Function run requests and specifying the version of the Function to run. For more details check out https://docs.evervault.com/sdks/python#run()
