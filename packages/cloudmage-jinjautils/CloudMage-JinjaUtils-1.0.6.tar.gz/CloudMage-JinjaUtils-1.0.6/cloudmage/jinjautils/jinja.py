##############################################################################
# CloudMage : Jinja Templating Helper Class to simplify using Jinja Templates
# ============================================================================
# CloudMage Jinja Helper Object Utility/Library
#   - Find, Load, and Render Jinja Templates with Simplicity.
# Author: Richard Nason rnason@cloudmage.io
# Project Start: 2/13/2020
# License: GNU GPLv3
##############################################################################

###############
# Imports:    #
###############
# Import Pip Installed Modules:
from jinja2 import Template, Environment, FileSystemLoader

# Import Base Python Modules
from datetime import datetime
import inspect
import ntpath
import shutil
import json
import sys
import os


#####################
# Class Definition: #
#####################
class JinjaUtils(object):
    """ CloudMage Jinja Helper Class

    This class is designed to make defining, loading, and rendering Jinja
    templates easily. It provides helper methods that will allow you to
    construct a Jinja object that will make loading, rendering and writing
    templates available through the instantiated object constructed by this
    class.
    """

    def __init__(self, verbose=False, log=None):
        """ JinjaHelper Class Constructor

        Parameters:
            verbose (bool): optional [default=False]
            log     (obj):  optional [default=None]

        Attributes:
            self._verbose             (bool) : private
            self._log                 (obj)  : private
            self._log_context         (str)  : private
            self._trim_blocks         (bool) : private
            self._lstrip_blocks       (bool) : private
            self._template_directory  (str)  : private
            self._available_templates (list) : private
            self._loaded_template     (obj)  : private
            self._rendered_template   (obj)  : private
            self._jinja_loader        (obj)  : private
            self._jinja_tpl_library   (str)  : private
            self._output_directory    (str)  : private
            self._output_file         (str)  : private

        Properties:
            self.trim_blocks         (bool) : public
            self.lstrip_blocks       (bool) : public
            self.verbose             (bool) : public
            self.template_directory  (str)  : public
            self.available_templates (str)  : public
            self.load                (str)  : public
            self.rendered:           (str)  : public

        Methods:
            self._exception_handler
            self.log
            self.load
            self.render
            self.write
        """

        # Class Public Properties and Attributes ######
        # Check the passed value to ensure its a bool before assignment.
        if verbose is not None and isinstance(verbose, bool):
            self._verbose = verbose
        else:
            self._verbose = False

        # Check to ensure that the passed log object is in fact an object,
        # and has the proper attributes, if not don't assign.
        if (
            log is not None and isinstance(log, object) and
            hasattr(log, 'debug') and hasattr(log, 'info') and
            hasattr(log, 'warning') and hasattr(log, 'error')
        ):
            self._log = log
        else:
            self._log = None
        self._log_context = "CLS->JinjaUtils"

        # Class Private Properties and Attributes ######
        # Getter and Setter propert vars
        self._trim_blocks = True
        self._lstrip_blocks = True
        self._template_directory = None
        self._available_templates = []
        self._loaded_template = None
        self._rendered_template = None

        # Jinja Objects using Jinja FileSystemLoader,
        # and Jinja Environment objects.
        self._jinja_loader = None
        self._jinja_tpl_library = None
        self._output_directory = None
        self._output_file = None

    ############################################
    # Class Exception Handler:                 #
    ############################################
    def _exception_handler(self, caller_function, exception_object):
        """ Class Exception Handler

        Handle any exceptions that arise in a universal format
        for easy debuging purposes.

        Parameters:
            caller_function  (str):  required
            exception_object (obj):  required

        Returns:
            Publish properly formatted exceptions
            to log object or stdout, stderr
        """
        this_exception_msg = (
            "EXCEPTION occurred in: "
            f"{self._log_context}.{caller_function}, on line "
            f"{sys.exc_info()[2].tb_lineno}: -> {str(exception_object)}"
        )
        self.log(this_exception_msg, 'error', caller_function)

    ############################################
    # Class Logger:                            #
    ############################################
    def log(self, log_msg, log_type, log_id):
        """ Class Log Handler

        Provides the logging for this class. If the class caller instantiates
        the object with the verbose setting set to true, then the class will
        log to stdout/stderr or to a provided log object if one was passed
        during object instantiation.

        Parameters:
            log_msg  (str):  required
            log_type (str):  required
            log_id   (str):  required

        Returns:
            Log Stream
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        try:
            # Internal method variable assignments:
            this_log_msg_caller = f"{self._log_context}.{log_id}"

            # Set the log message offset based on the message type:
            # [debug=3, info=4, warning=1, error=3]
            this_log_msg_offset = 3
            if log_type.lower() == 'info':
                this_log_msg_offset = 4
            elif log_type.lower() == 'warning':
                this_log_msg_offset = 1

            # If a valid log object was passed into the class constructor,
            # publish the log to the log object:
            if self._log is not None:
                # Set the log message prefix
                this_log_message = f"{this_log_msg_caller}: -> {log_msg}"
                if log_type.lower() == 'error':
                    self._log.error(this_log_message)
                elif log_type.lower() == 'warning':
                    self._log.warning(this_log_message)
                elif log_type.lower() == 'info':
                    self._log.info(this_log_message)
                else:
                    self._log.debug(this_log_message)
            # If no valid log object was passed into the class constructor,
            # write the message to stdout, stderr:
            else:
                this_log_message = "{}    {}{}{}: -> {}".format(
                    datetime.now(),
                    log_type.upper(),
                    " " * this_log_msg_offset,
                    this_log_msg_caller,
                    log_msg
                )
                if log_type.lower() == 'error':
                    print(this_log_message, file=sys.stderr)
                else:
                    if self._verbose:
                        print(this_log_message, file=sys.stdout)
        except Exception as e:
            self._exception_handler(__id, e)

    ################################################
    # Verbose Setter / Getter Methods:             #
    ################################################
    @property
    def verbose(self):
        """ Verbose Property Getter

        Getter method for the verbose property.
        This method will return the verbose setting.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property requested.", 'info', __id)
        return self._verbose

    @verbose.setter
    def verbose(self, verbose):
        """ Verbose Property Setter

        Setter method for the verbose property.
        This method will set the verbose setting if a valid
        bool value is provided.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property update requested.", 'info', __id)

        if verbose is not None and isinstance(verbose, bool):
            self._verbose = verbose
            self.log(
                f"Updated {__id} property with value: {self._verbose}",
                'info',
                __id
            )
        else:
            self.log(
                f"{__id} property argument expected type bool "
                f"but received type: {type(verbose)}",
                'error',
                __id
            )

    ############################################
    # Jinja Option Getters and Setters:        #
    ############################################
    @property
    def trim_blocks(self):
        """ Trim Blocks Property Getter

        Getter method for Jinja trim_blocks property.
        This method returns the current trim_blocks setting value."""
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property requested.", 'info', __id)
        return self._trim_blocks

    @trim_blocks.setter
    def trim_blocks(self, trim_blocks_setting=True):
        """ Trim Blocks Property Setter

        Setter method for Jinja trim_blocks property.
        This method will only take a value of true or false
        as a valid value for the property.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property update requested.", 'info', __id)

        # if the passed value is a valid bool value then set the value.
        if (
            trim_blocks_setting is not None and
            isinstance(trim_blocks_setting, bool)
        ):
            self._trim_blocks = trim_blocks_setting
            self.log(
                "Updated {} property with value: {}".format(
                    __id,
                    self._trim_blocks
                ),
                'info',
                __id
            )
        else:
            self.log(
                "{} argument expected bool but received type: {}".format(
                    __id,
                    type(trim_blocks_setting)
                ),
                'error',
                __id
            )

    @property
    def lstrip_blocks(self):
        """ LStrip  Blocks Property Getter

        Getter method for Jinja lstrip_blocks property.
        This method returns the current lstrip_blocks setting value.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property requested.", 'info', __id)
        return self._lstrip_blocks

    @lstrip_blocks.setter
    def lstrip_blocks(self, lstrip_blocks_setting=True):
        """ LStrip Blocks Property Setter

        Setter method for Jinja lstrip_blocks property.
        This method will only take a value of true or false as a valid value
        for the lstrip_blocks property.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property update requested.", 'info', __id)

        # if the passed value is a valid bool value then set the value.
        if (
            lstrip_blocks_setting is not None and
            isinstance(lstrip_blocks_setting, bool)
        ):
            self._lstrip_blocks = lstrip_blocks_setting
            self.log(
                "Updated {} property with value: {}".format(
                    __id,
                    self._lstrip_blocks
                ),
                'info',
                __id
            )
        else:
            self.log(
                "{} argument expected bool but received type: {}".format(
                    __id,
                    type(lstrip_blocks_setting)
                ),
                'error',
                __id
            )

    ############################################
    # Jinja Template Directory Getter/Setter:  #
    ############################################
    @property
    def template_directory(self):
        """ Template Directory Property Getter

        This class Getter method will retreive the currently set value of the
        template directory and return it back to the method caller.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property requested.", 'info', __id)
        if self._template_directory is None:
            return "A template directory has not yet been configured."
        else:
            return self._template_directory

    @property
    def available_templates(self):
        """ Available Template Property Getter

        Class property method that will return the self._available_templates
        property. The available_templates property is a list of all templates
        available in the configured template_directory. The template_directory
        setter method constructs the list of template files when a
        template_directory is updated.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log("Call to retrieve available_templates", 'info', __id)
        if (
            self._available_templates is not None and
            isinstance(self._available_templates, list)
        ):
            return self._available_templates
        else:
            return []

    @template_directory.setter
    def template_directory(self, template_directory_path):
        """ Template Directory Property Setter

        Setter method that will take a valid directory path location
        and use that location to set the object template_directory property.
        Once validated this method will call the load method to load the
        template directory and populate the available_templates list property.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property update requested.", 'info', __id)

        try:
            # Set template directory
            if (
                template_directory_path is not None and
                isinstance(template_directory_path, str)
            ):
                if (
                    os.path.exists(template_directory_path) and
                    os.access(template_directory_path, os.R_OK)
                ):
                    # Set the template_directory property.
                    self._template_directory = template_directory_path
                    self.log(
                        "Template directory path set to: {}".format(
                            self._template_directory
                        ),
                        'debug',
                        __id
                    )
                    # Load the templates into Jinja
                    self._jinja_loader = FileSystemLoader(
                        self._template_directory
                    )
                    self._jinja_tpl_library = Environment(
                        loader=self._jinja_loader,
                        trim_blocks=self._trim_blocks,
                        lstrip_blocks=self._lstrip_blocks
                    )
                    self._jinja_tpl_library.filters['to_json'] = json.dumps
                    self.log(
                        "Jinja successfully loaded: {}".format(
                            self._template_directory
                        ),
                        'debug',
                        __id
                    )
                    self.log(
                        "Added to_json filter to Jinja Environment object.",
                        'debug',
                        __id
                    )
                    # Set Jinja template library
                    template_list = self._jinja_tpl_library.list_templates()

                    # Set available_templates property
                    if isinstance(template_list, list) and template_list:
                        self._available_templates = template_list
                        self.log(
                            "Updated {} property with: {}".format(
                                __id,
                                self._available_templates
                            ),
                            'debug',
                            __id
                        )
                else:
                    self.log(
                        "Provided directory path doesn't exit.",
                        'error',
                        __id
                    )
                    self.log(
                        "Aborting property update...",
                        'error',
                        __id
                    )
            else:
                self.log(
                    "Provided path expected type str but received: {}".format(
                        type(template_directory_path)
                    ),
                    'error',
                    __id
                )
                self.log("Aborting property update...", 'error', __id)
        except Exception as e:  # pragma: no cover
            self._exception_handler(__id, e)  # pragma: no cover

    ############################################
    # Jinja Template Getter/Setter:            #
    ############################################
    @property
    def load(self):
        """ Load Template Property Getter

        Getter Method that returns the value of
        self._loaded_template back to the caller
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property requested.", 'info', __id)

        # Return the loaded template name.
        if (
            self._loaded_template is not None and
            self._loaded_template.name is not None and
            isinstance(self._loaded_template.name, str)
        ):
            return str(self._loaded_template.name)
        else:
            return "No template has been loaded!"

    @load.setter
    def load(self, template):
        """ Load Template Property Setter

        Class method to load the specified template. The template can be:

        * The name of a template already loaded in the jinja_loader
          from a template_directory
        * A file path to a valid jinja file on the filesystem
        """
        # Reinitialize the loaded template
        self._loaded_template = None
        try:
            # Define this methods identity for functional logging:
            __id = inspect.stack()[0][3]
            self.log(f"{__id} property update requested.", 'info', __id)

            # Check the value passed to determine what type
            # of template was passed.
            if os.path.isfile(template) and os.access(template, os.R_OK):
                self._loaded_template = Template(open(template).read())
                self.log(
                    "Loaded template file from path: {}".format(
                        self._loaded_template
                    ),
                    'info',
                    __id
                )
                if not self._loaded_template.name:
                    self._loaded_template.name = os.path.basename(template)
                self.log(
                    "Loaded template name set to: {}".format(
                        self._loaded_template.name
                    ),
                    'debug',
                    __id
                )
            else:
                if isinstance(template, str):
                    for tpl in self._jinja_tpl_library.list_templates():
                        if template == tpl:
                            self._loaded_template = \
                                self._jinja_tpl_library.get_template(
                                    template
                                )
                            self.log(
                                "Loaded template file from: {}".format(
                                    self._loaded_template
                                ),
                                'info',
                                __id
                            )
                    if (
                        self._loaded_template is None
                    ):
                        self.log(
                            "Requested template not found in: {}".format(
                                self._template_directory
                            ),
                            'warning',
                            __id
                        )
                else:
                    self.log(
                        "{} expected str template but received: {}".format(
                            __id,
                            type(template)
                        ),
                        'error',
                        __id
                    )
        except Exception as e:
            self._exception_handler(__id, e)

    @property
    def rendered(self):
        """ Rendered Template Property Getter

        Class method that will return the currently rendered version
        of the currently loaded template.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property requested.", 'info', __id)

        # Return the rendered template value.
        if self._rendered_template is not None:
            return self._rendered_template
        else:
            return "No template has been rendered!"

    def render(self, **kwargs):
        """ Render Template Method

        Class method that will render the template loaded in the objects
        self._loaded_template property. This method will accept multiple
        dictionary objects as an input provided that they were provided
        in the format of keyword = dictionary where keyword is the variable
        in the Jinja template that will map to the dictionary object being
        passed.
        """
        # Reinitialize the rendered property
        self._rendered_template = None
        try:
            # Define this methods identity for functional logging:
            __id = inspect.stack()[0][3]
            self.log(
                "{} of loaded template requested.".format(__id),
                'info',
                __id
            )
            if (
                isinstance(self._loaded_template, Template) and
                hasattr(self._loaded_template, 'render')
            ):
                # Render the template passing in the kwargs input.
                self._rendered_template = \
                    self._loaded_template.render(**kwargs)
                self.log(
                    "{} rendered successfully!".format(
                        self._loaded_template
                    ),
                    'info',
                    __id
                )
            else:
                self.log(
                    "No template loaded, Aborting render!",
                    'error',
                    __id
                )
        except Exception as e:
            self._exception_handler(__id, e)

    def write(self, output_directory, output_file, backup=True):
        """ Write Rendered Template Method

        Class method that will write the rendered jinja template that
        is currently loaded in memory to disk in the specified
        directory/path location.
        """
        try:
            # Define this methods identity for functional logging:
            __id = inspect.stack()[0][3]
            self.log(
                "{} called on rendered template requested.".format(__id),
                'info',
                __id
            )

            # Set local method variables
            if isinstance(backup, bool):
                self.__backup = backup
            else:
                self.log(
                    "Backup expected bool value but received type: {}".format(
                        type(backup)
                    ),
                    'warning',
                    __id
                )
                self.log(
                    "Setting backup to default setting...",
                    'warning',
                    __id
                )
                self.__backup = True
            self.log(
                    "Backup setting has been set to: {}.".format(
                        self.__backup
                    ),
                    'info',
                    __id
                )

            # Set the Output Directory and perform directory validation checks
            if (
                isinstance(output_directory, str) and
                os.path.exists(output_directory) and
                not os.path.isfile(output_directory)
            ):
                self._output_directory = output_directory
                self.log(
                    "Output directory has been set to: {}!".format(
                        self._output_directory
                    ),
                    'debug',
                    __id
                )
                # Set the Output file and perform validation checks
                if isinstance(output_file, str):
                    head, tail = ntpath.split(output_file)
                    if tail or ntpath.basename(head) is not None:
                        self._output_file = tail or ntpath.basename(head)
                        self.log(
                            "Output file has been set to: {}!".format(
                                self._output_file
                            ),
                            'debug',
                            __id
                        )
                else:
                    self.log(
                        "Output expected str filename but received {}".format(
                            type(output_file)
                        ),
                        'error',
                        __id
                    )
                    return False
            else:
                self.log(
                    "Invalid output directory specified in {} call".format(
                        __id
                    ),
                    'error',
                    __id
                )
                return False

            # Check if file back up is enabled and if so backup the file.
            if os.path.exists(os.path.join(
                self._output_directory,
                self._output_file
            )):
                # If backup enabled, make a backup of the file.
                if self.__backup:
                    # Separate the filename from the file extention
                    raw_filename, raw_file_extention = os.path.splitext(
                        self._output_file
                    )
                    backup_timestamp = datetime.now().strftime(
                        "%Y%m%d_%H%M%S"
                    )
                    source_filename = os.path.join(
                        self._output_directory,
                        self._output_file
                    )
                    backup_filename = os.path.join(
                        self._output_directory,
                        "{}_{}.bak".format(
                            raw_filename, backup_timestamp
                        )
                    )
                    shutil.copy(source_filename, backup_filename)
                    self.log(
                        "{} backed up to: {}".format(
                            self._output_file,
                            backup_filename
                        ),
                        "info",
                        __id
                    )
                else:
                    self.log(
                        "File backup is disabled, overwritting: {}!".format(
                            self._output_file
                        ),
                        "warning",
                        __id
                    )
            # Write the output file.
            write_output_file = os.path.join(
                self._output_directory,
                self._output_file
            )
            self.log(
                "Writing rendered template to output file: {}".format(
                    write_output_file
                ),
                "debug",
                __id
            )
            if self.rendered == "No template has been rendered!":
                self.log(
                    "Render method not called or failed to render.",
                    'warning',
                    __id
                )
                self.log(
                    "No rendered template available for write request!",
                    'warning',
                    __id
                )
                return False
            else:
                output = open(write_output_file, "w")
                output.write(self._rendered_template)
                output.close()
                self.log(
                    "{} written successfully!".format(write_output_file),
                    "info",
                    __id
                )
                return True
        except Exception as e:  # pragma: no cover
            self._exception_handler(__id, e)  # pragma: no cover
