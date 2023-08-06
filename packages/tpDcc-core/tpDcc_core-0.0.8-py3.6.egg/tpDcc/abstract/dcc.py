#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains abstract definition of basic DCC functions
"""

from __future__ import print_function, division, absolute_import

from collections import OrderedDict

from tpDcc.libs.python import decorators


class AbstractDCC(object):

    class DialogResult(object):
        Yes = 'Yes'
        No = 'No'
        Cancel = 'No'
        Close = 'No'

    TYPE_FILTERS = OrderedDict()

    @staticmethod
    @decorators.abstractmethod
    def get_name():
        """
        Returns the name of the DCC
        :return: str
        """

        raise NotImplementedError('abstract DCC function get_name() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_extensions():
        """
        Returns supported extensions of the DCC
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC function get_extensions() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_dpi(value=1):
        """
        Returns current DPI used by DCC
        :param value: float
        :return: float
        """

        raise NotImplementedError('abstract DCC function get_dpi() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_dpi_scale(value):
        """
        Returns current DPI scale used by DCC
        :param value: float
        :return: float
        """

        raise NotImplementedError('abstract DCC function get_dpi_scale() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_version():
        """
        Returns version of the DCC
        :return: int
        """

        raise NotImplementedError('abstract DCC function get_version() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_version_name():
        """
        Returns version of the DCC
        :return: str
        """

        raise NotImplementedError('abstract DCC function get_version_name() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def is_batch():
        """
        Returns whether DCC is being executed in batch mode or not
        :return: bool
        """

        raise NotImplementedError('abstract DCC function is_batch() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def enable_component_selection():
        """
        Enables DCC component selection mode
        """

        raise NotImplementedError('abstract DCC function enable_component_selection() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_main_window():
        """
        Returns Qt object that references to the main DCC window
        :return:
        """

        raise NotImplementedError('abstract DCC function get_main_window() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_main_menubar():
        """
        Returns Qt object that references to the main DCC menubar
        :return:
        """

        raise NotImplementedError('abstract DCC function get_main_menubar() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def is_window_floating(window_name):
        """
        Returns whether or not DCC window is floating
        :param window_name: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function is_window_floating() not implemented!')

    @staticmethod
    def focus_ui_panel(panel_name):
        """
        Focus UI panel with given name
        :param panel_name: str
        """

        raise NotImplementedError('abstract DCC function focus_ui_panel() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def enable_wait_cursor():
        """
        Enables wait cursor in current DCC
        """

        raise NotImplementedError('abstract DCC function enable_wait_cursor() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def disable_wait_cursor():
        """
        Enables wait cursor in current DCC
        """

        raise NotImplementedError('abstract DCC function disable_wait_cursor() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def execute_deferred(fn):
        """
        Executes given function in deferred mode
        """

        raise NotImplementedError('abstract DCC function execute_deferred() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def new_scene(force=True, do_save=True):
        """
        Creates a new DCC scene
        :param force: bool, True if we want to save the scene without any prompt dialog
        :param do_save: bool, True if you want to save the current scene before creating new scene
        :return:
        """

        raise NotImplementedError('abstract DCC function new_scene() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def object_exists(node):
        """
        Returns whether given object exists or not
        :return: bool
        """

        raise NotImplementedError('abstract DCC function object_exists() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def object_type(node):
        """
        Returns type of given object
        :param node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function object_type() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def check_object_type(node, node_type, check_sub_types=False):
        """
        Returns whether give node is of the given type or not
        :param node: str
        :param node_type: str
        :param check_sub_types: bool
        :return: bool
        """

        raise NotImplementedError('abstract DCC function check_object_type() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_empty_group(name, parent=None):
        """
        Creates a new empty group node
        :param name: str
        :param parent: str or None
        """

        raise NotImplementedError('abstract DCC function create_empty_group() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_buffer_group(node, **kwargs):
        """
        Creates a buffer group on top of the given node
        :param node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function create_buffer_group() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_buffer_group(node, **kwargs):
        """
        Returns buffer group above given node
        :param node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function get_buffer_group() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def group_node(node, name, parent=None):
        """
        Creates a new group and parent give node to it
        :param node: str
        :param name: str
        :param parent: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function group_node() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_node(node_type, node_name=None):
        """
        Creates a new node of the given type and with the given name
        :param node_type: str
        :param node_name: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function create_node() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_name(node):
        """
        Returns the name of the given node
        :param node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_name() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_name_without_namespace(node):
        """
        Returns the name of the given node without namespace
        :param node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_name_without_namespace() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_handle(node):
        """
        Returns unique identifier of the given node
        :param node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_handle() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_type(node):
        """
        Returns node type of given object
        :param node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_type() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_is_empty(node, *args, **kwargs):
        """
        Returns whether given node is an empty one
        The concept of empty node can vary depending on the DCC
        :param node: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function node_is_empty() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_is_transform(node):
        """
        Returns whether or not given node is a transform node
        :param node: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function node_is_transform() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_is_joint(node):
        """
        Returns whether or not given node is a joint node
        :param node: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function node_is_joint() not implemented!')

    @staticmethod
    def node_is_locator(node):
        """
        Returns whether or not given node is a locator node
        :param node: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function node_is_locator() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_world_space_translation(node):
        """
        Returns world translation of given node
        :param node: str
        :return: list
        """

        raise NotImplementedError('abstract DCC function node_world_space_translation() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_world_bounding_box(node):
        """
        Returns node_world_bounding_box box of given node
        :param node: str
        :return:
        """

        raise NotImplementedError('abstract DCC function node_bounding_box() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def move_node(node, x, y, z, **kwargs):
        """
        Moves given node
        :param node: str
        :param x: float
        :param y: float
        :param z: float
        :param kwargs:
        """

        raise NotImplementedError('abstract DCC function move_node() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def translate_node_in_world_space(node, translation_list, **kwargs):
        """
        Translates given node with the given translation vector
        :param node: str
        :param translation_list:  list(float, float, float)
        """

        raise NotImplementedError('abstract DCC translate_node_in_world_space() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def translate_node_in_object_space(node, translation_list, **kwargs):
        """
        Translates given node with the given translation vector
        :param node: str
        :param translation_list:  list(float, float, float)
        """

        raise NotImplementedError('abstract DCC translate_node_in_object_space() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_world_space_rotation(node):
        """
        Returns world rotation of given node
        :param node: str
        :return: list
        """

        raise NotImplementedError('abstract DCC function node_world_space_rotation() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def rotate_node(node, x, y, z, **kwargs):
        """
        Rotates given node
        :param node: str
        :param x: float
        :param y: float
        :param z: float
        :param kwargs:
        """

        raise NotImplementedError('abstract DCC function rotate_node() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def rotate_node_in_world_space(node, rotation_list, **kwargs):
        """
        Translates given node with the given translation vector
        :param node: str
        :param rotation_list:  list(float, float, float)
        """

        raise NotImplementedError('abstract DCC rotate_node_in_world_space() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def rotate_node_in_object_space(node, rotation_list, **kwargs):
        """
        Translates given node with the given translation vector
        :param node: str
        :param rotation_list:  list(float, float, float)
        """

        raise NotImplementedError('abstract DCC rotate_node_in_object_space() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_world_space_scale(node):
        """
        Returns world scale of given node
        :param node: str
        :return: list
        """

        raise NotImplementedError('abstract DCC function node_world_space_scale() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def scale_node(node, x, y, z, **kwargs):
        """
        Scales node
        :param node: str
        :param x: float
        :param y: float
        :param z: float
        :param kwargs:
        """

        raise NotImplementedError('abstract DCC function scale() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def scale_node_in_world_space(node, scale_list, **kwargs):
        """
        Scales given node with the given vector list
        :param node: str
        :param scale_list: list(float, float, float)
        """

        raise NotImplementedError('abstract DCC scale_node_in_world_space() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def scale_node_in_object_space(node, scale_list, **kwargs):
        """
        Scales given node with the given vector list
        :param node: str
        :param scale_list: list(float, float, float)
        """

        raise NotImplementedError('abstract DCC scale_node_in_object_space() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_world_space_pivot(node):
        """
        Returns node pivot in world space
        :param node: str
        :return:
        """

        raise NotImplementedError('abstract DCC node_world_space_pivot() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def all_scene_objects(full_path=True):
        """
        Returns a list with all scene nodes
        :param full_path: bool
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function all_scene_objects() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def rename_node(node, new_name, **kwargs):
        """
        Renames given node with new given name
        :param node: str
        :param new_name: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function rename_node() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def rename_transform_shape_nodes(node):
        """
        Renames all shape nodes of the given transform node
        :param node: str
        """

        raise NotImplementedError('abstract DCC function rename_transform_shape_nodes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def show_object(node):
        """
        Shows given object
        :param node: str
        """

        raise NotImplementedError('abstract DCC function show_object() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def hide_object(node):
        """
        Hides given object
        :param node: str
        """

        raise NotImplementedError('abstract DCC function hide_object() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def select_object(node, replace_selection=False, **kwargs):
        """
        Selects given object in the current scene
        :param replace_selection: bool
        :param node: str
        """

        raise NotImplementedError('abstract DCC function select_object() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def select_hierarchy(root=None, add=False):
        """
        Selects the hierarchy of the given node
        If no object is given current selection will be used
        :param root: str
        :param add: bool, Whether new selected objects need to be added to current selection or not
        """

        raise NotImplementedError('abstract DCC function select_hierarchy() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def deselect_object(node):
        """
        Deselects given node from current selection
        :param node: str
        """

        raise NotImplementedError('abstract DCC function deselect_object() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def clear_selection():
        """
        Clears current scene selection
        """

        raise NotImplementedError('abstract DCC function clear_selection() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def duplicate_object(node, name='', only_parent=False):
        """
        Duplicates given object in current scene
        :param node: str
        :param name: str
        :param only_parent: bool, If True, only given node will be duplicated (ignoring its children)
        :return: str
        """

        raise NotImplementedError('abstract DCC function duplicate_object() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def delete_object(node):
        """
        Removes given node from current scene
        :param node: str
        """

        raise NotImplementedError('abstract DCC function delete_object() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def selected_nodes(full_path=True, **kwargs):
        """
        Returns a list of selected nodes
        :param full_path: bool
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function selected_nodes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def selected_nodes_of_type(node_type, full_path=True):
        """
        Returns a list of selected nodes of given type
        :param node_type: str
        :param full_path: bool
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC function select_nodes_of_type() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def selected_hilited_nodes(full_path=True):
        """
        Returns a list of selected nodes that are hilited for component selection
        :param full_path: bool
        :param kwargs:
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC function selected_hilited_nodes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def filter_nodes_by_selected_components(filter_type, nodes=None, full_path=False, **kwargs):
        """
        Function that filter nodes taking into account specific component filters
        :param filter_type: int
        :param nodes: list(str)
        :param full_path: bool
        :param kwargs:
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC function filter_nodes_by_selected_components() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def all_shapes_nodes(full_path=True):
        """
        Returns all shapes nodes in current scene
        :param full_path: bool
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function all_shapes_nodes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def default_scene_nodes(full_path=True):
        """
        Returns a list of nodes that are created by default by the DCC when a new scene is created
        :param full_path: bool
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function default_scene_nodes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_short_name(node, **kwargs):
        """
        Returns short name of the given node
        :param node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_short_name() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_long_name(node):
        """
        Returns long name of the given node
        :param node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_long_name() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_object_color(node):
        """
        Returns the color of the given node
        :param node: str
        :return: list(int, int, int, int)
        """

        raise NotImplementedError('abstract DCC function node_object_color() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_override_enabled(node):
        """
        Returns whether the given node has its display override attribute enabled or not
        :param node: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function node_object_color() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_namespaces():
        """
        Returns a list of all available namespaces
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC function list_namespaces() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def namespace_separator():
        """
        Returns character used to separate namespace from the node name
        :return: str
        """

        raise NotImplementedError('abstract DCC function namespace_separator() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def namespace_exists(name):
        """
        Returns whether or not given namespace exists in current scene
        :param name: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function namespace_exists() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def unique_namespace(name):
        """
        Returns a unique namespace from the given one
        :param name: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function unique_namespace() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_namespace(node, check_node=True, clean=False):
        """
        Returns namespace of the given node
        :param node: str
        :param check_node: bool
        :param clean: bool
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_namespace() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def all_nodes_in_namespace(namespace_name):
        """
        Returns all nodes in given namespace
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC function node_namespace() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def rename_namespace(current_namespace, new_namespace):
        """
        Renames namespace of the given node
        :param current_namespace: str
        :param new_namespace: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function rename_namespace() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_parent_namespace(node):
        """
        Returns namespace of the given node parent
        :param node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_parent_namespace() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_is_visible(node):
        """
        Returns whether given node is visible or not
        :param node: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function node_is_visible() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_color(node):
        """
        Returns color of the given node
        :param node: str
        :return:
        """

        raise NotImplementedError('abstract DCC function node_color() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_node_color(node, color):
        """
        Sets the color of the given node
        :param node: str
        :param color:
        """

        raise NotImplementedError('abstract DCC function set_node_color() not implemented!')

    @staticmethod
    def node_components(node):
        """
        Returns all components of the given node
        :param node: str
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC function node_components() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_is_referenced(node):
        """
        Returns whether given node is referenced or not
        :param node: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function node_is_referenced() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_reference_path(node, without_copy_number=False):
        """
        Returns reference path of the referenced node
        :param node: str
        :param without_copy_number: bool
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_reference_path() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_unreference(node):
        """
        Unreferences given node
        :param node: str
        """

        raise NotImplementedError('abstract DCC function node_unreference() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_is_loaded(node):
        """
        Returns whether given node is loaded or not
        :param node: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function node_is_loaded() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_is_locked(node):
        """
        Returns whether given node is locked or not
        :param node: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function node_is_locked() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_children(node, all_hierarchy=True, full_path=True):
        """
        Returns a list of children of the given node
        :param node: str
        :param all_hierarchy: bool
        :param full_path: bool
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function node_children() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_parent(node, full_path=True):
        """
        Returns parent node of the given node
        :param node: str
        :param full_path: bool
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_parent() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_root(node, full_path=True):
        """
        Returns hierarchy root node of the given node
        :param node: str
        :param full_path: bool
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_root() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_parent(node, parent):
        """
        Sets the node parent to the given parent
        :param node: str
        :param parent: str
        """

        raise NotImplementedError('abstract DCC function set_parent() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_shape_parent(shape, transform_node):
        """
        Sets given shape parent
        :param shape: str
        :param transform_node: str
        """

        raise NotImplementedError('abstract DCC function set_shape_parent() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_parent_to_world(node):
        """
        Parent given node to the root world node
        :param node: str
        """

        raise NotImplementedError('abstract DCC function set_parent_to_world() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_nodes(node):
        """
        Returns referenced nodes of the given node
        :param node: str
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function node_nodes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_filename(node, no_copy_number=True):
        """
        Returns file name of the given node
        :param node: str
        :param no_copy_number: bool
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_filename() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_matrix(node):
        """
        Returns the world matrix of the given node
        :param node: str
        :return:
        """

        raise NotImplementedError('abstract DCC function node_matrix() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_node_matrix(node, matrix):
        """
        Sets the world matrix of the given node
        :param node: str
        :param matrix: variant
        :return:
        """

        raise NotImplementedError('abstract DCC function set_node_matrix() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def show_node(node):
        """
        Shows given node
        :param node: str
        """

        raise NotImplementedError('abstract DCC function show_node() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def hide_node(node):
        """
        Hides given node
        :param node: str
        """

        raise NotImplementedError('abstract DCC function hide_node() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_node_types(type_string):
        """
        List all dependency node types satisfying given classification string
        :param type_string: str
        :return:
        """

        raise NotImplementedError('abstract DCC function list_node_types() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_nodes(node_name=None, node_type=None, full_path=True):
        """
        Returns list of nodes with given types. If no type, all scene nodes will be listed
        :param node_name:
        :param node_type:
        :param full_path:
        :return:  list<str>
        """

        raise NotImplementedError('abstract DCC function list_nodes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_children(node, all_hierarchy=True, full_path=True, children_type=None):
        """
        Returns a list of children nodes of the given node
        :param node:
        :param all_hierarchy:
        :param full_path:
        :param children_type:
        :return:
        """

        raise NotImplementedError('abstract DCC function list_children() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_relatives(
            node, all_hierarchy=False, full_path=True, relative_type=None, shapes=False, intermediate_shapes=False):
        """
        Returns a list of relative nodes of the given node
        :param node:
        :param all_hierarchy:
        :param full_path:
        :param relative_type:
        :param shapes:
        :param intermediate_shapes:
        :return:
        """

        raise NotImplementedError('abstract DCC function list_relatives() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_is_a_shape(node):
        """
        Returns whether or not given node is a shape one
        :param node: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function node_is_a_shape() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_shapes(node, full_path=True, intermediate_shapes=False):
        """
        Returns a list of shapes of the given node
        :param node: str
        :param full_path: bool
        :param intermediate_shapes: bool
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_shapes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_shapes_of_type(node, shape_type=None, full_path=True, intermediate_shapes=False):
        """
        Returns a list of shapes of the given node
        :param node: str
        :param shape_type: str
        :param full_path: bool
        :param intermediate_shapes: bool
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_shapes_of_type() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_has_shape_of_type(node, shape_type):
        """
        Returns whether or not given node has a shape of the given type attached to it
        :param node: str
        :param shape_type: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function node_has_shape_of_type() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_children_shapes(node, all_hierarchy=True, full_path=True):
        """
        Returns a list of children shapes of the given node
        :param node:
        :param all_hierarchy:
        :param full_path:
        :return:
        """

        raise NotImplementedError('abstract DCC function list_children_shapes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def shape_transform(shape_node):
        """
        Returns the transform parent of the given shape node
        :param shape_node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function shape_transform() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_bounding_box_pivot(node):
        """
        Returns the bounding box pivot center of the given node
        :param node: str
        :return: list(float, float, float)
        """

        raise NotImplementedError('abstract DCC function node_bounding_box_pivot_center() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def shapes_bounding_box_pivot(shapes):
        """
        Returns the bounding box pivot center point of the given meshes
        :param shapes: list(str)
        :return: list(float, float, float)
        """

        raise NotImplementedError('abstract DCC function shapes_bounding_box_pivot_center() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def default_shaders():
        """
        Returns a list with all thte default shadres of the current DCC
        :return: str
        """

        raise NotImplementedError('abstract DCC function default_shaders() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_surface_shader(shader_name, **kwargs):
        """
        Creates a new basic DCC surface shader
        :param shader_name: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function create_surface_shader() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def apply_shader(material, node):
        """
        Applies shader to given node
        :param material: str
        :param node: str
        """

        raise NotImplementedError('abstract DCC function apply_shader() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_materials(skip_default_materials=False, nodes=None):
        """
        Returns a list of materials in the current scene or given nodes
        :param skip_default_materials: bool, Whether to return also standard materials or not
        :param nodes: list(str), list of nodes we want to search materials into. If not given, all scene materials
            will be retrieved
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC function list_materials() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def scene_namespaces():
        """
        Returns all the available namespaces in the current scene
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC function scene_namespaces() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def change_namespace(old_namespace, new_namespace):
        """
        Changes old namespace by a new one
        :param old_namespace: str
        :param new_namespace: str
        """

        raise NotImplementedError('abstract DCC function change_namespace() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def change_filename(node, new_filename):
        """
        Changes filename of a given reference node
        :param node: str
        :param new_filename: str
        """

        raise NotImplementedError('abstract DCC function change_filename() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def import_reference(filename):
        """
        Imports object from reference node filename
        :param filename: str
        """

        raise NotImplementedError('abstract DCC function import_reference() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def attribute_default_value(node, attribute_name):
        """
        Returns default value of the attribute in the given node
        :param node: str
        :param attribute_name: str
        :return: object
        """

        raise NotImplementedError('abstract DCC function attribute_default_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_attributes(node, **kwargs):
        """
        Returns list of attributes of given node
        :param node: str
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_user_attributes(node):
        """
        Returns list of user defined attributes
        :param node: str
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_user_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_bool_attribute(node, attribute_name, default_value=False, **kwargs):
        """
        Adds a new boolean attribute into the given node
        :param node: str
        :param attribute_name: str
        :param default_value: bool
        :return:
        """

        raise NotImplementedError('abstract DCC function add_bool_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_integer_attribute(node, attribute_name, default_value=0, **kwargs):
        """
        Adds a new float attribute into the given node
        :param node: str
        :param attribute_name: str
        :param default_value: float
        :return:
        """

        raise NotImplementedError('abstract DCC function add_integer_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_float_attribute(node, attribute_name, default_value=0.0, **kwargs):
        """
        Adds a new boolean float into the given node
        :param node: str
        :param attribute_name: str
        :param default_value: float
        :return:
        """

        raise NotImplementedError('abstract DCC function add_float_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_double_attribute(node, attribute_name, default_value=0.0, **kwargs):
        """
        Adds a new boolean float into the given node
        :param node: str
        :param attribute_name: str
        :param default_value: float
        :return:
        """

        raise NotImplementedError('abstract DCC function add_double_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_string_attribute(node, attribute_name, default_value='', **kwargs):
        """
        Adds a new string attribute into the given node
        :param node: str
        :param attribute_name: str
        :param default_value: str
        """

        raise NotImplementedError('abstract DCC function add_string_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_string_array_attribute(node, attribute_name, **kwargs):
        """
        Adds a new string array attribute into the given node
        :param node: str
        :param attribute_name: str
        """

        raise NotImplementedError('abstract DCC function add_string_array_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_title_attribute(node, attribute_name, **kwargs):
        """
        Adds a new title attribute into the given node
        :param node: str
        :param attribute_name: str
        :param kwargs:
        :return:
        """

        raise NotImplementedError('abstract DCC function add_title_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_message_attribute(node, attribute_name, **kwargs):
        """
        Adds a new message attribute into the given node
        :param node: str
        :param attribute_name: str
        """

        raise NotImplementedError('abstract DCC function add_message_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def attribute_query(node, attribute_name, **kwargs):
        """
        Returns attribute qyer
        :param node: str
        :param attribute_name: str
        :param kwargs:
        :return:
        """

        raise NotImplementedError('abstract DCC function attribute_query() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def attribute_exists(node, attribute_name):
        """
        Returns whether given attribute exists in given node
        :param node: str
        :param attribute_name: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function attribute_exists() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def is_attribute_locked(node, attribute_name):
        """
        Returns whether given attribute is locked or not
        :param node: str
        :param attribute_name: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function is_attribute_locked() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def is_attribute_connected(self, node, attribute_name):
        """
        Returns whether given attribute is connected or not
        :param node: str
        :param attribute_name: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function is_attribute_connected() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_maximum_integer_attribute_value(node, attribute_name):
        """
        Returns the maximum value that a specific integer attribute has set
        :param node: str
        :param attribute_name: str
        :return: float
        """

        raise NotImplementedError('abstract DCC function get_maximum_integer_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_maximum_integer_attribute_value(node, attribute_name, max_value):
        """
        Sets the maximum value that a specific integer attribute has set
        :param node: str
        :param attribute_name: str
        :param max_value: float
        """

        raise NotImplementedError('abstract DCC function set_maximum_integer_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_maximum_float_attribute_value(node, attribute_name):
        """
        Returns the maximum value that a specific attribute has set
        :param node: str
        :param attribute_name: str
        :return: float
        """

        raise NotImplementedError('abstract DCC function get_maximum_float_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_maximum_float_attribute_value(node, attribute_name, max_value):
        """
        Sets the maximum value that a specific attribute has set
        :param node: str
        :param attribute_name: str
        :param max_value: float
        """

        raise NotImplementedError('abstract DCC function set_maximum_float_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_minimum_integer_attribute_value(node, attribute_name):
        """
        Returns the minimum value that a specific integer attribute has set
        :param node: str
        :param attribute_name: str
        :return: float
        """

        raise NotImplementedError('abstract DCC function get_minimum_integer_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_minimum_integer_attribute_value(node, attribute_name, min_value):
        """
        Sets the minimum value that a specific integer attribute has set
        :param node: str
        :param attribute_name: str
        :param min_value: float
        """

        raise NotImplementedError('abstract DCC function set_minimum_integer_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_minimum_float_attribute_value(node, attribute_name):
        """
        Returns the minimum value that a specific float attribute has set
        :param node: str
        :param attribute_name: str
        :return: float
        """

        raise NotImplementedError('abstract DCC function get_minimum_float_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_minimum_float_attribute_value(node, attribute_name, min_value):
        """
        Sets the minimum value that a specific float attribute has set
        :param node: str
        :param attribute_name: str
        :param min_value: float
        """

        raise NotImplementedError('abstract DCC function set_minimum_float_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def show_attribute(node, attribute_name):
        """
        Shows attribute in DCC UI
        :param node: str
        :param attribute_name: str
        """

        raise NotImplementedError('abstract DCC function show_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def hide_attribute(node, attribute_name):
        """
        Hides attribute in DCC UI
        :param node: str
        :param attribute_name: str
        """

        raise NotImplementedError('abstract DCC function hide_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def hide_attributes(node, attributes_list):
        """
        Hides given attributes in DCC UI
        :param node: str
        :param attributes_list: list(str)
        """

        raise NotImplementedError('abstract DCC function hide_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def lock_attributes(node, attributes_list, **kwargs):
        """
        Locks given attributes in DCC UI
        :param node: str
        :param attributes_list: list(str)
        :param kwargs:
        """

        raise NotImplementedError('abstract DCC function lock_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def keyable_attribute(node, attribute_name):
        """
        Makes given attribute keyable
        :param node: str
        :param attribute_name: str
        """

        raise NotImplementedError('abstract DCC function keyable_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def unkeyable_attribute(node, attribute_name):
        """
        Makes given attribute unkeyable
        :param node: str
        :param attribute_name: str
        """

        raise NotImplementedError('abstract DCC function unkeyable_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def lock_attribute(node, attribute_name):
        """
        Locks given attribute in given node
        :param node: str
        :param attribute_name: str
        """

        raise NotImplementedError('abstract DCC function lock_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def unlock_attribute(node, attribute_name):
        """
        Locks given attribute in given node
        :param node: str
        :param attribute_name: str
        """

        raise NotImplementedError('abstract DCC function unlock_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def hide_translate_attributes(node):
        """
        Hides all translate transform attributes of the given node
        :param node: str
        """

        raise NotImplementedError('abstract DCC function hide_translate_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def lock_translate_attributes(node):
        """
        Locks all translate transform attributes of the given node
        :param node: str
        """

        raise NotImplementedError('abstract DCC function lock_translate_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def hide_rotate_attributes(node):
        """
        Hides all rotate transform attributes of the given node
        :param node: str
        """

        raise NotImplementedError('abstract DCC function hide_rotate_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def lock_rotate_attributes(node):
        """
        Locks all rotate transform attributes of the given node
        :param node: str
        """

        raise NotImplementedError('abstract DCC function lock_rotate_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def hide_scale_attributes(node):
        """
        Hides all scale transform attributes of the given node
        :param node: str
        """

        raise NotImplementedError('abstract DCC function hide_scale_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def lock_scale_attributes(node):
        """
        Locks all scale transform attributes of the given node
        :param node: str
        """

        raise NotImplementedError('abstract DCC function lock_scale_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def hide_visibility_attribute(node):
        """
        Hides visibility attribute of the given node
        :param node: str
        """

        raise NotImplementedError('abstract DCC function hide_visibility_attribute() not implemented!')

    @staticmethod
    def lock_visibility_attribute(node):
        """
        Locks visibility attribute of the given node
        :param node: str
        """

        raise NotImplementedError('abstract DCC function lock_visibility_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def hide_scale_and_visibility_attributes(node):
        """
        Hides scale and visibility attributes of the given node
        :param node: str
        """

        raise NotImplementedError('abstract DCC function hide_scale_and_visibility_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def lock_scale_and_visibility_attributes(node):
        """
        Locks scale and visibility attributes of the given node
        :param node: str
        """

        raise NotImplementedError('abstract DCC function lock_scale_and_visibility_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def hide_keyable_attributes(node):
        """
        Hides all node attributes that are keyable
        :param node: str
        """

        raise NotImplementedError('abstract DCC function hide_keyable_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def lock_keyable_attributes(node):
        """
        Locks all node attributes that are keyable
        :param node: str
        """

        raise NotImplementedError('abstract DCC function lock_keyable_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_attribute_value(node, attribute_name):
        """
        Returns the value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :return: variant
        """

        raise NotImplementedError('abstract DCC function get_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_attribute_type(node, attribut_name):
        """
        Returns the type of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :return: variant
        """

        raise NotImplementedError('abstract DCC function get_attribute_type() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_attribute_by_type(node, attribute_name, attribute_value, attribute_type):
        """
        Sets the value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :param attribute_value: variant
        :param attribute_type: str
        """

        raise NotImplementedError('abstract DCC function set_attribute_by_type() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_boolean_attribute_value(node, attribute_name, attribute_value):
        """
        Sets the boolean value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :param attribute_value: int
        :return:
        """

        raise NotImplementedError('abstract DCC function set_boolean_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_numeric_attribute_value(node, attribute_name, attribute_value, clamp=False):
        """
        Sets the integer value of the given attribute in the given node
       :param node: str
        :param attribute_name: str
        :param attribute_value: int
        :param clamp: bool
        :return:
        """

        raise NotImplementedError('abstract DCC function set_numeric_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_integer_attribute_value(node, attribute_name, attribute_value, clamp=False):
        """
        Sets the integer value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :param attribute_value: int
        :param clamp: bool
        :return:
        """

        raise NotImplementedError('abstract DCC function set_integer_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_float_attribute_value(node, attribute_name, attribute_value, clamp=False):
        """
        Sets the integer value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :param attribute_value: int
        :param clamp: bool
        :return:
        """

        raise NotImplementedError('abstract DCC function set_float_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_string_attribute_value(node, attribute_name, attribute_value):
        """
        Sets the string value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :param attribute_value: str
        """

        raise NotImplementedError('abstract DCC function set_string_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_float_vector3_attribute_value(node, attribute_name, attribute_value):
        """
        Sets the float vector3 value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :param attribute_value: str
        """

        raise NotImplementedError('abstract DCC function set_vector3_attribute_name() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_inherits_transform(node):
        """
        Returns whether or not given node inherits its parent transforms
        :param node: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function node_inherits_transform() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_node_inherits_transform(node, flag):
        """
        Sets whether or not given node inherits parent transforms or not
        :param node: str
        :param flag: bool
        """

        raise NotImplementedError('abstract DCC function set_node_inherits_transform() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def reset_transform_attributes(node):
        """
        Reset all transform attributes of the given node
        :param node: str
        """

        raise NotImplementedError('abstract DCC function set_vector3_attribute_name() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def delete_attribute(node, attribute_name):
        """
        Deletes given attribute of given node
        :param node: str
        :param attribute_name: str
        """

        raise NotImplementedError('abstract DCC function delete_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def delete_multi_attribute(node, attribute_name, attribute_index):
        """
        Deletes given multi attribute of given node
        :param node: str
        :param attribute_name:str
        :param attribute_index: int or str
        """

        raise NotImplementedError('abstract DCC function delete_multi_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def delete_user_defined_attributes(node):
        """
        Removes all attributes in the given node that have been created by a user
        :param node: str
        """

        raise NotImplementedError('abstract DCC function delete_user_defined_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def connect_attribute(source_node, source_attribute, target_node, target_attribute, force=False):
        """
        Connects source attribute to given target attribute
        :param source_node: str
        :param source_attribute: str
        :param target_node: str
        :param target_attribute: str
        :param force: bool
        """

        raise NotImplementedError('abstract DCC function connect_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def connect_translate(source_node, target_node):
        """
        Connects the translation of the source node into the rotation of the target node
        :param source_node: str
        :param target_node: str
        """

        raise NotImplementedError('abstract DCC function connect_translate() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def connect_rotate(source_node, target_node):
        """
        Connects the rotation of the source node into the rotation of the target node
        :param source_node: str
        :param target_node: str
        """

        raise NotImplementedError('abstract DCC function connect_rotate() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def connect_visibility(control_and_attr, target_node, default_value=True):
        """
        Connect the visibility of the target node into an attribute
        :param control_and_attr: str, node.attribute name of a node. If it does not exists, it will ber created
        :param target_node: str, target node to connect its visibility into the attribute
        :param default_value: bool, Whether you want the visibility on/off by default
        """

        raise NotImplementedError('abstract DCC function connect_visibility() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def connect_message_attribute(source_node, target_node, message_attribute):
        """
        Connects the message attribute of the input_node into a custom message attribute on target_node
        :param source_node: str, name of a node
        :param target_node: str, name of a node
        :param message_attribute: str, name of the message attribute to create and connect into. If already exists,
        just connect
        """

        raise NotImplementedError('abstract DCC function connect_message_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_message_attributes(node, **kwargs):
        """
        Returns all message attributes of the give node
        :param node: str
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC function connect_message_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_attribute_input(attribute_node, **kwargs):
        """
        Returns the input into given attribute
        :param attribute_node: str, full node and attribute (node.attribute) attribute we want to retrieve inputs of
        :param kwargs:
        :return: str
        """

        raise NotImplementedError('abstract DCC function get_attribute_input() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_message_input(node, message_attribute):
        """
        Get the input value of a message attribute
        :param node: str
        :param message_attribute: str
        :return: object
        """

        raise NotImplementedError('abstract DCC function get_message_input() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def store_world_matrix_to_attribute(node, attribute_name='worldMatrix', **kwargs):
        """
        Stores world matrix of given transform into an attribute in the same transform
        :param node: str
        :param attribute_name: str
        :param kwargs:
        """

        raise NotImplementedError('abstract DCC function store_world_matrix_to_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_connections(node, attribute_name):
        """
        List the connections of the given out attribute in given node
        :param node: str
        :param attribute_name: str
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_connections() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_connections_of_type(node, connection_type):
        """
        Returns a list of connections with the given type in the given node
        :param node: str
        :param connection_type: str
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_connections_of_type() not implemented!')

    @staticmethod
    def list_node_connections(node):
        """
        Returns all connections of the given node
        :param node: str
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC function list_node_connections() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_source_destination_connections(node):
        """
        Returns source and destination connections of the given node
        :param node: str
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_source_destination_connections() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_source_connections(node):
        """
        Returns source connections of the given node
        :param node: str
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_source_connections() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_destination_connections(node):
        """
        Returns source connections of the given node
        :param node: str
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_destination_connections() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def new_file(force=True):
        """
        Creates a new file
        :param force: bool
        """

        raise NotImplementedError('abstract DCC function new_file() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def open_file(file_path, force=True):
        """
        Open file in given path
        :param file_path: str
        :param force: bool
        """

        raise NotImplementedError('abstract DCC function open_file() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def import_file(file_path, force=True, **kwargs):
        """
        Imports given file into current DCC scene
        :param file_path: str
        :param force: bool
        :return:
        """

        raise NotImplementedError('abstract DCC function import_file() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def reference_file(file_path, force=True, **kwargs):
        """
        References given file into current DCC scene
        :param file_path: str
        :param force: bool
        :param kwargs: keyword arguments
        :return:
        """

        raise NotImplementedError('abstract DCC function reference_file() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def is_plugin_loaded(plugin_name):
        """
        Return whether given plugin is loaded or not
        :param plugin_name: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function is_plugin_loaded() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def load_plugin(plugin_path, quiet=True):
        """
        Loads given plugin
        :param plugin_path: str
        :param quiet: bool
        """

        raise NotImplementedError('abstract DCC function load_plugin() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def unload_plugin(plugin_path):
        """
        Unloads the given plugin
        :param plugin_path: str
        """

        raise NotImplementedError('abstract DCC function unload_plugin() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_old_plugins():
        """
        Returns a list of old plugins in the current scene
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_old_plugins() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def remove_old_plugin(plugin_name):
        """
        Removes given old plugin from current scene
        :param plugin_name: str
        """

        raise NotImplementedError('abstract DCC function list_old_plugins() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def is_component_mode():
        """
        Returns whether current DCC selection mode is component mode or not
        :return: bool
        """

        raise NotImplementedError('abstract DCC function is_component_mode() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def scene_name():
        """
        Returns the name of the current scene
        :return: str
        """

        raise NotImplementedError('abstract DCC function scene_name() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def scene_is_modified():
        """
        Returns whether current scene has been modified or not since last save
        :return: bool
        """

        raise NotImplementedError('abstract DCC function scene_is_modified() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def save_current_scene(force=True, **kwargs):
        """
        Saves current scene
        :param force: bool
        """

        raise NotImplementedError('abstract DCC function save_current_scene() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def confirm_dialog(title, message, button=None, cancel_button=None, default_button=None, dismiss_string=None):
        """
        Shows DCC confirm dialog
        :param title:
        :param message:
        :param button:
        :param cancel_button:
        :param default_button:
        :param dismiss_string:
        :return:
        """

        raise NotImplementedError('abstract DCC function confirm_dialog() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def warning(message):
        """
        Prints a warning message
        :param message: str
        :return:
        """

        raise NotImplementedError('abstract DCC function warning() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def error(message):
        """
        Prints a error message
        :param message: str
        :return:
        """

        raise NotImplementedError('abstract DCC function error() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def show_message_in_viewport(msg, **kwargs):
        """
        Shows a message in DCC viewport
        :param msg: str, Message to show
        :param kwargs: dict, extra arguments
        """

        raise NotImplementedError('abstract DCC show_message_in_viewport error() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_shelf_menu_item(parent, label, command='', icon=''):
        """
        Adds a new menu item
        :param parent:
        :param label:
        :param command:
        :param icon:
        :return:
        """

        raise NotImplementedError('abstract DCC function add_shelf_menu_item() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_shelf_sub_menu_item(parent, label, icon=''):
        """
        Adds a new sub menu item
        :param parent:
        :param label:
        :param icon:
        :return:
        """

        raise NotImplementedError('abstract DCC function add_shelf_sub_menu_item() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_shelf_separator(shelf_name):
        """
        Adds a new separator to the given shelf
        :param shelf_name: str
        """

        raise NotImplementedError('abstract DCC function add_shelf_separator() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def shelf_exists(shelf_name):
        """
        Returns whether given shelf already exists or not
        :param shelf_name: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function shelf_exists() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_shelf(shelf_name, shelf_label=None):
        """
        Creates a new shelf with the given name
        :param shelf_name: str
        :param shelf_label: str
        """

        raise NotImplementedError('abstract DCC function create_shelf() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def delete_shelf(shelf_name):
        """
        Deletes shelf with given name
        :param shelf_name: str
        """

        raise NotImplementedError('abstract DCC function delete_shelf() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def select_file_dialog(title, start_directory=None, pattern=None):
        """
        Shows select file dialog
        :param title: str
        :param start_directory: str
        :param pattern: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function select_file_dialog() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def select_folder_dialog(title, start_directory=None):
        """
        Shows select folder dialog
        :param title: str
        :param start_directory: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function select_folder_dialog() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def save_file_dialog(title, start_directory=None, pattern=None):
        """
        Shows save file dialog
        :param title: str
        :param start_directory: str
        :param pattern: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function save_file_dialog() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_start_frame():
        """
        Returns current start frame
        :return: int
        """

        raise NotImplementedError('abstract DCC function get_start_frame() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_end_frame():
        """
        Returns current end frame
        :return: int
        """

        raise NotImplementedError('abstract DCC function get_end_frame() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_current_frame():
        """
        Returns current frame set in time slider
        :return: int
        """

        raise NotImplementedError('abstract DCC function get_current_frame() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_current_frame(frame):
        """
        Sets the current frame in time slider
        :param frame: int
        """

        raise NotImplementedError('abstract DCC function set_current_frame() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_time_slider_range():
        """
        Return the time range from Maya time slider
        :return: list<int, int>
        """

        raise NotImplementedError('abstract DCC function get_time_slider_range() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def fit_view(animation=True):
        """
        Fits current viewport to current selection
        :param animation: bool, Animated fit is available
        """

        raise NotImplementedError('abstract DCC function fit_view() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def refresh_viewport():
        """
        Refresh current DCC viewport
        """

        raise NotImplementedError('abstract DCC function refresh_viewport() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_key_frame(node, attribute_name, **kwargs):
        """
        Sets keyframe in given attribute in given node
        :param node: str
        :param attribute_name: str
        :param kwargs:
        :return:
        """

        raise NotImplementedError('abstract DCC function set_key_frame() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def copy_key(node, attribute_name, time=None):
        """
        Copy key frame of given node
        :param node: str
        :param attribute_name: str
        :param time: bool
        :return:
        """

        raise NotImplementedError('abstract DCC function copy_key() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def cut_key(node, attribute_name, time=None):
        """
        Cuts key frame of given node
        :param node: str
        :param attribute_name: str
        :param time: bool
        :return:
        """

        raise NotImplementedError('abstract DCC function cut_key() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def paste_key(node, attribute_name, option, time, connect):
        """
        Paste copied key frame
        :param node: str
        :param attribute_name: str
        :param option: str
        :param time: (int, int)
        :param connect: bool
        :return:
        """

        raise NotImplementedError('abstract DCC function paste_key() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def offset_keyframes(node, attribute_name, start_time, end_time, duration):
        """
        Offset given node keyframes
        :param node: str
        :param attribute_name: str
        :param start_time: int
        :param end_time: int
        :param duration: float
        """

        raise NotImplementedError('abstract DCC function offset_keyframes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def find_next_key_frame(node, attribute_name, start_time, end_time):
        """
        Returns next keyframe of the given one
        :param node: str
        :param attribute_name: str
        :param start_time: int
        :param end_time: int
        """

        raise NotImplementedError('abstract DCC function offset_keyframes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_flat_key_frame(self, node, attribute_name, start_time, end_time):
        """
        Sets flat tangent in given keyframe
        :param node: str
        :param attribute_name: str
        :param start_time: int
        :param end_time: int
        """

        raise NotImplementedError('abstract DCC function set_flat_key_frame() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def find_first_key_in_anim_curve(curve):
        """
        Returns first key frame of the given curve
        :param curve: str
        :return: int
        """

        raise NotImplementedError('abstract DCC function find_first_key_in_curve() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def find_last_key_in_anim_curve(curve):
        """
        Returns last key frame of the given curve
        :param curve: str
        :return: int
        """

        raise NotImplementedError('abstract DCC function find_last_key_in_curve() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def copy_anim_curve(curve, start_time, end_time):
        """
        Copies given anim curve
        :param curve: str
        :param start_time: int
        :param end_time: int
        """

        raise NotImplementedError('abstract DCC function copy_anim_curve() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_current_model_panel():
        """
        Returns the current model panel name
        :return: str | None
        """

        raise NotImplementedError('abstract DCC function current_model_panel() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def enable_undo():
        """
        Enables undo functionality
        """

        raise NotImplementedError('abstract DCC function enable_undo() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def disable_undo():
        """
        Disables undo functionality
        """

        raise NotImplementedError('abstract DCC function disable_undo() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def focus(object_to_focus):
        """
        Focus in given object
        :param object_to_focus: str
        """

        raise NotImplementedError('abstract DCC function() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def find_unique_name(
            obj_names=None, filter_type=None, include_last_number=True, do_rename=False,
            search_hierarchy=False, selection_only=True, **kwargs):
        """
        Returns a unique node name by adding a number to the end of the node name
        :param obj_names: str, name or list of names to find unique name from
        :param filter_type: str, find unique name on nodes that matches given filter criteria
        :param include_last_number: bool
        :param do_rename: bool
       :param search_hierarchy: bool, Whether to search objects in hierarchies
        :param selection_only: bool, Whether to search only selected objects or all scene object
        :return: str
        """

        raise NotImplementedError('abstract DCC find_unique_name() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def find_available_name(self, *args, **kwargs):
        """
        Returns an available object name in current DCC scene
        :param args: list
        :param kwargs: dict
        :return: str
        """

        raise NotImplementedError('abstract DCC find_available_name() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def clean_scene():
        """
        Cleans invalid nodes from current scene
        """

        raise NotImplementedError('abstract DCC clean_scene() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def is_camera(node_name):
        """
        Returns whether given node is a camera or not
        :param node_name: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC is_camera() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_all_cameras(full_path=True):
        """
        Returns all cameras in the scene
        :param full_path: bool
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC get_all_cameras() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_current_camera(full_path=True):
        """
        Returns camera currently being used in scene
        :param full_path: bool
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC get_current_camera() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def look_through_camera(camera_name):
        """
        Updates DCC viewport to look through given camera
        :param camera_name: str
        :return:
        """

        raise NotImplementedError('abstract DCC look_through_camera() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_camera_focal_length(camera_name):
        """
        Returns focal length of the given camera
        :param camera_name: str
        :return: float
        """

        raise NotImplementedError('abstract DCC get_camera_focal_length() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_playblast_formats():
        """
        Returns a list of supported formats for DCC playblast
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC get_playblast_formats() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_playblast_compressions(playblast_format):
        """
        Returns a list of supported compressions for DCC playblast
        :param playblast_format: str
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC get_playblast_compressions() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_viewport_resolution_width():
        """
        Returns the default width resolution of the current DCC viewport
        :return: int
        """

        raise NotImplementedError('abstract DCC get_viewport_resolution_width() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_viewport_resolution_height():
        """
        Returns the default height resolution of the current DCC viewport
        :return: int
        """

        raise NotImplementedError('abstract DCC get_viewport_resolution_height() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_renderers():
        """
        Returns dictionary with the different renderers supported by DCC
        :return: dict(str, str)
        """

        raise NotImplementedError('abstract DCC get_renderers() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_default_render_resolution_width():
        """
        Returns the default width resolution of the current DCC render settings
        :return: int
        """

        raise NotImplementedError('abstract DCC get_default_render_resolution_width() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_default_render_resolution_height():
        """
        Returns the default height resolution of the current DCC render settings
        :return: int
        """

        raise NotImplementedError('abstract DCC get_default_render_resolution_height() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_default_render_resolution_aspect_ratio():
        """
        Returns the default resolution aspect ratio of the current DCC render settings
        :return: float
        """

        raise NotImplementedError('abstract DCC get_default_render_resolution_aspect_ratio() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def match_translation(source_node, target_node):
        """
        Match translation of the given node to the translation of the target node
        :param source_node: str
        :param target_node: str
        """

        raise NotImplementedError('abstract DCC match_translation() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def match_rotation(source_node, target_node):
        """
        Match rotation of the given node to the rotation of the target node
        :param source_node: str
        :param target_node: str
        """

        raise NotImplementedError('abstract DCC match_rotation() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def match_scale(source_node, target_node):
        """
        Match scale of the given node to the rotation of the target node
        :param source_node: str
        :param target_node: str
        """

        raise NotImplementedError('abstract DCC match_scale() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def match_translation_rotation(source_node, target_node):
        """
        Match translation and rotation of the given node to the translation and rotation of the target node
        :param source_node: str
        :param target_node: str
        """

        raise NotImplementedError('abstract DCC match_translation_rotation() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def match_translation_to_rotate_pivot(source_node, target_node):
        """
        Matches target translation to the source transform rotate pivot
        :param source_node: str
        :param target_node: str
        :return:
        """

        raise NotImplementedError('abstract DCC match_translation_to_rotate_pivot() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def match_transform(source_node, target_node):
        """
        Match the transform (translation, rotation and scale) of the given node to the rotation of the target node
        :param source_node: str
        :param target_node: str
        """

        raise NotImplementedError('abstract DCC match_transform() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def open_render_settings():
        """
        Opens DCC render settings options
        """

        raise NotImplementedError('abstract DCC open_render_settings() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def all_scene_shots():
        """
        Returns all shots in current scene
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC all_scene_shots() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def shot_is_muted(shot_node):
        """
        Returns whether or not given shot node is muted
        :param shot_node: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC shot_is_muted() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def shot_track_number(shot_node):
        """
    Returns track where given shot node is located
        :param shot_node: str
        :return: int
        """

        raise NotImplementedError('abstract DCC shot_track() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def shot_start_frame_in_sequencer(shot_node):
        """
        Returns the start frame of the given shot in sequencer time
        :param shot_node: str
        :return: int
        """

        raise NotImplementedError('abstract DCC shot_start_frame_in_sequencer() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def shot_end_frame_in_sequencer(shot_node):
        """
        Returns the end frame of the given shot in sequencer time
        :param shot_node: str
        :return: int
        """

        raise NotImplementedError('abstract DCC shot_end_frame_in_sequencer() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_pre_hold(shot_node):
        """
        Returns shot prehold value
        :param shot_node: str
        :return: int
        """

        raise NotImplementedError('abstract DCC get_pre_hold() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_post_hold(shot_node):
        """
        Returns shot posthold value
        :param shot_node: str
        :return: int
        """

        raise NotImplementedError('abstract DCC get_post_hold() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def shot_scale(shot_node):
        """
        Returns the scale of the given shot
        :param shot_node: str
        :return: int
        """

        raise NotImplementedError('abstract DCC shot_scale() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def shot_start_frame(shot_node):
        """
        Returns the start frame of the given shot
        :param shot_node: str
        :return: int
        """

        raise NotImplementedError('abstract DCC shot_start_frame() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_shot_start_frame(shot_node, start_frame):
        """
        Sets the start frame of the given shot
        :param shot_node: str
        :param start_frame: int
        :return: int
        """

        raise NotImplementedError('abstract DCC set_shot_start_frame() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def shot_end_frame(shot_node):
        """
        Returns the end frame of the given shot
        :param shot_node: str
        :return: int
        """

        raise NotImplementedError('abstract DCC shot_end_frame() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_shot_end_frame(shot_node, end_frame):
        """
        Sets the end frame of the given shot
        :param shot_node: str
        :param end_frame: int
        :return: int
        """

        raise NotImplementedError('abstract DCC set_shot_end_frame() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def shot_camera(shot_node):
        """
        Returns camera associated given node
        :param shot_node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC shot_camera() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def export_shot_animation_curves(anim_curves_to_export, export_file_path, start_frame, end_frame, **kwargs):
        """
        Exports given shot animation curves in the given path and in the given frame range
        :param anim_curves_to_export: list(str), animation curves to export
        :param export_file_path: str, file path to export animation curves information into
        :param start_frame: int, start frame to export animation from
        :param end_frame: int, end frame to export animation until
        :param args:
        :param kwargs:
        :return:
        """

        raise NotImplementedError('abstract DCC export_animation_curves() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def import_shot_animation_curves(anim_curves_to_import, import_file_path, start_frame, end_frame):
        """
        Imports given shot animation curves in the given path and in the given frame range
        :param anim_curves_to_import: list(str), animation curves to import
        :param import_file_path: str, file path to import animation curves information fron
        :param start_frame: int, start frame to import animation from
        :param end_frame: int, end frame to import animation until
        :param args:
        :param kwargs:
        """

        raise NotImplementedError('abstract DCC import_shot_animation_curves() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_animation_curves(node):
        """
        Returns all animation curves of the given node
        :param node: str
        :return:
        """

        raise NotImplementedError('abstract DCC node_animation_curves() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def all_animation_curves():
        """
        Returns all animation located in current DCC scene
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC all_animation_curves() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def all_keyframes_in_anim_curves(anim_curves=None):
        """
        Retursn al keyframes in given anim curves
        :param anim_curves: list(str)
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC all_keyframes_in_anim_curves() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def key_all_anim_curves_in_frames(frames, anim_curves=None):
        """
        Inserts keyframes on all animation curves on given frame
        :param frames: list(int)
        :param anim_curves: list(str)
        """

        raise NotImplementedError('abstract DCC all_keyframes_in_anim_curves() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def remove_keys_from_animation_curves(range_to_delete, anim_curves=None):
        """
        Inserts keyframes on all animation curves on given frame
        :param range_to_delete: list(int ,int)
        :param anim_curves: list(str)
        """

        raise NotImplementedError('abstract DCC remove_keys_from_animation_curves() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def check_anim_curves_has_fraction_keys(anim_curves, selected_range=None):
        """
        Returns whether or not given curves have or not fraction keys
        :param anim_curves: list(str)
        :param selected_range: list(str)
        :return: bool
        """

        raise NotImplementedError('abstract DCC check_anim_curves_has_fraction_keys() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def convert_fraction_keys_to_whole_keys(animation_curves, consider_selected_range=False):
        """
        Find keys on fraction of a frame and insert a key on the nearest whole number frame
        Useful to make sure that no keys are located on fraction of frames
        :param animation_curves: list(str)
        :param consider_selected_range: bool
        :return:
        """

        raise NotImplementedError('abstract DCC convert_fraction_keys_to_whole_keys() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_active_frame_range(start_frame, end_frame):
        """
        Sets current animation frame range
        :param start_frame: int
        :param end_frame: int
        """

        raise NotImplementedError('abstract DCC set_active_frame_range() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_point_constraint(source, constraint_to, **kwargs):
        """
        Creates a new point constraint
        :param source:
        :param constraint_to:
        :param kwargs:
        :return:
        """

        raise NotImplementedError('abstract DCC create_point_constraint() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_orient_constraint(source, constraint_to, **kwargs):
        """
        Creates a new orient constraint
        :param source:
        :param constraint_to:
        :param kwargs:
        :return:
        """

        raise NotImplementedError('abstract DCC create_orient_constraint() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_scale_constraint(source, constraint_to, **kwargs):
        """
        Creates a new scale constraint
        :param source:
        :param constraint_to:
        :param kwargs:
        :return:
        """

        raise NotImplementedError('abstract DCC create_scale_constraint() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_parent_constraint(source, constraint_to, **kwargs):
        """
        Creates a new parent constraint
        :param source:
        :param constraint_to:
        :param kwargs:
        :return:
        """

        raise NotImplementedError('abstract DCC create_parent_constraint() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_aim_constraint(source, point_to, **kwargs):
        """
        Creates a new aim constraint
        :param source: str
        :param point_to: str
        """

        raise NotImplementedError('abstract DCC create_aim_constraint() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_selection_groups(name=None):
        """
        Returns all selection groups (sets) in current DCC scene
        :param name: str
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC get_selection_groupsº() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_is_selection_group(node):
        """
        Returns whether or not given node is a selection group (set)
        :param node: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC create_selection_group() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_selection_group(name, empty=False):
        """
        Creates a new DCC selection group
        :param name: str
        :param empty: bool
        :return: str
        """

        raise NotImplementedError('abstract DCC create_selection_group() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_node_to_selection_group(node, selection_group_name):
        """
        Adds given node to selection group
        :param node: str
        :param selection_group_name: str
        :return: str
        """

        raise NotImplementedError('abstract DCC add_node_to_selection_group() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def zero_transform_attribute_channels(node):
        """
        Sets to zero all transform attribute channels of the given node (transform rotate and scale)
        :param node: str
        """

        raise NotImplementedError('abstract DCC zero_transform_attribute_channels() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def zero_scale_joint(jnt):
        """
        Sets the given scale to zero and compensate the change by modifying the joint translation and rotation
        :param jnt: str
        """

        raise NotImplementedError('abstract DCC zero_scale_joint() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_joint_orient(jnt, orient_axis, secondary_orient_axis=None, **kwargs):
        """
        Sets the joint orientation and scale orientation so that the axis indicated by the first letter in the
         argument will be aligned with the vector from this joint to its first child joint.
        :param jnt: str
        :param orient_axis: str
        :param secondary_orient_axis: str
        :return:
        """

        raise NotImplementedError('abstract DCC set_joint_orient() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def attach_joints(source_chain, target_chain, **kwargs):
        """
        Attaches a chain of joints to a matching chain
        :param source_chain: str
        :param target_chain: str
        """

        raise NotImplementedError('abstract DCC zero_scale_joint() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_hierarchy(transforms, replace_str=None, new_str=None):
        """
        Creates a transforms hierarchy with the given list of joints
        :param transforms: list(str)
        :param replace_str: str, if given this string will be replace with the new_str
        :param new_str: str, if given replace_str will be replace with this string
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC create_hierarchy() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def duplicate_hierarchy(transforms, stop_at=None, force_only_these=None, replace_str=None, new_str=None):
        """
        Duplicates given hierarchy of transform nodes
        :param transforms: list(str), list of joints to duplicate
        :param stop_at: str, if given the duplicate process will be stop in the given node
        :param force_only_these: list(str), if given only these list of transforms will be duplicated
        :param replace_str: str, if given this string will be replace with the new_str
        :param new_str: str, if given replace_str will be replace with this string
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC duplicate_hierarchy() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def delete_history(node):
        """
        Removes the history of the given node
        """

        raise NotImplementedError('abstract DCC delete_history() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def freeze_transforms(node, **kwargs):
        """
        Freezes the transformations of the given node and its children
        :param node: str
        """

        raise NotImplementedError('abstract DCC freeze_transforms() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def move_pivot_to_zero(node):
        """
        Moves pivot of given node to zero (0, 0, 0 in the world)
        :param node: str
        """

        raise NotImplementedError('abstract DCC move_pivot_to_zero() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def combine_meshes(meshes_to_combine=None, **kwargs):
        """
        Combines given meshes into one unique mesh. If no meshes given, all selected meshes will be combined
        :param meshes_to_combine: list(str) or None
        :return: str
        """

        raise NotImplementedError('abstract DCC combine_meshes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def reset_node_transforms(node, **kwargs):
        """
        Reset the transformations of the given node and its children
        :param node: str
        """

        raise NotImplementedError('abstract DCC reset_node_transforms() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_node_rotation_axis_in_object_space(node, x, y, z):
        """
        Sets the rotation axis of given node in object space
        :param node: str
        :param x: int
        :param y: int
        :param z: int
        """

        raise NotImplementedError('abstract DCC set_node_rotation_axis_in_object_space() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def filter_nodes_by_type(filter_type, search_hierarchy=False, selection_only=True, **kwargs):
        """
        Returns list of nodes in current scene filtered by given filter
        :param filter_type: str, filter used to filter nodes to edit index of
        :param search_hierarchy: bool, Whether to search objects in hierarchies
        :param selection_only: bool, Whether to search all scene objects or only selected ones
        :param kwargs:
        :return: list(str), list of filtered nodes
        """

        raise NotImplementedError('abstract DCC filter_nodes_by_type() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_name_prefix(
            prefix, obj_names=None, filter_type=None, search_hierarchy=False, selection_only=True, **kwargs):
        """
        Add prefix to node name
        :param prefix: str, string to add to the start of the current node name
        :param obj_names: str or list(str), name of list of node names to rename
        :param filter_type: str, name of object type to filter the objects to apply changes ('Group, 'Joint', etc)
        :param search_hierarchy: bool, Whether to search objects in hierarchies
        :param selection_only: bool, Whether to search only selected objects or all scene objects
        :param kwargs:
        """

        raise NotImplementedError('abstract DCC add_name_prefix() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_name_suffix(
            suffix, obj_names=None, filter_type=None, search_hierarchy=False, selection_only=True, **kwargs):
        """
        Add suffix to node name
        :param suffix: str, string to add to the end of the current node name
        :param obj_names: str or list(str), name of list of node names to rename
        :param filter_type: str, name of object type to filter the objects to apply changes ('Group, 'Joint', etc)
        :param search_hierarchy: bool, Whether to search objects in hierarchies
        :param selection_only: bool, Whether to search only selected objects or all scene objects
        :param kwargs:
        """

        raise NotImplementedError('abstract DCC add_name_suffix() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def remove_name_prefix(
            obj_names=None, filter_type=None, separator='_', search_hierarchy=False, selection_only=True, **kwargs):
        """
        Removes prefix from node name
        :param obj_names: str or list(str), name of list of node names to rename
        :param filter_type: str, name of object type to filter the objects to apply changes ('Group, 'Joint', etc)
        :param separator: str, separator character for the prefix
        :param search_hierarchy: bool, Whether to search objects in hierarchies
        :param selection_only: bool, Whether to search only selected objects or all scene objects
        :param kwargs:
        """

        raise NotImplementedError('abstract DCC remove_name_prefix() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def remove_name_suffix(
            obj_names=None, filter_type=None, separator='_', search_hierarchy=False, selection_only=True, **kwargs):
        """
        Removes suffix from node name
        :param obj_names: str or list(str), name of list of node names to rename
        :param filter_type: str, name of object type to filter the objects to apply changes ('Group, 'Joint', etc)
        :param separator: str, separator character for the suffix
        :param search_hierarchy: bool, Whether to search objects in hierarchies
        :param selection_only: bool, Whether to search only selected objects or all scene objects
        :param kwargs:
        """

        raise NotImplementedError('abstract DCC remove_name_suffix() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def auto_name_suffix(obj_names=None, filter_type=None, search_hierarchy=False, selection_only=True, **kwargs):
        """
        Automatically add a sufix to node names
        :param obj_names: str or list(str), name of list of node names to rename
        :param filter_type: str, name of object type to filter the objects to apply changes ('Group, 'Joint', etc)
        :param separator: str, separator character for the suffix
        :param search_hierarchy: bool, Whether to search objects in hierarchies
        :param selection_only: bool, Whether to search only selected objects or all scene objects
        :param kwargs:
        """

        raise NotImplementedError('abstract DCC auto_name_suffix() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def remove_name_numbers(
            obj_names=None, filter_type=None, search_hierarchy=False, selection_only=True, remove_underscores=True,
            trailing_only=False, **kwargs):
        """
        Removes numbers from node names
        :param obj_names: str or list(str), name of list of node names to rename
        :param filter_type: str, name of object type to filter the objects to apply changes ('Group, 'Joint', etc)
        :param search_hierarchy: bool, Whether to search objects in hierarchies
        :param selection_only: bool, Whether to search only selected objects or all scene objects
        :param remove_underscores: bool, Whether or not to remove unwanted underscores
        :param trailing_only: bool, Whether or not to remove only numbers at the ned of the name
        :param kwargs:
        :return:
        """

        raise NotImplementedError('abstract DCC remove_name_numbers() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def renumber_objects(
            obj_names=None, filter_type=None, remove_trailing_numbers=True, add_underscore=True, padding=2,
            search_hierarchy=False, selection_only=True, **kwargs):
        """
        Removes numbers from node names
        :param obj_names: str or list(str), name of list of node names to rename
        :param filter_type: str, name of object type to filter the objects to apply changes ('Group, 'Joint', etc)
        :param remove_trailing_numbers: bool, Whether to remove trailing numbers before doing the renumber
        :param add_underscore: bool, Whether or not to remove underscore between name and new number
        :param padding: int, amount of numerical padding (2=01, 3=001, etc). Only used if given names has no numbers.
        :param search_hierarchy: bool, Whether to search objects in hierarchies
        :param selection_only: bool, Whether to search only selected objects or all scene objects
        :param kwargs:
        :return:
        """

        raise NotImplementedError('abstract DCC renumber_objects() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def change_suffix_padding(
            obj_names=None, filter_type=None, add_underscore=True, padding=2,
            search_hierarchy=False, selection_only=True, **kwargs):
        """
        Removes numbers from node names
        :param obj_names: str or list(str), name of list of node names to rename
        :param filter_type: str, name of object type to filter the objects to apply changes ('Group, 'Joint', etc)
        :param add_underscore: bool, Whether or not to remove underscore between name and new number
        :param padding: int, amount of numerical padding (2=01, 3=001, etc). Only used if given names has no numbers.
        :param search_hierarchy: bool, Whether to search objects in hierarchies
        :param selection_only: bool, Whether to search only selected objects or all scene objects
        :param kwargs:
        :return:
        """

        raise NotImplementedError('abstract DCC change_suffix_padding() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_vertex_name(mesh_node, vertex_id):
        """
        Returns the full name of the given node vertex
        :param mesh_node: str
        :param vertex_id: int
        :return: str
        """

        raise NotImplementedError('abstract DCC node_vertex_name() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def total_vertices(mesh_node):
        """
        Returns the total number of vertices of the given geometry
        :param mesh_node: str
        :return: int
        """

        raise NotImplementedError('abstract DCC total_vertices() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_vertex_object_space_translation(mesh_node, vertex_id=None):
        """
        Returns the object space translation of the vertex id in the given node
        :param mesh_node: str
        :param vertex_id: int
        :return:
        """

        raise NotImplementedError('abstract DCC node_vertex_object_space_translation() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_vertex_world_space_translation(mesh_node, vertex_id=None):
        """
        Returns the world space translation of the vertex id in the given node
        :param mesh_node: str
        :param vertex_id: int
        :return:
        """

        raise NotImplementedError('abstract DCC node_vertex_world_space_translation() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_node_vertex_object_space_translation(mesh_node, translate_list, vertex_id=None):
        """
        Sets the object space translation of the vertex id in the given node
        :param mesh_node: str
        :param translate_list: list
        :param vertex_id: int
        :return:
        """

        raise NotImplementedError('abstract DCC set_node_vertex_object_space_translation() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_node_vertex_world_space_translation(mesh_node, translate_list, vertex_id=None):
        """
        Sets the world space translation of the vertex id in the given node
        :param mesh_node: str
        :param translate_list: list
        :param vertex_id: int
        :return:
        """

        raise NotImplementedError('abstract DCC set_node_vertex_world_space_translation() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_nurbs_sphere(name='sphere', radius=1.0, **kwargs):
        """
        Creates a new NURBS sphere
        :param name: str
        :param radius: float
        :return: str
        """

        raise NotImplementedError('abstract DCC create_cluster() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_nurbs_cylinder(name='sphere', radius=1.0, **kwargs):
        """
        Creates a new NURBS cylinder
        :param name: str
        :param radius: float
        :return: str
        """

        raise NotImplementedError('abstract DCC create_nurbs_cylinder() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def rebuild_curve(curve, spans, **kwargs):
        """
        Rebuilds curve with given parameters
        :param curve: str
        :param spans: int
        :param kwargs:
        :return:
        """

        raise NotImplementedError('abstract DCC rebuild_curve() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def convert_surface_to_bezier(surface, **kwargs):
        """
        Rebuilds given surface as a bezier surface
        :param surface: str
        :return:
        """

        raise NotImplementedError('abstract DCC convert_surface_to_bezier() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_locator(name='loc'):
        """
        Creates a new locator
        :param name: str
        :return: str
        """

        raise NotImplementedError('abstract DCC create_locator() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_cluster(objects, cluster_name='cluster', **kwargs):
        """
        Creates a new cluster in the given objects
        :param objects: list(str)
        :param cluster_name: str
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC create_cluster() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_decompose_matrix_node(node_name):
        """
        Creates a new decompose matrix node
        :param node_name: str
        :return: str
        """

        raise NotImplementedError('abstract DCC create_decompose_matrix_node() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_empty_mesh(mesh_name):
        """
        Creates a new empty mesh
        :param mesh_name:str
        :return: str
        """

        raise NotImplementedError('abstract DCC create_empty_mesh() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_circle_curve(name, **kwargs):
        """
        Creates a new circle control
        :param name: str
        :param kwargs:
        :return: str
        """

        raise NotImplementedError('abstract DCC create_circle_curve() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_joint(joint_name):
        """
        Creates a new joint
        :param joint_name: str
        :return: str
        """

        raise NotImplementedError('abstract DCC create_joint() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_ik_handle(name, start_joint, end_joint, solver_type=None, curve=None, **kwargs):
        """
        Creates a new IK handle
        :param name: str
        :param start_joint: str
        :param end_joint: str
        :param solver_type: str
        :param curve: str
        :param kwargs:
        :return: str
        """

        raise NotImplementedError('abstract DCC create_ik_handle() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_spline_ik_stretch(
            curve, joints, node_for_attribute=None, create_stretch_on_off=False, stretch_axis='X', **kwargs):
        """
        Makes the joints stretch on the curve
        :param curve: str, name of the curve that joints are attached via Spline IK
        :param joints: list<str>, list of joints attached to Spline IK
        :param node_for_attribute: str, name of the node to create the attributes on
        :param create_stretch_on_off: bool, Whether to create or not extra attributes to slide the stretch value on/off
        :param stretch_axis: str('X', 'Y', 'Z'), axis that the joints stretch on
        :param kwargs:
        """

        raise NotImplementedError('abstract DCC create_spline_ik_stretch() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_cluster_surface(
            surface, name, first_cluster_pivot_at_start=True, last_cluster_pivot_at_end=True, join_ends=False):
        """
        Creates a new clustered surface
        :param surface: str
        :param name: str
        :param first_cluster_pivot_at_start: str
        :param last_cluster_pivot_at_end: str
        :param join_ends: bool
        :return: list(str), list(str)
        """

        raise NotImplementedError('abstract DCC create_cluster_surface() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_cluster_curve(
            curve, name, first_cluster_pivot_at_start=True, last_cluster_pivot_at_end=True, join_ends=False):
        """
        Creates a new clustered curve
        :param curve: str
        :param name: str
        :param first_cluster_pivot_at_start: str
        :param last_cluster_pivot_at_end: str
        :param last_cluster_pivot_at_end: str
        :param join_ends: bool
        :return: list(str), list(str)
        """

        raise NotImplementedError('abstract DCC create_cluster_curve() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_wire(surface, curves, name='wire', **kwargs):
        """
        Creates a new wire that wires given surface to given curves
        :param surface:str
        :param curves: list(str)
        :param name:str
        :param kwargs:
        :return: str, str
        """

        raise NotImplementedError('abstract DCC create_wire() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def attach_transform_to_surface(transform, surface, u=None, v=None, constraint=False, attach_type=None):
        """
        Attaches a transform to given surface
        If no U an V values are given, the command will try to find the closest position on the surface
        :param transform: str, str, name of a transform to follicle to the surface
        :param surface: str, name of a surface to attach follicle to
        :param u: float, U value to attach to
        :param v: float, V value to attach to
        :param constraint: bool
        :param attach_type: bool
        :return: str, name of the follicle created
        """

        raise NotImplementedError('abstract DCC attach_transform_to_surface() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_curve_from_transforms(transforms, spans=None, description='from_transforms'):
        """
        Creates a curve from a list of transforms. Each transform will define a curve CV
        Useful when creating a curve from a joint chain (spines/tails)
        :param transforms: list<str>, list of tranfsorms to generate the curve from. Positions will be used to place CVs
        :param spans: int, number of spans the final curve should have
        :param description: str, description to given to the curve
        :return: str name of the new curve
        """

        raise NotImplementedError('abstract DCC create_curve_from_transforms() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_nurbs_surface_from_transforms(transforms, name, spans=-1, offset_axis='Y', offset_amount=1):
        """
        Creates a NURBS surface from a list of transforms
        Useful for creating a NURBS surface that follows a spine or tail
        :param transforms: list<str>, list of transforms
        :param name: str, name of the surface
        :param spans: int, number of spans to given to the final surface.
        If -1, the surface will have spans based on the number of transforms
        :param offset_axis: str, axis to offset the surface relative to the transform ('X', 'Y' or 'Z')
        :param offset_amount: int, amount the surface offsets from the transform
        :return: str, name of the NURBS surface
        """

        raise NotImplementedError('abstract DCC create_nurbs_surface_from_transforms() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_follow_group(source_transform, target_transform, **kwargs):
        """
        Creates a group above a target transform that is constrained to the source transform
        :param source_transform: str, name of the transform to follow
        :param target_transform: str, name of the transform make follow
        :param source_transform:
        :param target_transform:
        :param kwargs:
        :return:
        """

        raise NotImplementedError('abstract DCC create_empty_mesh() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_constraints():
        """
        Returns all constraints nodes in current DCC scene
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC get_constraints() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_constraint(node, constraint_type):
        """
        Returns a constraint on the transform with the given type
        :param node: str
        :param constraint_type: str
        :return: str
        """

        raise NotImplementedError('abstract DCC node_constraint() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_constraints(node):
        """
        Returns all constraints a node is linked to
        :param node: str
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC node_constraints() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_transforms(node):
        """
        Returns all transforms nodes of a given node
        :param node: str
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC node_transforms() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_joints(node):
        """
        Returns all oints nodes of a give node
        :param node: str
        :return: listr(str)
        """

        raise NotImplementedError('abstract DCC node_joints() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_shape_type(node):
        """
        Returns the type of the given shape node
        :param node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC node_shape_type() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_color_of_side(side='C', sub_color=False):
        """
        Returns override color of the given side
        :param side: str
        :param sub_color: fool, whether to return a sub color or not
        :return:
        """

        raise NotImplementedError('abstract DCC get_color_of_side() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_parent_controller(control, parent_controller):
        """
        Sets the parent controller of the given control
        :param control: str
        :param parent_controller: str
        """

        raise NotImplementedError('abstract DCC set_parent_controller() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def distance_between_nodes(source_node=None, target_node=None):
        """
        Returns the distance between 2 given nodes
        :param str source_node: first node to start measuring distance from.
            If not given, first selected node will be used.
        :param str target_node: second node to end measuring distance to.
            If not given, second selected node will be used.
        :return: distance between 2 nodes.
        :rtype: float
        """

        raise NotImplementedError('abstract DCC distance_between_nodes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def dock_widget(widget, *args, **kwargs):
        """
        Docks given widget into current DCC UI
        :param widget: QWidget
        :param args:
        :param kwargs:
        :return:
        """

        raise NotImplementedError('abstract DCC dock_widget() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def deferred_function(fn, *args, **kwargs):
        """
        Calls given function with given arguments in a deferred way
        :param fn:
        :param args: list
        :param kwargs: dict
        """

        return fn(*args, **kwargs)

    # ================================================================================================================

    @classmethod
    def set_attribute_value(cls, node, attribute_name, attribute_value, **kwargs):
        """
        Sets attribute to given node
        :param node:
        :param attribute_name:
        :param attribute_value:
        :param kwargs:
        :return:
        """

        if type(attribute_value) is bool:
            cls.set_boolean_attribute_value(node=node, attribute_name=attribute_name, attribute_value=attribute_value)
        elif type(attribute_value) is int:
            cls.set_integer_attribute_value(
                node=node, attribute_name=attribute_name, attribute_value=attribute_value, **kwargs)
        elif type(attribute_value) is float:
            cls.set_float_attribute_value(
                node=node, attribute_name=attribute_name, attribute_value=attribute_value, **kwargs)
        elif type(attribute_value) in [str, unicode]:
            cls.set_string_attribute_value(node=node, attribute_name=attribute_name, attribute_value=attribute_value)
        elif type(attribute_value) in [list, tuple]:
            if len(attribute_value) == 3:
                cls.set_float_vector3_attribute_value(
                    node=node, attribute_name=attribute_name, attribute_value=attribute_value)
            else:
                raise NotImplementedError(
                    'Vector Type of length: {} is not supported yet!'.format(type(len(attribute_value))))
        else:
            raise NotImplementedError('Type {} is not supported yet: {}!'.format(type(attribute_value), attribute_name))

    # ================================================================================================================

    @staticmethod
    def name_is_center(side, patterns=None):
        """
        Returns whether given side is a valid center side or not
        :param side: str
        :param patterns: list<str>
        :return: bool
        """

        if not patterns:
            patterns = ['C', 'c', 'Center', 'ct', 'center', 'middle', 'm']

        if str(side) in patterns:
            return True

        return False

    @staticmethod
    def name_is_left(side, patterns=None):
        """
        Returns whether given side is a valid left side or not
        :param side: str
        :param patterns: list<str>
        :return: bool
        """

        if not patterns:
            patterns = ['L', 'l', 'Left', 'left', 'lf']

        if str(side) in patterns:
            return True

        return False

    @staticmethod
    def name_is_right(side, patterns=None):
        """
        Returns whether given side is a valid right side or not
        :param side: str
        :param patterns: list<str>
        :return: bool
        """

        if not patterns:
            patterns = ['R', 'r', 'Right', 'right', 'rt']

        if str(side) in patterns:
            return True

        return False

    @staticmethod
    def get_dockable_window_class():
        """
        Returns class that should be used to instance an ew dockable DCC window
        :return: class
        """

        try:
            from tpDcc.libs.qt.core import window
            return window.MainWindow
        except Exception:
            pass

        return None

    @staticmethod
    def get_progress_bar(**kwargs):
        """
        Returns utils class instance that will manage DCC progress bar
        :return: AbstractProgressBar
        """

        from tpDcc.abstract import progressbar

        return progressbar.AbstractProgressBar(**kwargs)

    @staticmethod
    def get_progress_bar_class():
        """
        Return class of progress bar
        :return: class
        """

        from tpDcc.abstract import progressbar

        return progressbar.AbstractProgressBar

    @staticmethod
    @decorators.abstractmethod
    def get_undo_decorator():
        """
        Returns undo decorator for current DCC
        """

        return decorators.empty_decorator
