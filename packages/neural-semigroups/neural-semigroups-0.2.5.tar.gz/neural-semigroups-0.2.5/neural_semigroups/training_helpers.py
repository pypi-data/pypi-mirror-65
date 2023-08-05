"""
   Copyright 2019-2020 Boris Shminke

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import logging
from argparse import ArgumentParser, Namespace
from time import time
from typing import Dict, Tuple, Union

import numpy as np
import torch
from ignite.engine import Engine, Events, create_supervised_trainer
from ignite.handlers import EarlyStopping
from ignite.metrics.loss import Loss
from torch.nn import Module
from torch.optim import Adam
from torch.utils.data import DataLoader, TensorDataset
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

from neural_semigroups.cayley_database import CayleyDatabase
from neural_semigroups.constants import CURRENT_DEVICE
from neural_semigroups.magma import Magma


def load_database_as_cubes(
        cardinality: int,
        train_size: int,
        validation_size: int
) -> Tuple[
    np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray
]:
    """
    load a database file to probability cubes representation

    :param cardinality: cardinality of Cayley database (from ``smallsemi``) to read
    :param train_size: number of tables for training
    :param validation_size: number of tables for validation
    :returns: three arrays of probability Cayley cubes (train, validation, test
    ) and three arrays of labels for them
    """
    cayley_db = CayleyDatabase(cardinality)
    logging.info("reading data from disk")
    logging.info("splitting by train and test")
    train, validation, test = cayley_db.train_test_split(
        train_size, validation_size
    )
    train_cubes = list()
    for cayley_table in tqdm(train.database, desc="generating train cubes"):
        train_cubes.append(Magma(cayley_table).probabilistic_cube)
    validation_cubes = list()
    for cayley_table in tqdm(validation.database, desc="generating validation cubes"):
        validation_cubes.append(Magma(cayley_table).probabilistic_cube)
    test_cubes = list()
    for cayley_table in tqdm(test.database, desc="generating test cubes"):
        test_cubes.append(Magma(cayley_table).probabilistic_cube)
    return (
        np.stack(train_cubes), np.stack(validation_cubes),
        np.stack(test_cubes), train.labels, validation.labels, test.labels
    )


def get_arguments() -> Namespace:
    """
    parse script arguments


    :returns: script parameters
    """
    parser = ArgumentParser()
    parser.add_argument(
        "--cardinality",
        type=int,
        help="magma cardinality",
        required=True,
        choices=range(2, 8)
    )
    parser.add_argument(
        "--epochs",
        type=int,
        help="number of epochs to train",
        default=100,
        required=False
    )
    parser.add_argument(
        "--learning_rate",
        type=float,
        help="learning rate",
        default=0.001,
        required=False
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        help="batch size for training",
        default=32,
        required=False
    )
    parser.add_argument(
        "--train_size",
        type=int,
        help="number of tables for training",
        required=True
    )
    parser.add_argument(
        "--validation_size",
        type=int,
        help="number of tables for validation",
        required=True
    )
    return parser.parse_args()


def learning_pipeline(
        params: Dict[str, Union[int, float]],
        model: Module,
        evaluator: Engine,
        loss: Loss,
        data_loaders: Tuple[DataLoader, DataLoader],
) -> None:
    """
    run a comon learning pipeline

    :param params: parameters of learning: epochs, learning_rate.
                   Cardinality also goes here
    :param model: a network architecture
    :param evaluator: an ``ignite`` engine which evaluates the model's quality
    :param loss: the criterion to optimize
    :oaram data_loader: train and validation data loaders
    """
    logging.info("data prepared")
    optimizer = Adam(
        model.parameters(),
        lr=params["learning_rate"]
    )
    trainer = create_supervised_trainer(model, optimizer, loss)

    def score_function(engine):
        val_loss = engine.state.metrics["loss"]
        return -val_loss
    handler = EarlyStopping(
        patience=100, score_function=score_function, trainer=trainer
    )
    evaluator.add_event_handler(Events.COMPLETED, handler)
    writer = SummaryWriter()
    logger = logging.getLogger("training")
    @trainer.on(Events.EPOCH_COMPLETED)
    # pylint: disable=unused-variable
    def log_training_results(trainer):
        evaluator.run(data_loaders[0])
        # pylint: disable=no-member
        for metric in evaluator.state.metrics.keys():
            writer.add_scalars(
                metric,
                # pylint: disable=no-member
                {"training": evaluator.state.metrics[metric]},
                global_step=trainer.state.iteration,
                walltime=int(time())
            )

    @trainer.on(Events.EPOCH_COMPLETED)
    # pylint: disable=unused-variable
    def log_validation_results(trainer):
        evaluator.run(data_loaders[1])
        # pylint: disable=no-member
        for metric in evaluator.state.metrics.keys():
            writer.add_scalars(
                metric,
                # pylint: disable=no-member
                {"validation": evaluator.state.metrics[metric]},
                global_step=trainer.state.iteration,
                walltime=int(time())
            )
        # pylint: disable=no-member
        logger.debug(evaluator.state.metrics["loss"])
        torch.save(model, f"semigroups.{params['cardinality']}.model")
    logging.info("training started")
    trainer.run(data_loaders[0], max_epochs=params["epochs"])


def get_loaders(
        cardinality: int,
        batch_size: int,
        train_size: int,
        validation_size: int,
        use_labels: bool = False
) -> Tuple[DataLoader, DataLoader]:
    """
    get train and validation data loaders

    :param cardinality: the cardinality of a ``smallsemi`` database
    :param batch_size: batch size (common for train and validation)
    :param train_size: number of tables for training
    :param validation_size: number of tables for validation
    :param use_labels: whether to set a target as labels from database (for
    classifier) or to use X's as labels (for autoencoder)
    :returns: a pair of train and validation data loaders
    """
    (
        train, validation, _,
        train_labels, validation_labels, _
    ) = load_database_as_cubes(
        cardinality, train_size, validation_size
    )
    train_tensor = torch.from_numpy(train).to(CURRENT_DEVICE)
    val_tensor = torch.from_numpy(validation).to(CURRENT_DEVICE)
    if use_labels:
        train_data = TensorDataset(
            train_tensor, torch.from_numpy(train_labels).to(CURRENT_DEVICE)
        )
        val_data = TensorDataset(
            val_tensor, torch.from_numpy(validation_labels).to(CURRENT_DEVICE)
        )
    else:
        train_data = TensorDataset(train_tensor, train_tensor)
        val_data = TensorDataset(val_tensor, val_tensor)
    return (
        DataLoader(train_data, batch_size=batch_size, shuffle=True),
        DataLoader(val_data, batch_size=batch_size, shuffle=True)
    )
