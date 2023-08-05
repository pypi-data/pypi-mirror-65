from .DateTime import DateTime
from .Extension import Extension
from .Status import Status
from .Location import Location
from .LatLng import LatLng


class Argument(dict):
    """
    {
      "name": string,
      "rawText": string,
      "textValue": string,
      "status": {
        object(Status)
      },

      // Union field value can be only one of the following:
      "intValue": string,
      "floatValue": number,
      "boolValue": boolean,
      "datetimeValue": {
        object(DateTime)
      },
      "placeValue": {
        object(Location)
      },
      "extension": {
        "@type": string,
        field1: ...,
        ...
      },
      "structuredValue": {
        object
      }
      // End of list of possible types for union field value.
    }
    """

    # TODO Argument object needs to be completed.
    def __init__(self, name: str = '', raw_text: str = '', text_value: str = '', status: Status = None,
                 int_value: str = '',
                 float_value: str = '', bool_value: bool = False, datetime_value: str = '',
                 place_value: Location = None,
                 extension: Extension = None, **structure_values):
        super().__init__()

        if name is not None:
            self['name'] = name
        if raw_text is not None:
            self['rawText'] = raw_text
        if text_value is not None:
            self['textValue'] = text_value
        if status is not None:
            self['status'] = status
        if int_value is not None:
            self['intValue'] = int_value
        if float_value is not None:
            self['floatValue'] = float_value
        if bool_value is not None:
            self['boolValue'] = bool_value
        if datetime_value is not None:
            self['datetimeValue'] = datetime_value
        if place_value is not None:
            self['placeValue'] = place_value
        if extension is not None:
            self['extension'] = extension
        if structure_values is not None:
            self['structuredValue'] = structure_values

    def add_status(self, code: int, message: str, status_type: str, **fields) -> Status:
        self['status'] = Status(code=code, message=message, type=status_type, **fields)
        return self['status']

    def add_datetimevalue(self, date: str, time: str) -> DateTime:
        self['datetimeValue'] = DateTime(date=date, time=time)
        return self['datetimeValue']

    def add_place_value(self, coordinates: LatLng = None, formatted_address: str = '', zip_code: str = '',
                        city: str = '',
                        postal_address: str = '', name: str = '', phone_number: str = '', notes: str = '',
                        place_id: str = '') -> Location:
        self['placeValue'] = Location(coordinates=coordinates, formatted_address=formatted_address,
                                      zip_code=zip_code, city=city, postal_address=postal_address, name=name,
                                      phone_number=phone_number, notes=notes, place_id=place_id)
        return self['placeValue']

    def add_extension(self, extension_type: str, **kwargs) -> Extension:
        self['extension'] = Extension(extension_type, **kwargs)
        return self['extension']

    def add_structure(self, **kwargs) -> dict:
        self['structuredValue'] = kwargs
        return self['structuredValue']
