# KF pubsub

JsonFieldFilter and JsonFieldSearchFilter implementation with django and django rest framework

## Installation

### With requirements.txt

Add the following line in your `requirements.txt` file:

```
kfjsonfilter
```

### With PIP

```bash
$ pip install kfjsonfilter
```

## Getting Started

There are implemented two base filters: JsonFieldFilter and JsonFieldSearchFilter.

### JsonFieldFilter

Allow create a data filter from a json object. Its neccesary to declare two elements in the django rest framework viewset: json_field and json_filters


|   | TYPE | DESCRIPTION |
| :------------ |:---------------:| :-----|
| json_field      | string | Indicates the json field object form the model |
| json_filters      | list of dicts        |   Indicates the field thats allow filter and lookup type for each type |

#### json_filters structure

Allows filter by any value from a json data. Each element must be included in a dictionary with to key: field and lookup.

	json_filters = [{'field': <field_name>, 'lookup': <lookup>}, ...]

|   | DESCRIPTION |
| :------------ |:---------------|
| field      | field_name is the name of the element to filter included in json data |
| lookup      | lookup is the filter type, icontains, iexact, in, etc... and date_range (to filter by a date range). to filter only a date by a date indicates only lte, gte, exact...        |  


### JsonFieldSearchFilter

Allow create a data filter and search filter from a json object. Its neccesary to declare three elements in the django rest framework viewset: json_field and search_fields


|   | TYPE | DESCRIPTION |
| :------------ |:-----------------------:| :-----|
| json_field      | string         | Indicates the json field object form the model |
| json_filters      | list of dicts                |   Indicates the field thats allow filter by a field and lookup type for each type |
| search_fields      | list of dicts                |   Indicates the field thats allow search by a field and lookup type for each type |

#### json_filters and search_fields structure

Allows filter/search by any value from a json data. Each element must be included in a dictionary with to key: field and lookup.

	json_filters = [{'field': <field_name>, 'lookup': <lookup>}, ...]

|   | DESCRIPTION |
| :------------ |:---------------|
| field      | field_name is the name of the element to filter included in json data |
| lookup      | lookup is the filter type, icontains, iexact, in, etc... and date_range (to filter by a date range). to filter only a date by a date indicates only lte, gte, exact...        |  

Also, when lookup is 'date_range' field_name must finish with []

### Example

#### Django Model

	class MyModel(models.Model):
		data = JSONField(default=dict)


```
For example:
data = {'creation_date': '2020-01-01', 'total': 3, 'name': 'Pedro Miguel'}
```

#### Django Rest Framework View

	class MyModelViewSet(ListAPIView):
		queryset = MyModel.objects.all()
		filter_backends = [JsonFieldFilter, DjangoFilterBackend, OrderingFilter]
		json_field = 'data'
		json_filters = [{'field': 'creation_date', 'lookup': 'date_range'}, {'field': 'total', 'lookup': 'gte'}]

	or

	class MyModelViewSet(ListAPIView):
		queryset = MyModel.objects.all()
		filter_backends = [JsonFieldSearchFilter, DjangoFilterBackend, OrderingFilter]
		json_field = 'data'
		json_filters = [{'field': 'creation_date', 'lookup': 'lte'}, {'field': 'total', 'lookup': 'gte'}]	
		search_fields = [{'field': 'name', 'lookup': 'icontains'}]	

