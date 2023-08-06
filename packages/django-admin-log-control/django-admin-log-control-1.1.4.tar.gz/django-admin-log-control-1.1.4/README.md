Control your django admin panel logs(LogEntry)

# CustomModelAdmin
In admin.py for all apps, instead of admin.ModelAdmin use admintools.models.CustomModelAdmin:

```python
from django.contrib import admin
from admintools.models import CustomModelAdmin
import admintools.admin

@admin.register
class Polls(CustomModelAdmin):

```

