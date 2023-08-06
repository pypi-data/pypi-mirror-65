<!-- VSCode Markdown Exclusions-->
<!-- markdownlint-disable MD024 Multiple Headings with the Same Content-->
# CloudMage JinjaUtils Python Utility Package Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<br\>

## [v1.0.6] - BugFix LogIds (2020-04-08) - [@TheCloudMage](https://github.com/TheCloudMage)

-----

### Changed

- Function self.__id to __id, self. variables were being reset by other methods.

<br\><br\>

## [v1.0.5] - BugFix Patch (2020-03-31) - [@TheCloudMage](https://github.com/TheCloudMage)

-----

### Added:

- Added Verbose Getter and Setter methods.

<br\>

### Changed

- Fixed test for render exception to catch proper line number.
- Fixed image location pointed to public S3 bucket servered images.
- Added Function documentation.

<br\><br\>

## [v1.0.4] - Pep8 (2020-02-18) - [@TheCloudMage](https://github.com/TheCloudMage)

-----

### Added:

- Check for backup value type in write method, if not bool, set to default true.
- Test added to test for bad backup value in write method.
- Test added to test for bad values for verbose and log in init constructor
- Added test to validate exception behavior in render method if expected variable is not defined.
- Additional check added to write method, to abort write attempt if no rendered template is available.

<br\>

### Removed

- Internal _loaded_template_filename attribute, replaced with _loaded_template.name

<br\>

### Changed

- Class and Tests converted to pep8 standard with lines broken at the col 79 mark.
- Tests better divided out to test for single scenario instead of multiple scenarios

<br\><br\>

## [v1.0.0] - Initial Publish (2020-02-15) - [@TheCloudMage](https://github.com/TheCloudMage)

-----

### Added:

- Internal, External Logging method
- Verbose Getter/Setter property methods
- Trim Blocks Getter/Setter property methods
- Lstrip Blocks Getter/Setter property methods
- Template Directory Getter/Setter property methods
- Available Templates property method
- Load Template Getter/Setter method
- Render method
- Rendered property method
- write method
- Unit Tests written with 100% code coverage, functional and chaos testing
- Documentation of Readme File
- Github Actions Push/PR Unit Testing and Coverage Reporting Actions added
- V1 Release cut, and published to PyPi.
