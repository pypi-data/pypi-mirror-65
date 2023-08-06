import logging
import numpy as np
import torch

from eisen_cli.utils import json_file_to_dict, import_string
from eisen.utils import EisenModuleWrapper

from torchvision.transforms import Compose
from torch.utils.data import DataLoader


SUPPORTED_PHASES = ['Training', 'Validation']


def eisen_training(configuration, epochs, data_dir, artifacts_dir, resume):
    """
    :param configuration: path of configuration file for the job
    :type configuration: str
    :param epochs: number of epochs requested for training
    :type epochs: int
    :param data_dir: base path for the data of this job
    :type data_dir: str
    :param artifacts_dir: base path for the artifacts of this job
    :type artifacts_dir: str
    :param resume: use pre-existing artifacts to resume training
    :type resume: bool
    :return: None
    """

    # Read configuration which is stored in JSON format

    configuration_dictionary = json_file_to_dict(configuration)

    # Getting hyperparameters

    hyperparameters = configuration_dictionary['General'].get('Hyperparameters', {})

    model = configuration_dictionary['General'].get('Models')[0]

    batch_size = 4
    num_workers = 4

    for entry in hyperparameters:
        if entry['type'] == '.BatchSize':
            batch_size = entry['params']['value']

        if entry['type'] == '.NumWorkers':
            num_workers = entry['params']['value']

        if entry['type'] == '.Seed':
            np.random.seed(entry['params']['value'])
            torch.manual_seed(entry['params']['value'])

    # For each phase of the workflow [training, validation, testing]

    workflows = {}

    hooks = []

    for phase in [key for key in configuration_dictionary.keys() if key in SUPPORTED_PHASES]:
        logging.info('INFO: setting up everything relative to {}'.format(phase))

        # For each subsection in the configuration do appropriate actions
        phase_dictionary = configuration_dictionary[phase]

        # TRANSFORMS
        # instantiate transforms for the data and combine them together

        logging.info('INFO: setting up transforms...')

        readers_list = []

        for reader in phase_dictionary['Readers']:
            logging.debug('DEBUG: setting up readers type {}'.format(reader['type']))

            transform_object = import_string(reader['type'])
            readers_list.append(transform_object(data_dir=data_dir, **reader['params']))

        reader = Compose(readers_list)

        transform_list = []

        for transform in phase_dictionary['Transforms']:
            logging.debug('DEBUG: setting up transform type {}'.format(transform['type']))

            transform_object = import_string(transform['type'])
            transform_list.append(transform_object(**transform['params']))

        transform = Compose(transform_list)

        data_pipeline = Compose([reader, transform])

        # DATA
        # Instantiate data-sets and relative data loaders <torch.utils.DataLoader>

        logging.info('INFO: setting up the dataset...')

        dataset_object = import_string(phase_dictionary['Datasets'][0]['type'])

        dataset = dataset_object(
            transform=data_pipeline,
            data_dir=data_dir,
            **phase_dictionary['Datasets'][0]['params']
        )

        data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)

        # MODEL
        # Instantiate network

        logging.info('INFO: setting up the model...')

        model_object = import_string(model['type'])

        model = EisenModuleWrapper(module=model_object, **model['params'])

        # Instantiate metrics

        logging.info('INFO: setting up the metrics...')

        metrics = []

        for metric in phase_dictionary['Metrics']:
            logging.debug('DEBUG: setting up metric type {}'.format(metric['type']))

            metric_object = import_string(metric['type'])

            metrics.append(EisenModuleWrapper(module=metric_object, **metric['params']))

        losses = None
        optimizer = None

        if phase == 'Training':
            # Instantiate losses

            logging.info('INFO: setting up the losses...')

            losses = []

            for loss in phase_dictionary['Losses']:
                logging.debug('DEBUG: setting up loss type {}'.format(loss['type']))

                loss_object = import_string(loss['type'])

                losses.append(EisenModuleWrapper(module=loss_object, **loss['params']))

            # Instantiate optimizer

            logging.info('INFO: setting up the optimizer...')

            optimizer_object = import_string(phase_dictionary['Optimizer'][0]['type'])

            optimizer = optimizer_object(params=model.parameters(), **phase_dictionary['Optimizer'][0]['params'])

        # WORKFLOW
        # Instantiate work-flows

        logging.info('INFO: setting up the metrics...')

        workflow_object = import_string(phase_dictionary['Workflow'][0]['type'])

        workflow = workflow_object(
            model=model,
            losses=losses,
            optimizer=optimizer,
            metrics=metrics,
            data_loader=data_loader,
            **phase_dictionary['Workflow'][0]['params'],
        )

        workflows[phase] = workflow

        # HOOKS
        # Instantiate Hooks
        logging.info('INFO: setting up the Hooks...')

        for hook in phase_dictionary['Hooks']:
            logging.debug('DEBUG: setting up hook type {}'.format(hook['type']))

            hook_object = import_string(hook['type'])

            hooks.append(hook_object(workflows[phase].id, phase, artifacts_dir, **hook['params']))

    # RUN
    # run training for the requested number of epochs

    logging.info('INFO: running workflows...')

    training_context = workflows.get('Training', None)
    validation_context = workflows.get('Validation', None)

    for epoch in range(epochs):
        logging.info('INFO: running TRAINING epoch {}'.format(epoch))
        training_context.run()

        if validation_context:
            logging.info('INFO: running VALIDATION epoch {}'.format(epoch))

            validation_context.run()
