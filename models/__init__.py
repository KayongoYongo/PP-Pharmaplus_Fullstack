from models.engine.db import DB

# Create a storage instance
storage = DB()

# Reload the database
storage.reload()