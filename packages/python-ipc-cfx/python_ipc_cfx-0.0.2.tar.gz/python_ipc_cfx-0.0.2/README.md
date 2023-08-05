# python_ipc_cfx

Python implementation of the IPC CFX standard http://www.connectedfactoryexchange.com/CFXDemo/sdk/html/R_Project_CFXSDK.htm

**This package is in its very early development stage, and should not be relied upon at this time. Many features are missing, and backwards compatibility between releases is not guaranteed.**

`python_ipc_cfx` is compatible with Python3, and tested with Python3.7.

## CFX Classes

`python_ipc_cfx` ships with support for the IPC CFX classes defined in the reference CFXDemo document linked to previously. Furthermore, it makes use of the flexibility of Python to allow powerful templating. Example:

```python
from cfx.Production.TestAndInspection import UnitsInspected

# Sane defaults that fit the IPC CFX spec
u = UnitsInspected()
u.as_dict()
>> {
    'inspected_units': [],
    'inspection_method': 'Human',
    'inspector': {'actor_type': 'Human',
                'first_name': None,
                'last_name': None,
                'login_name': None,
                'operator_identifier': None},
    'sampling_information': {'lot_size': None,
                            'sample_size': None,
                            'sampling_method': 'NoSampling'},
    'transaction_id': 'f18a291e-5329-4098-a1ab-21eb4fdfcc8f'
}

# Simple yet powerful templating engine
from cfx.Structures import TestResult
template = {
    'inspected_units': [{"inspections": {"result": TestResult.Failed}}]
}
u = UnitsInspected(**template)
u.as_dict()
>>
{
    'inspected_units': [{'inspections': [{'comments': '',
                                    'defects_found': [{'comments': None,
                                                        'component_of_interest': None,
                                                        'confidence_level': 100.0,
                                                        'defect_category': None,
                                                        'defect_code': '',
                                                        'defect_images': [],
                                                        'description': '',
                                                        'priority': 1,
                                                        'region_of_interest': None,
                                                        'related_measurements': []}],
                                    'error': '',
                                    'inspection_end_time': None,
                                    'inspection_name': '',
                                    'inspection_start_time': None,
                                    'measurements': [{'crds': None,
                                                        'expected_value': True,
                                                        'measurement_name': '',
                                                        'result': True,
                                                        'sequence': None,
                                                        'time_recorded': None,
                                                        'unique_identifier': '6cde98ccd9294b62bc8726887dae7942',
                                                        'value': True}],
                                    'result': TestResult: Failed,
                                    'symptoms': [],
                                    'test_procedure': '',
                                    'unique_identifier': '3424d105-afef-480e-8e89-d41cac5d6788'}],
                    'overall_result': TestResult: Passed,
                    'unit_identifier': 'b86056c1-1b83-420b-816f-ce10d5c4b21d',
                    'unit_position_number': None}],
    'inspection_method': InspectionMethod: Human,
    'inspector': {'actor_type': ActorType: Human,
            'first_name': None,
            'last_name': None,
            'login_name': None,
            'operator_identifier': None},
    'sampling_information': {'lot_size': None,
                        'sample_size': None,
                        'sampling_method': SamplingMethod: NoSampling},
    'transaction_id': '28ecc1be-29cd-419c-a029-4d897cff9c34'
}
```

## CFX Structures and Enums

`python_ipc_cfx` makes use of various helper functions and classes defined in `cfx/Structures/base.py`, some of which have specific overriden behaviour compared to standard Python. Some examples:

```python
# CFXEnum-specific quirks
from cfx.Structures import TestResult
t = TestResult.Passed
str(t)  # 'Passed'
t  # In an interactive shell, will output TestResult: Passed
d = TestResult.default()  # TestResult.Passed . This takes the value of the Enum corresponding to 0

# CFXStructure-specific quirks
from cfx.Structures import Operator
o = Operator()
str(o)  # '{"actor_type": "Human", "first_name": null, "last_name": null, "login_name": null, "operator_identifier": null}'
o.as_dict()
>>
{
    'actor_type': ActorType: Human,
    'first_name': None,
    'last_name': None,
    'login_name': None,
    'operator_identifier': None
}
```

## Testing

Testing is done with `tox`. Make sure you have Python3.7 installed on your system.

```bash
pip install -r requirements_test.txt
tox
```

## Building and releasing

You will need to provided the following environment variables:

- `PYPI_USER`: PyPi user
- `PYPI_PASS`: PyPi password
- `SLACK_WEB_HOOK`: Incoming webhook for Arch's Slack integration

```bash
pip install -r requirements_build.txt
python3 scripts/release.py --check vX.Y.Z
# Double check that this output matches what you expected.
python3 scripts/release.py vX.Y.Z
```
