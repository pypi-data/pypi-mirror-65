from .Base import Base
from .JsonEnum import JsonEnum
from .utils import String
from .FileFormatSettings import FileFormatSettings

class CsvQuoteStyle(JsonEnum):
    Csv = "QuoteStyle.Csv"
    None_ = "QuoteStyle.None"


class CsvStyle(JsonEnum):
    QuoteAlways = "CsvStyle.QuoteAlways"
    QuoteAfterDelimiter = "CsvStyle.QuoteAfterDelimiter"


class CsvFormatSettings(FileFormatSettings):
    def __init__(self, schema=[]):
        self.schema = schema + [
            SchemaEntry("columnHeaders", bool, False),
            SchemaEntry("delimiter", String, ","),
            SchemaEntry("quoteStyle", CsvQuoteStyle, CsvQuoteStyle.Csv),
            SchemaEntry("csvStyle", CsvStyle, CsvStyle.QuoteAlways),
        ]
        super().__init__(self.schema)
