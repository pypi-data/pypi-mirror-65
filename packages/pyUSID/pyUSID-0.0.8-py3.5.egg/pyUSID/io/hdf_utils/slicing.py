from __future__ import division, print_function, absolute_import, unicode_literals

import os
import sys
from warnings import warn
import h5py
import numpy as np
import dask.array as da

from .base import get_attr
from .simple import check_if_main, create_results_group, \
                    write_reduced_anc_dsets, link_as_main, copy_attributes
from .model import  get_dimensionality, get_sort_order, get_unit_values, \
                    reshape_to_n_dims, write_main_dataset, reshape_from_n_dims

from ..dtype_utils import flatten_to_real, contains_integers, \
                          validate_single_string_arg, validate_list_of_strings
from ..write_utils import Dimension


def __validate_slice_dict(slice_dict, dim_labels):
    """
    Validates the slice dictionary

    Parameters
    ----------
    slice_dict : dict
        Dictionary of array-likes.

    Returns
    -------
    None
    """
    if not isinstance(slice_dict, dict):
        raise TypeError('slice_dict should be a dictionary of slice objects')

    dim_labels = validate_list_of_strings(dim_labels)

    for key, val in slice_dict.items():
        # Make sure the dimension is valid
        if key not in dim_labels:
            raise KeyError('Cannot slice on dimension {}.  '
                           'Valid dimensions are {}.'.format(key, dim_labels))
        if not isinstance(val, (slice, list, np.ndarray, tuple, int)):
            raise TypeError('The slices must be array-likes or slice objects.')
    return True


def _get_pos_spec_slices(slice_dict, h5_spec_inds, h5_pos_inds):
    """
    Convert the slice dictionary into two lists of indices, one each for the
    position and spectroscopic
    dimensions.

    Parameters
    ----------
    slice_dict : dict
        Dictionary of array-likes.

    Returns
    -------
    pos_slice : list of unsigned int
        Position indices included in the slice
    spec_slice : list of unsigned int
        Spectroscopic indices included in the slice
    """
    __validate_slice_dict(slice_dict, dim_labels)

    if len(slice_dict) == 0:
        pos_slice = np.expand_dims(np.arange(self.shape[0]), axis=1)
        spec_slice = np.expand_dims(np.arange(self.shape[1]), axis=1)
        return pos_slice, spec_slice

    # Create default slices that include the entire dimension
    n_dim_slices = dict()
    n_dim_slices_sizes = dict()
    for dim_lab, dim_size in zip(self.n_dim_labels, self.n_dim_sizes):
        n_dim_slices[dim_lab] = list(range(dim_size))
        n_dim_slices_sizes[dim_lab] = len(n_dim_slices[dim_lab])
    # Loop over all the keyword arguments and create slices for each.
    for key, val in slice_dict.items():
        # Check the value and convert to a slice object if possible.
        # Use a list if not.
        if isinstance(val, slice):
            val = n_dim_slices[key][val]
        elif isinstance(val, list):
            pass
        elif isinstance(val, np.ndarray):
            val = val.flatten().tolist()
        elif isinstance(val, tuple):
            val = list(val)
        elif isinstance(val, int):
            val = [val]
        else:
            raise TypeError('The slices must be array-likes or slice objects.')

        if not contains_integers(val, min_val=0):
            raise ValueError('Slicing indices should be >= 0')

        # check to make sure that the values are not out of bounds:
        dim_ind = np.squeeze(np.argwhere(self.__n_dim_labs == key))
        cur_dim_size = self.__n_dim_sizes[dim_ind]
        if np.max(val) >= cur_dim_size:
            raise ValueError('slicing argument for dimension: {} was beyond {}'.format(key, cur_dim_size))

        n_dim_slices[key] = val

        n_dim_slices_sizes[key] = len(val)

    # Build the list of position slice indices
    for pos_ind, pos_lab in enumerate(self.__pos_dim_labels):
        # n_dim_slices[pos_lab] = np.isin(self.h5_pos_inds[:, pos_ind], n_dim_slices[pos_lab])
        temp = [h5_pos_inds[:, pos_ind] == item for item in n_dim_slices[pos_lab]]
        n_dim_slices[pos_lab] = np.any(np.vstack(temp), axis=0)
        if pos_ind == 0:
            pos_slice = n_dim_slices[pos_lab]
        else:
            pos_slice = np.logical_and(pos_slice, n_dim_slices[pos_lab])
    pos_slice = np.argwhere(pos_slice)

    # Do the same for the spectroscopic slice
    for spec_ind, spec_lab in enumerate(self.__spec_dim_labels):
        # n_dim_slices[spec_lab] = np.isin(self.h5_spec_inds[spec_ind], n_dim_slices[spec_lab])
        temp = [h5_spec_inds[spec_ind] == item for item in n_dim_slices[spec_lab]]
        n_dim_slices[spec_lab] = np.any(np.vstack(temp), axis=0)
        if spec_ind == 0:
            spec_slice = n_dim_slices[spec_lab]
        else:
            spec_slice = np.logical_and(spec_slice, n_dim_slices[spec_lab])
    spec_slice = np.argwhere(spec_slice)

    # TODO: Shouldn't we simply squeeze before returning?
    return pos_slice, spec_slice

def _get_dims_for_slice(self, slice_dict=None, verbose=False):
    """
    Provides Dimension objects that express the reference position and spectroscopic dimensions for this dataset
    once it is sliced via the provided slicing dictionary.

    Parameters
    ----------
    slice_dict : dict (optional)
        Dictionary to slice one or more dimensions of the dataset by indices
    verbose : bool (optional)
        Whether or not to print debugging statements to stdout. Default = False

    Returns
    -------
    pos_dims : list
        List of :class:`~pyUSID.io.write_utils.Dimension` objects for each of the remaining position dimensions
    spec_dims : list
        List of :class:`~pyUSID.io.write_utils.Dimension` objects for each of the remaining spectroscopic dimensions
    """

    pos_labels = self.pos_dim_labels
    pos_units = get_attr(self.h5_pos_inds, 'units')
    spec_labels = self.spec_dim_labels
    spec_units = get_attr(self.h5_spec_inds, 'units')

    self.__validate_slice_dict(slice_dict)

    # First work on slicing the ancillary matrices. Determine dimensionality before slicing n dims:
    pos_slices, spec_slices = self._get_pos_spec_slices(slice_dict)
    # Things are too big to print here.

    pos_inds = self.h5_pos_inds[np.squeeze(pos_slices), :]
    pos_vals = self.h5_pos_vals[np.squeeze(pos_slices), :]

    if verbose:
        print('Checking for and correcting the dimensionality of the indices and values datasets:')
        print('Pos Inds: {}, Pos Vals: {}'.format(pos_inds.shape, pos_vals.shape))
    if pos_inds.ndim == 1:
        pos_inds = np.expand_dims(pos_inds, axis=0)
        pos_vals = np.expand_dims(pos_vals, axis=0)

    spec_inds = self.h5_spec_inds[:, np.squeeze(spec_slices)]
    spec_vals = self.h5_spec_vals[:, np.squeeze(spec_slices)]

    if verbose:
        print('Checking for and correcting the dimensionality of the indices and values datasets:')
        print('Spec Inds: {}, Spec Vals: {}'.format(spec_inds.shape, spec_vals.shape))

    if spec_inds.ndim == 1:
        spec_inds = np.expand_dims(spec_inds, axis=0)
        spec_vals = np.expand_dims(spec_vals, axis=0)

    if verbose:
        print('After correction of shape:')
        print('Pos Inds: {}, Pos Vals: {}, Spec Inds: {}, Spec Vals: {}'.format(pos_inds.shape, pos_vals.shape,
                                                                                spec_inds.shape,
                                                                                spec_vals.shape))

    pos_unit_values = get_unit_values(pos_inds, pos_vals, all_dim_names=self.pos_dim_labels, is_spec=False,
                                      verbose=False)
    spec_unit_values = get_unit_values(spec_inds, spec_vals, all_dim_names=self.spec_dim_labels, is_spec=True,
                                       verbose=False)

    if verbose:
        print('Position unit values:')
        print(pos_unit_values)
        print('Spectroscopic unit values:')
        print(spec_unit_values)

    # Now unit values will be correct for this slicing

    # additional benefit - remove those dimensions which have at most 1 value:
    def assemble_dimensions(full_labels, full_units, full_values):
        new_labels = []
        new_units = []
        for dim_ind, dim_name in enumerate(full_labels):
            if len(full_values[dim_name]) < 2:
                del (full_values[dim_name])
            else:
                new_labels.append(dim_name)
                new_units.append(full_units[dim_ind])
        return np.array(new_labels), np.array(new_units), full_values

    pos_labels, pos_units, pos_unit_values = assemble_dimensions(pos_labels, pos_units, pos_unit_values)
    spec_labels, spec_units, spec_unit_values = assemble_dimensions(spec_labels, spec_units, spec_unit_values)

    # Ensuring that there are always at least 1 position and spectroscopic dimensions:
    if len(pos_labels) == 0:
        pos_labels = ['arb.']
        pos_units = ['a. u.']
        pos_unit_values = {pos_labels[-1]: np.array([1])}

    if len(spec_labels) == 0:
        spec_labels = ['arb.']
        spec_units = ['a. u.']
        spec_unit_values = {spec_labels[-1]: np.array([1])}

    if verbose:
        print('\n\nAfter removing singular dimensions:')
        print('Position: Labels: {}, Units: {}, Values:'.format(pos_labels, pos_units))
        print(pos_unit_values)
        print('Spectroscopic: Labels: {}, Units: {}, Values:'.format(spec_labels, spec_units))
        print(spec_unit_values)

    pos_dims = []
    for name, units in zip(pos_labels, pos_units):
        pos_dims.append(Dimension(name, units, pos_unit_values[name]))
    spec_dims = []
    for name, units in zip(spec_labels, spec_units):
        spec_dims.append(Dimension(name, units, spec_unit_values[name]))

    return pos_dims, spec_dims