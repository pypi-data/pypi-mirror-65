#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
GLobal package configuration to improve consistency 
'''
#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import absolute_import, division, print_function, unicode_literals

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import six
import os
from collections import MutableMapping
from functools import wraps


_cfg_file = os.path.join(os.path.expanduser('~'),r".Pynomial\Configurations.json")


# validation functions
# ---------------------------------------------------------------------------------------------------------------------------------------------
def handle_none_value(validation_function):
	"""
	A method to handle None/null values
	"""
	@wraps(validation_function) # Using the wraps for invoking update_wrapper(). This keeps the name and doc string of the original function
	def wrapped_validation_function(*args, **kwargs):

		input_item = args[0]
		accept_none = kwargs.get('accept_none', True)
		if (input_item is None):
			if accept_none:
				return None
			else:
				raise ValueError('Could not pass None as a value for the configuration item')

		# call the plotting function
		returnargs = validation_function(*args, **kwargs)
		return returnargs
	
	return wrapped_validation_function


@handle_none_value
def _validate_string(input_item, accept_none = True):
	"""
	 A method to convert input_item to string or raise error if it is not convertable
	"""
	try:
		if isinstance(input_item,list):
			return [six.text_type(item) for item in input_item]
		elif isinstance(input_item,dict):
			return dict((six.text_type(key), six.text_type(value)) for key, value in input_item.items())
		else:
			return six.text_type(input_item)
	except ValueError:
		raise ValueError('Could not convert "{}" to string'.format(input_item))

@handle_none_value
def _validate_float(input_item, accept_none = True):
	"""
	 A method to convert input_item to float or raise error if it is not convertable
	"""
	try:
		return float(input_item)
	except ValueError:
		raise ValueError('Could not convert {} to float'.format(input_item))

@handle_none_value
def _validate_int(input_item, accept_none = True):
	"""
	 A method to convert input_item to integer or raise error if it is not convertable
	"""
	try:
		return int(input_item)
	except ValueError:
		raise ValueError('Could not convert {} to int'.format(input_item))

@handle_none_value
def _validate_color(input_item, accept_none = False):

	from matplotlib.colors import is_color_like
	'return a valid color arg'
	try:
		if input_item.lower() == 'none':
			return 'none'
	except AttributeError:
		pass

	if isinstance(input_item, six.string_types):
		if len(input_item) == 6 or len(input_item) == 8:
			stmp = '#' + input_item
			if is_color_like(stmp):
				return stmp

	if is_color_like(input_item):
		return input_item

@handle_none_value
def _validate_list(input_item, accept_none=True):
	"""
	A validation method to convert input_item to a list or raise error if it is not convertable
	"""
	if input_item is None and accept_none:
		return None
	try:
		return list(input_item)
	except ValueError:
		raise ValueError('Could not convert input to list')

@handle_none_value
def _validate_bool(input_item, accept_none=False):
	"""
	A validation method to convert input_item to boolean or raise error if it is not convertable
	"""
	try:
		return bool(input_item)
	except ValueError:
		raise ValueError('Could not convert input_item to boolean')

# writing and loading the configurations
#------------------------------------------------------------------------------------
def _write_config_dict(file_name, dictionary, section, description = None):

	import json

	if os.path.isfile(file_name):
		with open(file_name, 'r') as cfg_file:
			dict_main = dict(json.load(cfg_file))
	else:
		dict_main = {}
	if section in dict_main.keys():
		dict_main.pop(section, None)
	
	section_dict={}
	for key in list(sorted(dictionary.keys())):
		section_dict.update({key: {'Value': dictionary[key], 'Description':None if description is None else description[key]}})
	
	dict_main.update({section:section_dict})

	with open(file_name, 'w') as cfg_file:
		json.dump(dict_main, cfg_file)


def _parse_config_dict(file_name, section):
	import json
	if os.path.isfile(file_name):
		try:
			with open(file_name, 'r') as fp:
				dict_main = dict(json.load(fp))
		except:
			print('Unable to open the provided parameter file: {}'.format(file_name))
			return {}
	else:
		print('Unable to load the system defaults as it does no exist! Use gs.Programs.set_systems_defaults to create one.')
		return {}
	# Allowing no values
	if section not in dict_main.keys():
		return {}
		
	new_dict = {}
	input_dict = dict_main[section]
	for key in input_dict:
		new_dict.update({key: input_dict[key]['Value']})

	return new_dict



# Default configurations
#------------------------------------------------------------------------------------

default_configs = {
	
	'config.verbose': [True, _validate_bool]
	,'config.autoload': [True, _validate_bool]
	,'ETL.DefaultTimeZone': ['Canada/Mountain', _validate_string]
	,'Azure.SP.client_id': [None, _validate_string]
	,'Azure.SP.tenant_id': [None, _validate_string]
	,'Azure.SP.client_secret': [None, _validate_string]
	,'Azure.login.user_name': [None, _validate_string]
}

default_config_description ={
	'config.verbose': ('Option to have verbose description when the default configurations are loaded')
	,'config.autoload': ('Option to control if the configurations are auto loaded from the system defaults file')
	,'ETL.DefaultTimeZone': ('The default time zone that is used for Extract, Transform and Load operations')
	,'Azure.SP.client_id': ('Default Azure service principal client id')
	,'Azure.SP.tenant_id': ('Default Azure tenant id')
	,'Azure.SP.client_secret': ('Secret for the default service principal')
	,'Azure.login.user_name': ('Default user name for Azure credentials')
}

# Plotstyles
#----------------------------------------------------------------------------------------------------------
import matplotlib as mpl


# Classes
#-------------------------------------------------------------------------------------------
class Configurations(MutableMapping, dict):
	'''
	A dictionary object to define an maintain the default/user configurations. This helps to minimize repetition of parameters
	and facilitate implementing consistent workflows.


	Examples of modifying the configurations:

		>>> import pynomial as pn
		>>> pn.Configurations['ETL.DefaultTimeZone']


	.. codeauthor:: Mostafa Hadavand 2020-03-18

	'''


	def __init__(self, *args, **kwargs):

		self.__validation_dict = dict((key, converter) for key, (_, converter) in six.iteritems(default_configs))
		self.update(*args, **kwargs)
		self._section_name = 'Configurations'
		self.__default_configs = dict((key, config) for key, (_, config) in six.iteritems(default_configs))
		self.__default_descriptions = default_config_description


	def __setitem__(self, key, value):

		try:
			try:
				c_value = self.__validation_dict[key](value)
			except ValueError as ve:
				raise ValueError("Key %s: %s" % (key, str(ve)))
			dict.__setitem__(self, key, c_value)
		except KeyError:
			raise KeyError('%s is not a valid configurations. See Configurations.keys() for a '
						   'list of valid configurations.' % (key,))

	def __getitem__(self, key):
		value = dict.__getitem__(self, key)

		return value

	def __iter__(self):
		"""
		Yield sorted list of keys.
		"""
		for item in sorted(dict.__iter__(self)):
			yield item
	
	def __repr__(self):
		import pprint
		class_name = self.__class__.__name__
		indent = len(class_name) + 1
		repr_split = pprint.pformat(dict(self), indent=1,
									width=80 - indent).split('\n')
		repr_indented = ('\n' + ' ' * indent).join(repr_split)
		return '{0}({1})'.format(class_name, repr_indented)

	def __str__(self):
		return '\n'.join('{}: {}'.format(key, value) for key, value in sorted(self.items()))


	def __delitem__(self, key):
		raise KeyError('Not allowed to remove a paramater!')


	def restore_defaults(self):
		"""
		Restore to the original dictionary of defaults values for the current instance
		"""
		self.update([(key, value) for key, value in self.__default_configs.items()])


	def describe(self, key=None, verbose=True):
		"""
		Prints a description of an individual configuration in the
		pynomial configurations set, as specified by the provided key. If key
		is None, all configuration descriptions will be printed.

		Parameters:
			key(str) : the target configuration key to retrieve its description

		"""
		if key is None:
			# Print the entire dictionary description
			for iterkey in iter(self):
				print(iterkey + ':\n' + self._default_descriptions[iterkey] + '\n')
		else:
			if key not in iter(self):
				raise KeyError('%s is not a valid configuration. See pygeostat.Configurations.keys() for a '
							   'list of valid configurations.' % (key,))
			if verbose:
				print(key + ':\n' + self._default_descriptions[key])

	def save(self, file_name):
		"""
		Save the current configurations to the given file
		"""
		_write_config_dict(file_name, self, self._section_name, description=self.__default_descriptions)

	def load(self, file_name):
		"""
		Load the pygeostat configurations from a given file
		"""
		import os
		assert os.path.isfile(file_name), "ERROR: `{}` does not exist".format(file_name)
		newdict = _parse_config_dict(file_name, self._section_name)
		self.update(newdict)

	def reset_systemdefault(self):
		"""
		Overwrite the system default configurations stored in ``%USER%/.Pynomial`` with the default configurations of
		pygeostat
		"""
		_write_config_dict(_cfg_file, self.__default_configs, self._section_name, description=self.__default_descriptions)


	def set_systemdefault(self):
		"""
		Write the current configuration from the current instance i.e. ``self`` to the system default configurations in ``%USER%/.Pynomial``
		"""
		print("Writing current `{}` to system default at: {}".format(self._section_name, _cfg_file))
		main_dir = os.path.dirname(_cfg_file)
		if not os.path.exists(main_dir):
			os.makedirs(main_dir)
		self.save(_cfg_file)


	def get_systemdefault(self, confirm_autoload=False):
		"""
		Get the pynomial configurations stored in the system defaults in ``%USER%/.Pynomial``. ``confirm_autoload``
		is passed only on the very first call on module init.
		"""
		if os.path.isfile(_cfg_file):
			newdict = _parse_config_dict(_cfg_file, section=self._section_name)
			
			if newdict: # If dictionary is not empty
				if confirm_autoload:
					if newdict.get("config.autoload", False):
						self.update(newdict)
						if newdict.get("config.verbose", False):
							print("Loading default pynomial configurations from {}".format(_cfg_file))
				else:
					self.update(newdict)
					if newdict.get("config.verbose", False):
						print("Loading default pynomial configurations from {}".format(_cfg_file))


#--------------------Initializations-------------------
#-----------------------------------------------------
# Configurations initializations
def _configurations_initialize():
	ret = Configurations([(key, default) for key, (default, _) in
					six.iteritems(default_configs)])

	ret.get_systemdefault(confirm_autoload=True)
	return ret

Configurations = _configurations_initialize()