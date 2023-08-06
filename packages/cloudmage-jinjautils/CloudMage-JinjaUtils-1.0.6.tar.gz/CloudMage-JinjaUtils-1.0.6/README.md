# CloudMage JinjaUtils Python3 Utility Package

<br/>

![CloudMage](https://cloudmage-images-public.s3.us-east-2.amazonaws.com/banners/cloudmage-nebula-glow.png)

<br/>

![PyTests](https://github.com/TheCloudMage/PyPkgs-JinjaUtils/workflows/PyTests/badge.svg)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Coverage](https://github.com/TheCloudMage/PyPkgs-JinjaUtils/workflows/Coverage/badge.svg)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![codecov](https://codecov.io/gh/TheCloudMage/PyPkgs-JinjaUtils/branch/master/graph/badge.svg)](https://codecov.io/gh/TheCloudMage/PyPkgs-JinjaUtils)

<br/><br/>

## Table of Contents

* [Description](#description)
* [Road Map](#road-map)
* [Python Version Support](#python-version-support)
* [Package Installation](#package-installation)
* [Package Dependencies](#package-dependencies)
* [JinjaUtils Class](#jinjautils-class)
  * [JinjaUtils Constructor Arguments](#jinjautils-constructor-arguments)
  * [JinjaUtils Attributes and Properties](#jinjautils-attributes-and-properties)
  * [JinjaUtils Available Methods](#jinjautils-available-methods)
  * [JinjaUtils Class Usage](#jinjautils-class-usage)
* [ChangeLog](#changelog)
* [Contacts and Contributions](#contacts-and-contributions)

<br/><br/>

## Description

This utility package was created to allow quick and easy access method to work with Jinja templates within a python environment. The package will give access to a class that can be imported and instantiated, creating a JinjaUtils instance that will allow the consumer the ability to quickly and easily set jinja options via object properties, load templates including custom templates, render those templates and write the template output to the an output directory/file with little concern around error handling and processing. A few lines of code and a provided template is all that is needed to start producing template driven file creation quickly and easily.

<br/><br/>

## Road Map

Beyond the initial capabilities of this library, new features will be evaluated and could be added with feature requests, or as additional processes that can be simplified are discovered.

<br/><br/>

## Python Version Support

This library is compatible with Python 3.6 and higher. It may work with earlier versions of Python3 but was not tested against anything earlier then 3.6. As Python 2.x is soon to be end of life, backward compatibility was not taken into consideration.

<br/><br/>

## Package Installation

This library has been published to [PyPi](https://pypi.org/project/cloudmage-jinjautils/) and can be installed via normal python package manager conventions such as [pip](https://pip.pypa.io/en/stable/) or [poetry](https://pypi.org/project/poetry/).

<br/>

```python
pip3 install cloudmage-jinjautils
```

<br/><br/>

## Package Dependencies

This package installs and imports the following python modules during installation:

* jinja2
  * Template
  * Environment
  * FileSystemLoader

<br/>

Additionally the package takes advantage of the following built in python modules:

* os
* sys
* json
* inspect
* ntpath
* shutil
* datetime

<br/><br/>

## JinjaUtils Class

The JinjaUtils class has the following described methods, properties and attributes accessable to it upon object instantiation. A few object constructor arguments can be provided at the time that the object is instantiated. Object getter property methods are accessed from the object in standard dot notation `Jinja.verbose, Jinja.template_directory, etc.` and Object settter methods are used by assigning a value to the object property `Jinja.template_directory = '/path/to/templates`. The class gives the object instance access to the following properties:

<br/>

### JinjaUtils Constructor Arguments

-----

| __[verbose]('')__ |  *Enables verbose mode. &nbsp; [[true]('')=enable &nbsp; [false]('')=disable]* |
|:------------------|:-------------------------------------------------------------------------------|
| *required*        | [false]('')                                                                    |
| *type*            | [bool](https://docs.python.org/3/library/stdtypes.html)                        |
| *default*         | [false]('') *(disabled)*                                                       |

<br/>

| __[log]('')__ |  *Redirects object standard log messaging to provided log object.* |
|:--------------|:-------------------------------------------------------------------|
| *required*    | [false]('')                                                        |
| *type*        | [obj](https://docs.python.org/3/library/stdtypes.html)             |
| *default*     | [None]('') *(log to stdout, stderr if verbose=[true](''))*         |

<br/><br/>

### JinjaUtils Attributes and Properties

-----

The following attributes/properties are available to an instantiated object instance. Any of the attributes or properties can be accessed with standard object dot notation as in the example: `verbose_mode = JinjaUtils.verbose`

<br/>

| __[verbose]('')__ |  *Verbose setting that controls logging level within the object class. &nbsp; [[true]('')=enabled, [false]('')=disabled]* |
|:---------------------|:--------------------------------------------------------|
| *returns*            | [true](true) or [false](false) *(enabled or disabled)*  |
| *type*               | [bool](https://docs.python.org/3/library/stdtypes.html) |
| *instantiated value* | [false](false)                                          |

<br/>

| __[trim_blocks]('')__|  *Enables or disables the Jinja trim_blocks setting used when loading templates by the Jinja FileSystemLoader.* |
|:---------------------|:---------------------------------------------------------------------------------------------|
| *returns*            | [true](true) or [false](false) *(enabled or disabled)*                                       |
| *type*               | [bool](https://docs.python.org/3/library/stdtypes.html)                                      |
| *instantiated value* | [true](true)                                                                                 |

<br/>

| __[lstrip_blocks]('')__ |  *Enables or disables the Jinja lstrip_blocks setting used when loading templates by the Jinja FileSystemLoader.* |
|:---------------------|:---------------------------------------------------------------------------------------------|
| *returns*            | [true](true) or [false](false) *(enabled or disabled)*                                       |
| *type*               | [bool](https://docs.python.org/3/library/stdtypes.html)                                      |
| *instantiated value* | [true](true)                                                                                 |

<br/>

| __[template_directory]('')__ | *Getter property method that returns the string value of the currently configured Jinja template directory* |
|:---------------------|:---------------------------------------------------------------------------------|
| *returns*            | Jinja template directory [->](->) `/jinja/templates`                             |
| *type*               | [str](https://docs.python.org/3/library/stdtypes.html)                           |
| *instantiated value* | [None]('')                                                                       |

<br/>

| __[available_templates]('')__ | *Returns a list of available template files that have been loaded by the Jinja FileSystemLoader located in the configured template directory that are available for use.* |
|:---------------------|:--------------------------------------------------------------------------------------------------|
| *returns*            | List of files available in the loaded template library [->](->) [`"template1.j2"`,`"template2.j2"`|
| *type*               | [list](https://docs.python.org/3/library/stdtypes.html)                                           |
| *instantiated value* | [None]('')                                                                                        |

<br/>

| __[load]('')__       |  *Returns the file name of the currently loaded Jinja template that is ready for rendering* |
|:---------------------|:-------------------------------------------------------------------------------|
| *returns*            | Loaded template name [->](->) `myFile.j2`                                      |
| *type*               | [str](https://docs.python.org/3/library/stdtypes.html)                         |
| *instantiated value* | [None]('')                                                                     |

<br/>

| __[rendered]('')__   |  *Returns the currently rendered template object, ready to be written to disk* |
|:---------------------|:-------------------------------------------------------------------------------|
| *returns*            | Rendered template object                                                       |
| *type*               | [obj](https://docs.python.org/3/library/stdtypes.html)                         |
| *instantiated value* | [None]('')                                                                     |

<br/>

| __[write]('')__      |  *Returns [true](true) or [false](false) depending on if the rendered template was successfully written to disk* |
|:---------------------|:-----------------------------------------------------------------------------------------------------------------|
| *returns*            | [true](true) or [false](false) value signaling a valid write or failed write to disk                             |
| *type*               | [bool](https://docs.python.org/3/library/stdtypes.html)                                                          |
| *instantiated value* | [true](true) or [false](false) value signaling a valid write or failed write                                     |

<br/>

| __[log]('')__  | *The class logger. Will either write directly to stdout, stderr, or to a lob object if passed into the object constructor during object instantiation* |
|:---------------------|:-------------------------------------------------------------------------------|
| *returns*            | Log Event Stream                                                               |
| *type*               | [str](https://docs.python.org/3/library/stdtypes.html)                         |
| *instantiated value* | *Logs written to stdout, stderr*                                               |

<br/><br/>

### JinjaUtils Available Methods

-----

The following methods are available to an instantiated object instance. Some of the methods are simply setter methods that run the logic required to discover and then set one of the above instance properties.

<br/><br/>

__[verbose]('')__

Setter method for `verbose` property that enables or disables verbose mode

<br/>

| parameter   | type       | required     | arg info                                                              |
|:-----------:|:----------:|:------------:|:----------------------------------------------------------------------|
| verbose     | [bool]('')  | [true](true) | *[True]('') enables verbose logging, &nbsp; [False]('') disables it* |

<br/>

__Examples:__

```python
# Getter method
verbose_setting = JinjaUtils.verbose

# Setter method
JinjaUtils.verbose = True
```

<br/><br/>

__[trim_blocks]('')__

Setter method for `trim_blocks` property that enables or disables the Jinja trim_blocks option during the construction of the Jinja Environment and template loading process via the Jinja FileSystemLoader.

<br/>

| parameter   | type       | required     | arg info                                                                         |
|:-----------:|:----------:|:------------:|:---------------------------------------------------------------------------------|
| trim_blocks | [bool]('') | [true](true) | *[True]('') enables trim_blocks logging, &nbsp; [False]('') disables the option* |

<br/>

__Examples:__

```python
# Getter method
jinja_trim_blocks_setting = JinjaUtils.trim_blocks

# Setter method
JinjaUtils.trim_blocks = True
```

<br/><br/>

__[lstrip_blocks]('')__

Setter method for `lstrip_blocks` property that enables or disables the Jinja lstrip_blocks option during the construction of the Jinja Environment and template loading process via the Jinja FileSystemLoader.

<br/>

| parameter   | type       | required     | arg info                                                                  |
|:-----------:|:----------:|:------------:|:--------------------------------------------------------------------------|
| lstrip_blocks | [bool]('') | [true](true) | *[True]('') enables lstrip_blocks logging, &nbsp; [False]('') disables the option* |

<br/>

__Examples:__

```python
# Getter method
jinja_lstrip_blocks = JinjaUtils.lstrip_blocks

# Setter method
JinjaUtils.lstrip_blocks = True
```

<br/><br/>

__[template_directory]('')__

Setter method for `template_directory` property that is used to specify the location of the Jinja template directory. When this setter method is called, a valid directory path must be provided. The directory path is checked by `os.path.exists()` and must be a valid directory location path. The method will search the directory path for any files in the given directory location and automatically instruct the Jinja FileSystemLoader to load the templates into the Environment template library where they can be called by the object consumer at any point to be loaded, rendered and written to on disk. This setter will also set the value of the `.available_templates` attribute.

<br/>

| parameter           | type       | required     | arg info                                                                  |
|:-------------------:|:----------:|:------------:|:--------------------------------------------------------------------------|
| template_directory  | [str]('')  | [true](true) | *Provided path must be a valid URL directory path.*                       |

<br/>

__Examples:__

```python
# Getter method
jinja_template_directory = JinjaUtils.template_directory

# Setter method
JinjaUtils.template_directory = '/path/to/my/template/directory'
```

<br/><br/>

__[load]('')__

Setter method for `load` property. When this method is invoked either a file path argument or template name argument must be provided. If a file name argument is given, the loader will search through the templates that are contained in the currently configured template directory and loaded into the current Jinja Environment by the `.template_directory` setter call. To view a list of the available templates a call to the `.available_templates` attribute can be made. If a file system path is provided to the loader, then the loader will search the given file path, and if a valid file is found, it will instruct the loader to load the provided file. Once a file has been loaded by the object, it is ready to be rendered with the `.render` property.

<br/>

| parameter          | type      | required      | arg info                                                                  |
|:------------------:|:----------:|:------------:|:--------------------------------------------------------------------------|
| template           | [str]('')  | [true](true) | *Template file name located in the templates directory or valid file path to template file.* |

<br/>

__Examples:__

```python
# Getter method
jinja_loaded_template = JinjaUtils.load

# Setter method
JinjaUtils.load = '/path/to/my/template/directory/template.j2'

for template in JinjaUtils.available_templates:
  print(template)

JinjaUtils.load = 'template.j2'
```

<br/><br/>

__[render]('')__

The render method takes an undermined number of keyword arguments representing the template variables and objects that will supply the values to those variables respectively when rendering the template. The keyword example formats such as `variables=dictionaryObject`, `people=["tom", "susan", tonya"]` would be mapped to the template at the time of render and made available to the template. In the given examples, the template may require a dictionary named variables that it will iterate through, or a variable named people that is an expected list that it will use to populate template sections. When the `render` method is called, Jinja will attempt to render the currently loaded template and supply any of keyword arguments that were passed as method arguments at the time that the render method was called.

<br/>

| parameter          | type      | required      | arg info                                                                  |
|:------------------:|:----------:|:------------:|:--------------------------------------------------------------------------|
| [names]('')=names, [values]('')=values, [etc]('')=4 | [**kwargs]('')  | [false](false) | *Currently loaded template will be rendered.* |

<br/>

__Examples:__

```python
print(JinjaUtils.load)  # template.j2

JinjaUtils.render(names=names, values=values, etc=4)

# This will render the currently loaded template2.j2 and pass the names, values, and etc values to it
```

<br/><br/>

__[write]('')__

Once the template has been rendered, it can be written to disk using the `write` method. The write method takes 2 required arguments consisting of the *output directory* and *output file*, along with 1 optional argument to turn file backup off. When the write method is used, it will write the currently rendered template to the output directory specified as the output file name specified. If during the write operation it discovers an existing file with the same name in the target directory, by default instead of just overwriting the file callously, the write method will take a copy of the existing file, strip off the original extention to avoid non unique file name conflicts and write the copy appending an extention in the format of `_YYYYMMDD_HMS.bak`. This timestamp formatted extention will allow easy identification of when the backup of the file was taken. The default file backup feature can be turned off by passing the `backup=False` option to the write command when called. If backup is disabled, then calling the write method will simply just overwrite any existing files in the output directory with the output filename that already exist. Provided output_directory argument value must exist and be valid directory paths, which are validated by `os.path.exists()`, and must not be the path to a file. The provided output_file argument value must be a valid file name, and will be stripped of any trailing path.

<br/>

| parameter          | type      | required        | arg info                                                                           |
|:-------------------|:---------:|:---------------:|:-----------------------------------------------------------------------------------|
| output_directory   | str       | [true](true )   | *Must be valid directory path to existing directory.*                              |
| output_file        | str       | [true](true )   | *Filename only, paths are stripped using only the file basename .*                 |
| backup             | bool      | [false](false ) | *Bool value to enable or disable existing file backups. __Default=[true](true )__* |

<br/>

__Examples:__

```python
print(str(JinjaUtils.rendered))

JinjaUtils.write(output_directory='/reports', output_file='monthly_report.yaml', backup=True)
```

<br/><br/>

__[log]('')__

Method to enable logging throughout the class. Log messages are sent to the log method providing the log message, the message type being one of `[debug, info, warning, error]`, and finally the function or method id that is automatically derived within the function or method using the python inspect module. If a log object such as a logger or an already instantiated log object instance was passed to the class constructor during the objects instantiation, then all logs will be written to the provided log object. If no log object was provided during instantiation then all `debug`, `info`, and `warning` logs will be written to stdout, while any encountered `error` log entries will be written to stderr. Note that debug or verbose mode needs to be enabled to receive the event log stream.

<br/>

| arg      | type       | required     | arg info                                          |
|:--------:|:----------:|:------------:|:--------------------------------------------------|
| log_msg  | [str]('')  | [true](true) | *The actual message being sent to the log method* |
| log_type | [str]('')  | [true](true) | *The type of message that is being sent to the log method, one of `[debug, info, warning, error]`*    |
| log_id   | [str]('')  | [true](true) | *A string value identifying the sender method or function, consisting of the method or function name* |

<br/>

__Examples:__

```python
def my_function():
  __function_id = inspect.stack()[0][3]
  JinjaUtils.log(
    f"{__function_id} called.",
    'info',
    __function_id
  )
```

<br/><br/>

### JinjaUtils Class Usage

-----

The following section will show a few examples of how the module can be used to generate documents from available templates quickly and easily.

<br/>

#### Basic Usage

```python
from cloudmage.jinjautils import JinjaUtils

# Set template directory, contains weekly_report.j2, monthly_report.j2, annual_report.j2
jinja_template_path = os.path.join(os.getcwd(), 'templates')
jinja_output_path = os.path.join(os.getcwd(), 'monthly_reports')

# Set data variable
monthly_sales = {'week_1': 15000, 'week_2': 1000, 'week_3': 2000, 'week_4': 2500}
sales_team = ['tonya', 'tom', 'billy', 'amanda']

# Instantiate JinjaUtils Object
Jinja = JinjaUtils()

# Set the template directory, this loads all templates into the Jinja Environment
# and constructs the available_templates attribute list value
Jinja.template_directory = jinja_template_path

print(Jinja.available_templates) # prints ['weekly_report.j2', 'monthly_report.j2', 'annual_report.j2']

# Load one of the available templates
Jinja.load = 'monthly_report.j2'

# Render the template
Jinja.render(pnl=monthly_sales, team=sales_team)

# Write the rendered template to disk, Backup of existing files is ENABLED by default, so turn it off
Jinja.write(output_directory=jinja_output_path, output_file='feb_sales.html', backup=False)
```

<br/><br/>

> ![CloudMage](https://cloudmage-images-public.s3.us-east-2.amazonaws.com/icons/cloudmage/32/note.png) &nbsp;&nbsp; [__Optional Verbose Class Constructor Argument:__](Note) <br/> When instantiating the class an optional `verbose` argument can be provided. The argument expects a bool value of either `True` or `False`. By default verbose is set to False. If `verbose=True` is passed during object instantiation, then debug mode is turned on allowing the class to output DEBUG, INFO, and WARNING messages to stdout, and ERROR messages to stderr.

<br/><br/>

```python
from cloudmage.jinjautils import JinjaUtils

# Instantiate JinjaUtils Object
Jinja = JinjaUtils(verbose=True)

# Load one of the available templates
Jinja.load = './templates/annual_sales.j2'

# Render the template
Jinja.render(total_sales="25,000")

# Write the rendered template to disk
Jinja.write(output_directory='.', output_file='2019-sales.yaml')

# Class DEBUG, INFO, and WARNING messages will be printed to stdout, and ERROR messages will be printed to stderr
```

<br/><br/>

> ![CloudMage](https://cloudmage-images-public.s3.us-east-2.amazonaws.com/icons/cloudmage/32/note.png) &nbsp;&nbsp; [__Optional Log Object:__](Note) <br/> When instantiating the class an optional `log` argument can also be provided. The argument expects an Logger object to be passed as an input. If passed then all DEBUG, INFO, WARNING, and ERROR messages will be printed to the standard log levels (`log.debug()`, `log.info()`, `log.warning()`, `log.error()`) and printed to the passed respective logger object method.

<br/><br/>

```python
from cloudmage.jinjautils import JinjaUtils

# Define test log class
# This is an example log object that simply appends any DEBUG, INFO and ERROR received class messages
# to the respective log level list. Normally this would be a logger or custom log object.
class Log(object):
        """Test Log Object"""

        def __init__(self):
            """Class Constructor"""
            self.debug_logs = []
            self.info_logs = []
            self.warning_logs = []
            self.error_logs = []

        def debug(self, message):
            """Log Debug Messages"""
            self.debug_logs.append(message)

        def info(self, message):
            """Log Info Messages"""
            self.info_logs.append(message)

        def warning(self, message):
            """Log Warning Messages"""
            self.warning_logs.append(message)

        def error(self, message):
            """Log Error Messages"""
            self.error_logs.append(message)

# Instantiate test log class
Logger = Log()

# Instantiate JinjaUtils Object
Jinja = JinjaUtils(verbose=True, logs=Logger)

# Disable trim_blocks, lstrip_blocks
Jinja.trim_blocks = False
Jinja.lstrip_blocks = False

# Load one of the available templates
Jinja.load = './templates/team_schedule.j2'

# Render the template
Jinja.render()

# Write the rendered template to disk
Jinja.write(output_directory='/reports', output_file='Feb_Schedule.yaml', backup=True)

for items in Logger.debug_logs:
    print(item) # Prints stored debug logs
```

<br/><br/>

## Changelog

To view the project changelog see: [ChangeLog:](CHANGELOG.md)

<br/><br/>

## ![TheCloudMage](https://cloudmage-images-public.s3.us-east-2.amazonaws.com/icons/cloudmage/32/logo.png) &nbsp;&nbsp;Contacts and Contributions

This project is owned and maintained by: [@TheCloudMage](https://github.com/TheCloudMage)

<br/>

To contribute, please:

* Fork the project
* Create a local branch
* Submit Changes
* Create A Pull Request
