import os
import sys
import inspect
import time
import uuid
from functools import partial
import numpy as np
import random
import tensorflow as tf
from tensorflow.python.eager import context, tape, function
from tensorflow.python.eager.backprop import GradientTape
from tensorflow.python.keras import backend
from tensorflow.python.ops.losses import util as tf_losses_utils
from tensorflow.python.keras.utils import losses_utils
from tensorflow.python.keras.engine import training_utils
from tensorflow.python.client import device_lib
from .tensorflow_optimizers import get_optimizer
from .tensorflow_regularizers import *

from .tensorflow_constraints import get_constraint
from .tensorflow_losses import *
from .tensorflow_metrics import get_metric
from ..misc.visualization_utils import tile_rgb_images, loss_metric_curve
from ..callbacks import *
from ..callbacks.lr_schedulers import get_lr_scheduler
from .trainers import ModelBase, OptimizerBase, progress_bar
from ..backend.common import *
from ..backend.tensorflow_backend import Input, Sequential, to_numpy, to_tensor, print_summary
from ..data.image_common import *

__all__ = ['Model', 'ImageClassificationModel', 'ImageDetectionModel', 'ImageSegmentationModel', 'LanguageModel']

_device = 'CPU'
for device in device_lib.list_local_devices():
    if tf.DeviceSpec.from_string(device.name).device_type == 'GPU':
        _device = 'GPU'
        break


def _to_tuple(x):
    if isinstance(x, tuple):
        return x
    elif isinstance(x, list):
        return tuple(x)
    else:
        return x,


class Model(ModelBase):
    def __init__(self, inputs=None, output=None, input_shape=None):
        super(Model, self).__init__(inputs, output, input_shape)

    def _initial_graph(self, inputs=None, output=None, input_shape=None):
        input_var = inputs
        out_var = output
        if output is None:
            raise ValueError('There is at least one output')

        if inputs is None:
            if input_shape is None:
                pass
            else:
                input_shape = tuple(to_list(input_shape))
                input_name = 'input_{0}'.format(len(self.inputs) + 1)
                input_var = tf.keras.Input(input_shape)
                # input_var = Input(input_shape, name=input_name)
                self.inputs[input_name] = input_shape
        elif inputs is tf.keras.layers.InputLayer:
            self.inputs[inputs.__name__] = tf.keras.backend.int_shape(inputs.input_shape)

        elif isinstance(inputs, (tuple, list)):
            for inp in inputs:
                if isinstance(inp, tf.keras.Input):
                    input_name = inp.name if inp.name != '' else 'input_{0}'.format(len(self.inputs) + 1)
                    self.inputs[input_name] = tf.keras.backend.int_shape(inp.input_shape)
        elif isinstance(inputs, dict):
            input_var = list(inputs.values())
            for k, v in inputs.items():
                if isinstance(v, tf.keras.Input):
                    self.inputs[k] = tf.keras.backend.int_shape(v.input_shape)

        if isinstance(out_var, Sequential):
            model = tf.keras.Model(input_var, out_var)
            dummay_input = np.random.standard_normal((2, *input_shape)).astype(np.float32)
            out = out_var(dummay_input)
            out_var._set_inputs(dummay_input)
            self._model = out_var
            if isinstance(out, tuple):
                for i in range(len(out)):
                    self.targets[self._model.output_names[i]] = list(to_numpy(out[i]).shape[1:])
            else:
                self.targets[self._model.output_names[0]] = list(to_numpy(out).shape[1:])
        else:
            model = tf.keras.Model(input_var, out_var)
            dummay_input = np.random.standard_normal((2, *input_shape)).astype(np.float32)
            out = model(dummay_input)
            model._set_inputs(dummay_input)
            self._model = model
            if isinstance(out, tuple):
                for i in range(len(out)):
                    self.targets[self._model.output_names[i]] = list(to_numpy(out[i]).shape[1:])
            else:
                self.targets[self._model.output_names[0]] = list(to_numpy(out).shape[1:])

        self.device = _device
        self.training_context['current_model'] = self._model
        return self

    def train(self):
        tf.keras.backend.set_learning_phase(1)
    def eval(self):
        tf.keras.backend.set_learning_phase(0)

    @property
    def layers(self):
        return self._model.layers

    #
    # def complie(self, optimizer, losses=None, metrics=None, loss_weights=None, sample_weight_mode=None,
    #             weighted_metrics=None, target_tensors=None):
    #     self.with_optimizer(optimizer)
    #     if losses is not None and isinstance(losses, (list, tuple)):
    #         for loss in losses:
    #             self.with_loss(loss)
    #     if metrics is not None and isinstance(metrics, (list, tuple)):
    #         for metric in metrics:
    #             self.with_metric(metric)
    #
    #     return self

    def with_optimizer(self, optimizer, **kwargs):
        if 'lr' in kwargs:
            lr = kwargs['lr']
            kwargs['learning_rate'] = lr
            kwargs.pop('lr')
        if isinstance(optimizer, str):
            optimizer_class = get_optimizer(optimizer)
            self.optimizer = optimizer_class(**kwargs)

        else:
            self.optimizer = optimizer(**kwargs)

        self.base_lr = kwargs.get('lr', kwargs.get('learning_rate', 1e-3))
        self.training_context['optimizer'] = self.optimizer
        self.training_context['base_lr'] = self.base_lr
        self.training_context['current_lr'] = self.base_lr
        return self

    def with_loss(self, loss, loss_weight=1, output_idx=0, name='', **kwargs):
        if isinstance(loss, str):
            loss = get_loss(loss)
        alias = name
        if inspect.isclass(loss):
            alias = loss.__name__ if len(alias) == 0 else alias
        if len(alias) == 0 and hasattr(loss, '__name__'):
            alias = loss.__name__
        with backend.name_scope(alias):
            if inspect.isclass(loss):
                # keras (y_true,y_pred)
                self._losses[alias] = loss(**kwargs)
            elif callable(loss):
                self._losses[alias] = loss
        return self

    def with_metric(self, metric, output_idx=0, name='', **kwargs):
        if isinstance(metric, str):
            metric = get_metric(metric)
        alias = name
        if inspect.isfunction(metric):
            alias = metric.__name__ if len(alias) == 0 else alias
        if len(alias) == 0 and hasattr(metric, 'name'):
            alias = metric.name
        with backend.name_scope(alias):
            if inspect.isclass(metric):
                # keras (y_true,y_pred)
                self._metrics[alias] = metric(**kwargs)
            elif callable(metric):
                self._metrics[alias] = metric
        return self

    def with_regularizer(self, reg, **kwargs):
        if reg is None:
            return self
        reg_fn = None
        alias = None
        if isinstance(reg, str):
            reg_fn = get_reg(reg)
            alias = reg_fn.__name__
        elif reg is callable:
            reg_fn = reg
            alias = reg_fn.__name__

        args = reg_fn.__code__.co_varnames
        if 'reg_weight' in args:
            if 'model' in args:
                self._model_regs[alias + '_Loss'] = partial(reg_fn, **kwargs)

            elif 'output' in args:
                self._output_regs[alias + '_Loss'] = partial(reg_fn, **kwargs)
        return self

    def with_constraint(self, constraint, **kwargs):
        if constraint is None:
            return self
        constraint_fn = None
        if isinstance(constraint, str):
            constraint_fn = get_constraint(constraint)
        elif inspect.isfunction(constraint):
            constraint_fn = constraint

        print(constraint.__qualname__)
        if hasattr(constraint_fn, 'forward') and constraint_fn.__name__[-4:] == 'norm':
            self._constraints[constraint_fn.__name__] = constraint_fn(**kwargs)

        elif callable(constraint_fn) and constraint_fn.__name__[-4:] == 'norm':
            self._constraints[constraint_fn.__name__] = partial(constraint_fn, **kwargs)

        return self

    def with_learning_rate_scheduler(self, lr_schedule, warmup=0, **kwargs):
        if lr_schedule is None:
            return self
        if isinstance(lr_schedule, str):
            lr_schedule = get_lr_scheduler(lr_schedule)
        if callable(lr_schedule):
            self.lr_scheduler = lr_schedule(**kwargs)
            self.callbacks.append(self.lr_scheduler)
        self.warmup = warmup
        if self.warmup > 0:
            self.optimizer.adjust_learning_rate(1e-5, False)
            self.training_context['current_lr'] = 1e-5
        return self

    def with_model_save_path(self, save_path, **kwargs):
        self.save_path = make_dir_if_need(save_path)
        self.training_context['save_path'] = self.save_path
        return self

    def adjust_learning_rate(self, lr, verbose=True):
        new_lr = lr
        old_lr = self.optimizer.lr
        self.optimizer._set_hyper('learning_rate', new_lr)
        self.training_context['current_lr'] = new_lr
        if verbose and old_lr != new_lr:
            if verbose:
                print('learning rate changed! ( form {0:.3e} to {1:.3e})'.format(old_lr, new_lr))

    def do_on_training_start(self):
        # self._model.compile(self.optimizer,loss={**self._losses, **self._model_regs,**self._output_regs},
        # metrics=self._metrics,loss_weights=self.loss_weights)
        tf.keras.backend.set_learning_phase(1)
        tf.executing_eagerly()
        self._model.run_eagerly = True

    def do_on_training_end(self):
        tf.keras.backend.set_learning_phase(0)

    def do_on_epoch_start(self):
        if self.training_context['current_epoch'] < self.warmup:
            lr = 1e-5 * (self.training_context['current_epoch'] + 1)
            self.adjust_learning_rate(lr, False)
        elif self.training_context['current_epoch'] == self.warmup:
            self.adjust_learning_rate(self.base_lr, False)

    def do_on_epoch_end(self):
        if self.training_context['current_epoch'] < self.training_context['total_epoch'] - 1:
            if self.training_context['current_epoch'] > self.warmup:

                if self.optimizer.lr < 1e-8:
                    self.optimizer.adjust_learning_rate(0.05 * self.base_lr, True)
            elif self.warmup > 0 and self.training_context['current_epoch'] == self.warmup:
                self.optimizer.adjust_learning_rate(self.base_lr, True)
                self.training_context['current_lr'] = self.base_lr
            elif self.warmup > 0 and self.training_context['current_epoch'] < self.warmup:
                self.optimizer.adjust_learning_rate(1e-5 * (self.training_context['current_epoch'] + 1), True)
                self.training_context['current_lr'] = 1e-5 * (self.training_context['current_epoch'] + 1)

    def do_on_batch_end(self):
        if self.training_context['current_batch'] == 0 and self.training_context['current_epoch'] == 0:
            print(self.training_context['losses'])


    def do_on_data_received(self, train_data, test_data):
        input = None
        target = None
        test_input = None
        test_target = None
        if 'signature' in self.training_context and len(self.training_context['signature']) > 0:
            data_feed = self.training_context['signature']
            input = to_tensor(train_data[data_feed.get('input')]) if data_feed.get('input') >= 0 else None
            target = to_tensor(train_data[data_feed.get('target')]) if data_feed.get('target') >= 0 else None
            if test_data is None:
                test_data = train_data
            test_input = to_tensor(test_data[data_feed.get('input')]) if data_feed.get('input') >= 0 else None
            test_target = to_tensor(test_data[data_feed.get('target')]) if data_feed.get('target') >= 0 else None

        else:
            data_feed = OrderedDict()
            data_feed['input'] = -1
            data_feed['target'] = -1
            inshapes = self.inputs.value_list
            outshapes = self.targets.value_list

            if train_data is not None:
                if len(train_data) == 1:
                    input = to_tensor(train_data[0])
                    target = to_tensor(train_data[0].copy())
                    data_feed['input'] = 0
                    data_feed['target'] = 0
                else:
                    for i in range(len(train_data)):
                        data = train_data[i]
                        data_shape = list(data.shape[:-1])
                        if data_shape == inshapes[0] and data_feed['input'] < 0:
                            data_feed['input'] = i if data_feed['input'] < 0 else data_feed['input']
                            input = to_tensor(train_data[i])
                        elif data_shape == outshapes[0] and data_feed['target'] < 0:
                            data_feed['target'] = i if data_feed['target'] < 0 else data_feed['target']
                            target = to_tensor(train_data[i])
                        elif list(data.shape) == inshapes[0]:
                            data_feed['input'] = i if data_feed['input'] < 0 else data_feed['input']
                            input = to_tensor(train_data[i])
            self.training_context['signature'] = data_feed
            if test_data is None:
                test_data = train_data
            test_input = to_tensor(test_data[data_feed.get('input')]) if data_feed.get('input') >= 0 else None
            test_target = to_tensor(test_data[data_feed.get('target')]) if data_feed.get('target') >= 0 else None
        self.training_context['current_input'] = input
        self.training_context['current_target'] = target
        return input, target, test_input, test_target

    def do_preparation_for_loss(self):
        pass

    def do_post_loss_calculation(self):
        pass

    def do_gradient_update(self, log_gradients=False, keep_gradients_history=False):
        if log_gradients:
            self.gradients_history.append(to_numpy(self.training_context['grads']))

        for callback in self.training_context['callbacks']:
            callback.on_optimization_step_start(self.training_context)

        # self.optimizer.apply_gradients(zip(self.training_context['grads'],self._model.trainable_variables))  # loss,
        # metrics = self._model.train_on_batch(self.training_context['current_input'], self.training_context[
        # 'current_target'])  # if self.training_context['is_collect_data']:  #     if len(loss)==1:  #
        # self.training_context['losses']['total_losses'] = loss[0]  #         self.training_context['current_loss']=
        # loss[0]  #         k=list(self.losses.keys())[0]  #         if  k not in self.training_context['losses']:
        #             self.training_context['losses'][k] = []  #         self.training_context['losses'][k]= loss[0]
        #     else:  #         self.training_context['losses']['total_losses'] = loss[0]  #
        #     self.training_context['current_loss'] = loss[0]  #         n=1  #         for k,
        #     v in self._losses.items():  #             if k not in self.training_context['losses']:  #
        #     self.training_context['losses'][k] = []  #                 self.training_context['losses'][k] = loss[n]
        #                 n+=1  #     n=0  #     for k, v in self._metrics.items():  #         if k not in
        #                 self.training_context['metrics']:  #             self.training_context['metrics'][k] = []
        #             self.training_context['metrics'][k] = metrics[n]  #             n += 1
        if self.training_context['stop_update'] == 0:
            self.optimizer.apply_gradients(zip(self.training_context['grads'], self._model.trainable_variables))
        elif 0 < self.training_context['stop_update'] < 1:
            if random.random() <= self.training_context['stop_update']:
                self.optimizer.apply_gradients(zip(self.training_context['grads'], self._model.trainable_variables))
        else:
            self.training_context['stop_update'] = self.training_context['stop_update'] - 1

        for callback in self.training_context['callbacks']:
            callback.on_optimization_step_end(self.training_context)

    def do_post_gradient_update(self):
        self.training_context['tmp_losses'].append(to_numpy(self.training_context['current_loss']).mean())
        if self.training_context['is_collect_data'] == True:
            self.training_context['losses']['total_losses'].append(
                float(to_numpy(self.training_context['tmp_losses']).mean()))
            self.training_context['tmp_losses'] = []


    def do_on_progress_end(self):
        pass

    def log_gradient(self, grads=None, keep_gradients_history=False):
        grad_dict = {}
        for k, v in grads:
            grad_dict[k] = to_numpy(v.grad.clone())
        if keep_gradients_history:
            self.gradients_history.append(grad_dict)

    def log_weight(self, weghts=None, keep_weghts_history=False):
        if keep_weghts_history:
            self.weights_history.append(self._model.get_weights()[0])

    def save_model(self, save_path=None):
        for callback in self.training_context['callbacks']:
            callback.on_model_saving_start(self.training_context)
        save_path = self.training_context.get('save_path', save_path)
        if save_path is not None:
            self._model.save(save_path)
        else:
            if 'Models' is not None and len('Models') > 1 and not os.path.exists('Models'):
                try:
                    os.makedirs('Models')
                except Exception as e:
                    pass
            save_full_path = 'Models/model_{0}_epoch{1}.h5'.format(self._model.__name__,
                                                                   self.training_context['current_epoch'])
            self._model.save(save_full_path)

    def save_onnx(self, file_path):
        pass

    def save_weights(self, file_path):
        for callback in self.training_context['callbacks']:
            callback.on_model_saving_start(self.training_context)

        if file_path is not None:
            self._model.save_weights(file_path)
        elif 'save_path' in self.training_context and self.training_context['save_path'] is not None:
            self._model.save_weights(self.training_context['save_path'])

        else:
            if 'Models' is not None and len('Models') > 1 and not os.path.exists('Models'):
                try:
                    os.makedirs('Models')
                except Exception as e:
                    pass
            save_full_path = os.path.join('Models/', 'model_{0}_epoch{1}.h5'.format(self._model.__name__,
                                                                                    self.training_context[
                                                                                        'current_epoch']))
            self._model.save_weights(self.training_context['save_full_path'])

        self._model.train()

    def merge_grads(self, old_grads, new_grades):
        if isinstance(old_grads, list) and isinstance(new_grades, list) and len(old_grads) == len(new_grades):
            result = []
            for i in range(len(old_grads)):
                old_grad = old_grads[i]
                new_grade = new_grades[i]
                result.append(old_grad + new_grade)
            return result
        else:
            raise ValueError('In tensorflow ,grads should be list in eager mode')

    def train_model(self, train_data, test_data, current_epoch, current_batch, total_epoch, total_batch,
                    is_collect_data=True, is_print_batch_progress=True, is_print_epoch_progress=True,
                    log_gradients=False, log_weights=False, accumulate_grads=False):
        try:
            self.training_context['current_epoch'] = current_epoch
            self.training_context['current_batch'] = current_batch
            self.training_context['total_epoch'] = total_epoch
            self.training_context['total_batch'] = total_batch
            self.training_context['is_collect_data'] = is_collect_data
            self.training_context['log_gradients'] = log_gradients
            self.training_context['log_weights'] = log_weights
            self.training_context['current_model'] = self._model
            self.training_context['current_lr'] = self.optimizer.lr

            self.sample_collect_history.append(1 if is_collect_data else 0)

            if self.training_context['current_batch'] == 0:
                if self.training_context['current_epoch'] == 0:
                    self.do_on_training_start()
                    # epoch is not the logical inteval for us to control the flow
                    self.training_context['tmp_losses'] = []
                    self.training_context['tmp_metrics'] = OrderedDict()
                    self.training_context['losses'] = OrderedDict()
                    self.training_context['losses']['total_losses'] = []
                    self.training_context['metrics'] = OrderedDict()
                    self.training_context['grads_state'] = OrderedDict()
                    self.training_context['grads_state']['first_layer'] = []
                    self.training_context['grads_state']['last_layer'] = []

                self.training_context['print_batch_progress_frequency'] = 1
                self.training_context['print_epoch_progress_frequency'] = 1

                self.do_on_epoch_start()
                for callback in self.callbacks:
                    callback.on_epoch_start(self.training_context)

            self.do_on_batch_start()
            input, target, test_input, test_target = self.do_on_data_received(train_data, test_data)

            self.training_context['current_input'] = input
            self.training_context['current_target'] = target
            self.training_context['current_model'] = self._model
            for callback in self.callbacks:
                callback.on_data_received(self.training_context)
            input = self.training_context['current_input']
            target = self.training_context['current_target']

            if accumulate_grads == False:
                self.training_context['current_loss'] = 0
                self.do_preparation_for_loss()
                self.training_context['current_model'] = self._model
                self.training_context['optimizer'] = self.optimizer

            with tf.GradientTape() as g:

                output = self._model(input)
                self.training_context['current_model'] = self._model
                self.training_context['current_output'] = output

                # losss
                for k, v in self._losses.items():
                    if k not in self.training_context['losses']:
                        self.training_context['losses'][k] = []
                    loss_weight = 1
                    if k in self.loss_weights:
                        loss_weight = self.loss_weights[k]
                    this_loss = v(target, output) if callable(v) else v.call(target, )  # v.call(target,output) if
                    # hasattr(v, 'call') else
                    self.training_context['current_loss'] += this_loss * loss_weight
                    if is_collect_data:
                        self.training_context['losses'][k].append(to_numpy(this_loss) * loss_weight)

                if accumulate_grads == False:
                    for k, v in self._output_regs.items():
                        kl = k
                        if '_Loss' not in k:
                            kl = k + '_Loss'
                        if k not in self.training_context['losses']:
                            self.training_context['losses'][kl] = []
                        this_loss = v(output)
                        self.training_context['current_loss'] += this_loss  # self
                        # .training_context['current_loss'] + this_loss
                        if is_collect_data:
                            self.training_context['losses'][kl].append(float(to_numpy(this_loss)))

                    for k, v in self._model_regs.items():
                        kl = k
                        if '_Loss' not in k:
                            kl = k + '_Loss'
                        if kl not in self.training_context['losses']:
                            self.training_context['losses'][kl] = []
                        this_loss = v(self._model)
                        self.training_context['current_loss'] += this_loss
                        if is_collect_data:
                            self.training_context['losses'][kl].append(float(to_numpy(this_loss)))

                    self.training_context['optimizer'] = self.optimizer
                    self.do_post_loss_calculation()
                    for callback in self.callbacks:
                        callback.on_loss_calculation_end(self.training_context)

                    grads = g.gradient(self.training_context['current_loss'], self._model.trainable_variables)

                    if self.training_context['grads'] is None or isinstance(self.training_context['grads'],
                                                                            (int, float)):
                        self.training_context['grads'] = grads
                    else:
                        self.training_context['grads'] = self.merge_grads(self.training_context['grads'], grads)

                    self.training_context['optimizer'] = self.optimizer
                    self.do_pre_optimization_step()

                    if self.training_context['stop_update'] == 0:
                        self.do_gradient_update(log_gradients and is_collect_data)
                    else:
                        print(self._model.name, 'stop_update {0} times'.format(self.training_context['stop_update']))
                        self.training_context['stop_update'] = self.training_context['stop_update'] - 1

                    self.training_context['optimizer'] = self.optimizer
                    self.training_context['current_lr'] = self.optimizer.lr

                    # ON_POSTBACKWARD_CALCULATION
                    self.do_post_gradient_update()


                    self.training_context['grads'] = 0
                    # model comfirm
                    for k, v in self._constraints.items():
                        v(self._model)

                    if log_weights and is_collect_data:
                        self.log_weight()

                    output = self._model(test_input, training=False)
                    self.training_context['current_model'] = self._model
                    self.training_context['current_output'] = output

                    # ON_EVALUATION_START
                    self.do_on_metrics_evaluation_start()
                    for callback in self.training_context['callbacks']:
                        callback.on_metrics_evaluation_start(self.training_context)

                    for k, v in self._metrics.items():
                        if k not in self.training_context['metrics']:
                            self.training_context['metrics'][k] = []
                        if is_collect_data:
                            self.training_context['metrics'][k].append(
                                v.call(test_target, ).numpy() if hasattr(v, 'forward') else v(test_target,
                                                                                              output).numpy())

                    # ON_EVALUATION_END
                    self.do_on_metrics_evaluation_end()
                    for callback in self.training_context['callbacks']:
                        callback.on_metrics_evaluation_end(self.training_context)

                    if is_print_batch_progress:
                        self.do_on_progress_start()
                        for callback in self.training_context['callbacks']:
                            callback.on_progress_start(self.training_context)

                        self.print_batch_progress(self.training_context['print_batch_progress_frequency'])
                        self.training_context['print_batch_progress_frequency'] = 1
                        self.do_on_progress_end()
                        for callback in self.training_context['callbacks']:
                            callback.on_progress_end(self.training_context)
                    else:
                        self.training_context['print_batch_progress_frequency'] += 1

                    # ON_BATCH_END
                    self.do_on_batch_end()
                    for callback in self.training_context['callbacks']:
                        callback.on_batch_end(self.training_context)

            if self.training_context['current_batch'] == self.training_context['total_batch'] - 1:
                self.do_on_epoch_end()
                slice_cnt = sum(self.sample_collect_history[-1 * total_batch:])
                self.epoch_loss_history['total_losses'].append(
                    np.array(self.training_context['losses']['total_losses'][-1 * slice_cnt:]).mean())
                for k, v in self.training_context['metrics'].items():
                    self.epoch_metric_history[k].append(np.array(v[-1 * slice_cnt:]).mean())

                if is_print_epoch_progress:
                    self.do_on_progress_start()
                    for callback in self.training_context['callbacks']:
                        callback.on_progress_start(self.training_context)
                    self.print_epoch_progress(self.training_context['print_epoch_progress_frequency'])
                    self.training_context['print_epoch_progress_frequency'] = 1
                    self.do_on_progress_end()
                    for callback in self.training_context['callbacks']:
                        callback.on_progress_end(self.training_context)
                else:
                    self.training_context['print_epoch_progress_frequency'] += 1

                for callback in self.training_context['callbacks']:
                    callback.on_epoch_end(self.training_context)

                if self.training_context['current_epoch'] == self.training_context['total_epoch'] - 1:
                    self.do_on_training_end()
                    for callback in self.training_context['callbacks']:
                        callback.on_training_end(self.training_context)
        except Exception:
            PrintException()

    def summary(self):
        if self._model.built:
            return print_summary(self._model, get_terminal_size()[0])
        else:
            raise ValueError('This model has not yet been built. ')

    def extra_repr(self):
        return ''

    def __str__(self):
        self.__repr__()

    def _get_name(self):
        return self.__class__.__name__

    def __repr__(self):
        # We treat the extra repr like the sub-module, one item per line
        extra_lines = []
        extra_repr = self.extra_repr()
        # empty string will be split into list ['']
        if extra_repr:
            extra_lines = extra_repr.split('\n')
        child_lines = []
        for key, value in self.__dict__.items():
            if isinstance(value, OrderedDict):
                for subkey, subvalue in value.items():
                    mod_str = repr(subvalue)
                    mod_str = addindent(mod_str, 2)
                    child_lines.append('(' + key + '): ' + mod_str)
            else:
                mod_str = repr(value)
                mod_str = addindent(mod_str, 2)
                child_lines.append('(' + key + '): ' + mod_str)
        lines = extra_lines + child_lines

        main_str = self._get_name() + '('
        if lines:
            # simple one-liner info, which most builtin Modules will use
            if len(extra_lines) == 1 and not child_lines:
                main_str += extra_lines[0]
            else:
                main_str += '\n  ' + '\n  '.join(lines) + '\n'

        main_str += ')'
        return main_str

    def __dir__(self):
        module_attrs = dir(self._model.__class__)
        optimizer_attrs = dir(self.optimizer.__class__)
        attrs = list(self.__dict__.keys()) if self.__dict__ is not None else {}
        losses = list(self._losses.keys()) if self._losses is not None else {}
        metrics = list(self._metrics.keys()) if self._metrics is not None else {}
        output_regs = list(self._output_regs.keys()) if self._output_regs is not None else {}
        model_regs = list(self._model_regs.keys()) if self._model_regs is not None else {}
        constraints = list(self._constraints.keys()) if self._constraints is not None else {}
        keys = module_attrs + optimizer_attrs + attrs + losses + metrics + output_regs + model_regs + constraints
        # Eliminate attrs that are not legal Python variable names
        keys = [key for key in keys if not key[0].isdigit()]

        return sorted(keys)


class ImageClassificationModel(Model):
    def __init__(self, inputs=None, output=None, input_shape=None):
        super(ImageClassificationModel, self).__init__(inputs, output, input_shape)

        self._class_names = []
        self.preprocess_flow = []
        self._idx2lab = {}
        self._lab2idx = {}


    @property
    def class_names(self):
        return self._class_names

    @class_names.setter
    def class_names(self, value):
        if self._class_names != value:
            self._class_names = value
            self._lab2idx = {v: k for k, v in enumerate(self._class_names)}
            self._idx2lab = {k: v for k, v in enumerate(self._class_names)}

    def index2label(self, idx: int):
        if self._idx2lab is None or len(self._idx2lab.items()) == 0:
            raise ValueError('You dont have proper mapping class names')
        elif idx not in self._idx2lab:
            raise ValueError('Index :{0} is not exist in class names'.format(idx))
        else:
            return self._idx2lab[idx]

    def label2index(self, label):
        if self._lab2idx is None or len(self._lab2idx.items()) == 0:
            raise ValueError('You dont have proper mapping class names')
        elif label not in self._lab2idx:
            raise ValueError('label :{0} is not exist in class names'.format(label))
        else:
            return self._lab2idx[label]

    def infer_single_image(self, img, topk=1):
        if self._model.built:
            img = image2array(img)
            if img.shape[-1] == 4:
                img = img[:, :, :3]

            for func in self.preprocess_flow:
                if inspect.isfunction(func) and func is not image_backend_adaptive:
                    img = func(img)
            img = image_backend_adaptive(img)
            result = self._model.predict(to_tensor(np.expand_dims(img, 0)))

            result = to_numpy(result)[0]

            argresult = np.argsort(result)
            argresult = argresult[::-1]
            answer = OrderedDict()
            idxs = list(argresult[:topk])
            for idx in idxs:
                prob = result[idx]
                answer[self.index2label(idx)] = (idx, prob)
            # idx=int(np.argmax(result,-1)[0])

            return answer


class ImageDetectionModel(Model):
    def __init__(self, inputs=None, output=None, input_shape=None):
        super(ImageDetectionModel, self).__init__(inputs, output, input_shape)
        self.preprocess_flow = []
        self.detection_threshould = 0.5

    def infer_single_image(self, img, scale=1):
        if self._model.built:
            self._model.to(self.device)
            self._model.eval()
            img = image2array(img)
            if img.shape[-1] == 4:
                img = img[:, :, :3]

            for func in self.preprocess_flow:
                if inspect.isfunction(func):
                    img = func(img)

            result = self._model(to_tensor(np.expand_dims(img, 0)))
            self._model._set_inputs(to_tensor(np.expand_dims(img, 0)))
            bboxes = self.generate_bboxes(*result, threshould=self.detection_threshould, scale=scale)
            bboxes = self.nms(bboxes)
            # idx=int(np.argmax(result,-1)[0])
            return bboxes
        else:
            raise ValueError('the model is not built yet.')

    def generate_bboxes(self, *outputs, threshould=0.5, scale=1):
        raise NotImplementedError

    def nms(self, bboxes):
        raise NotImplementedError


class ImageSegmentationModel(Model):
    def __init__(self, inputs=None, output=None, input_shape=None):
        super(ImageSegmentationModel, self).__init__(inputs, output, input_shape)
        self.preprocess_flow = []


class LanguageModel(Model):
    def __init__(self, inputs=None, output=None, input_shape=None):
        super(LanguageModel, self).__init__(inputs, output, input_shape)
        self.preprocess_flow = []
