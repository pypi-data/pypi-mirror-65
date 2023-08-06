import pickle
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import ModelCheckpoint
from collections import defaultdict

class EpochCounter(keras.callbacks.Callback):
  def __init__(self, period, counter_path):
    self.period = period
    self.counter_path = counter_path
    self.clock = 0
    super(EpochCounter, self).__init__()
  def on_epoch_end(self, epoch, logs=None):
    # save epoch number to disk
    self.clock += 1
    if self.clock % self.period == 0:
      pickle.dump(epoch+1, open(self.counter_path, "wb"))

class HistoryLogger(keras.callbacks.Callback):
  def __init__(self, period, history_path):
    self.period = period
    self.history_path = history_path
    self.clock = 0
    super(HistoryLogger, self).__init__()
  def on_epoch_end(self, epoch, logs=None):
    self.clock += 1
    if self.clock % self.period == 0:
      pickle.dump(self.model.history.history, open(self.history_path, "wb"))

def _merge_dicts_with_only_lists_as_values(dicts):
  dd = defaultdict(list)
  for d in dicts:
    for key, value in d.items():
      # dict values are always lists for history dicts so extending is fine
      dd[key].extend(value)
  return dd

class ResumableModel(object):
  """Save and overwrite a model every 'save_every_epochs' epochs to 'to_path',
  preserving the number of epochs and the history dict over multiple interrupted
  executions.

  If to_path is mymodel.h5, then there will be mymodel_epoch_num.pkl and 
  mymodel_history.pkl in the same directory as mymodel.pkl, which backup the epoch
  counter and the history dict, respectively.

  Args:
    save_every_epochs (int): How often to save the model and the accompanying 
      parameters.
    to_path (str): A path to a model destination with the .h5 extension, which is 
      where model weights will be saved.

  Returns: A Keras History.history dictionary of the entire training process.
  """
  def __init__(self, model, save_every_epochs=10, to_path="model.h5"):
    
    assert to_path.endswith(".h5"):
    assert save_every_epochs > 0

    self.model = model
    self.save_every_epochs = save_every_epochs
    self.to_path = to_path
    self.prefix = os.path.splitext(to_path)[0]
    self.epoch_num_file = self.prefix + "_epoch_num.pkl"
    self.history_file = self.prefix + "_history.pkl"

    # recover latest epoch
    self.initial_epoch = self.get_epoch_num()
    # recover history
    self.history = self.get_history()
    # recover model from path
    if os.path.exists(to_path):
      self.model = load_model(to_path)
      print(f"Recovered model from {to_path} at epoch {self.initial_epoch}.")

  def _load_pickle(self, filePath, default_value):
    return pickle.load(open(filePath, 'rb')) if os.path.exists(filePath) else default_value
  
  def get_epoch_num(self):
    return self._load_pickle(self.epoch_num_file, 0)
  
  def get_history(self):
    return self._load_pickle(self.history_file, {})

  def _make_fit_args(self, *args, **kwargs):
    assert not 'initial_epoch' in kwargs
    # add callbacks for periodic checkpointing
    if 'callbacks' not in kwargs:
      kwargs['callbacks'] = []
    kwargs['callbacks'].append(HistoryLogger(period=self.save_every_epochs, history_path=self.history_file))
    kwargs['callbacks'].append(ModelCheckpoint(self.to_path, verbose=True, period=self.save_every_epochs))
    kwargs['callbacks'].append(EpochCounter(period=self.save_every_epochs, counter_path=self.epoch_num_file))
    # Warn user if the training is already complete.
    if 'epochs' in kwargs and self.initial_epoch >= kwargs['epochs']:
      epochs = kwargs['epochs']
      print(f'You want to train for {epochs} epochs but {self.initial_epoch} epochs already completed; nothing to do.')
    return args, kwargs
  
  def fit(self, *args, **kwargs):
    args, kwargs = self._make_fit_args(*args, **kwargs)
    remainingHistory = self.model.fit(initial_epoch=self.initial_epoch, *args, **kwargs)
    return _merge_dicts_with_only_lists_as_values([self.history, remainingHistory.history])

  
  def fit_generator(self, *args, **kwargs):
    args, kwargs = self._make_fit_args(*args, **kwargs)
    remainingHistory = self.model.fit_generator(initial_epoch=self.initial_epoch, *args, **kwargs)
    return _merge_dicts_with_only_lists_as_values([self.history, remainingHistory.history])