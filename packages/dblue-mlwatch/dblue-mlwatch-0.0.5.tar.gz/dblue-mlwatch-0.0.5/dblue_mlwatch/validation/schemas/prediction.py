PREDICTION_SCHEMA = {
    'features': {
        'type': 'dict',
        'required': True,
    },
    'prediction': {
        'type': ['number', 'boolean', 'string'],
        'required': True,
    },
    'prediction_probs': {
        'type': 'dict',
        'nullable': True,
    },
    'unique_id': {
        'type': 'string',
        'nullable': True
    },
}
