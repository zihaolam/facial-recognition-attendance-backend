from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, DiscriminatorAttribute
import config


class BaseModel(Model):
    class Meta:
        table_name = "ab3-attendance-main-table"
        region = "ap-southeast-1"
        if config.STAGE == "dev":
            host = "http://localhost:8392"

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    type = DiscriminatorAttribute()
