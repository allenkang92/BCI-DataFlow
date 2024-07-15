import matplotlib.pyplot as plt
from .filters import bandpass_filter, notch_filter
from .artifact_removal import ica_artifact_removal

def apply_preprocessing(data, preprocessor):
    steps = preprocessor.steps.order_by('order')
    processed_data = data.copy()
    
    for step in steps:
        if step.step_type == 'bandpass_filter':
            processed_data = bandpass_filter(processed_data, **step.parameters)
        elif step.step_type == 'notch_filter':
            processed_data = notch_filter(processed_data, **step.parameters)
        elif step.step_type == 'ica_artifact_removal':
            processed_data = ica_artifact_removal(processed_data, **step.parameters)
    
    return processed_data

def visualize_preprocessing(original_data, processed_data):
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(original_data)
    plt.title('Original Data')
    plt.subplot(2, 1, 2)
    plt.plot(processed_data)
    plt.title('Processed Data')
    plt.tight_layout()
    return plt