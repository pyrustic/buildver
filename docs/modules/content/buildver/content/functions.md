Back to [All Modules](https://github.com/pyrustic/buildver/blob/master/docs/modules/README.md#readme)

# Module Overview

**buildver**
 
No description

> **Classes:** &nbsp; None
>
> **Functions:** &nbsp; [\_increment](#_increment) &nbsp;&nbsp; [\_reset\_to\_zero](#_reset_to_zero) &nbsp;&nbsp; [build\_project](#build_project) &nbsp;&nbsp; [get\_latest\_build](#get_latest_build) &nbsp;&nbsp; [get\_version](#get_version) &nbsp;&nbsp; [interpret\_version](#interpret_version) &nbsp;&nbsp; [set\_version](#set_version) &nbsp;&nbsp; [update\_build\_report](#update_build_report)
>
> **Constants:** &nbsp; None

# All Functions
[\_increment](#_increment) &nbsp;&nbsp; [\_reset\_to\_zero](#_reset_to_zero) &nbsp;&nbsp; [build\_project](#build_project) &nbsp;&nbsp; [get\_latest\_build](#get_latest_build) &nbsp;&nbsp; [get\_version](#get_version) &nbsp;&nbsp; [interpret\_version](#interpret_version) &nbsp;&nbsp; [set\_version](#set_version) &nbsp;&nbsp; [update\_build\_report](#update_build_report)

## \_increment
No description



**Signature:** (number)





**Return Value:** None

[Back to Top](#module-overview)


## \_reset\_to\_zero
No description



**Signature:** (target, from\_index, to\_index)





**Return Value:** None

[Back to Top](#module-overview)


## build\_project
Build the project




**Signature:** (project\_dir=None)

|Parameter|Description|
|---|---|
|project\_dir|str, project dir (default: os.getcwd) |





**Return Value:** Returns a tuple: success_boolean, error_str
    

[Back to Top](#module-overview)


## get\_latest\_build
Get basic information about the latest build




**Signature:** (project\_dir=None)

|Parameter|Description|
|---|---|
|project\_dir|str, project dir (default: os.getcwd) |





**Return Value:** Returns a tuple of strings: (version, timestamp).
Return None if there is nothing to show.

[Back to Top](#module-overview)


## get\_version
This function read the VERSION file in the project_dir project
then returns the version (str) of the project.




**Signature:** (project\_dir=None)

|Parameter|Description|
|---|---|
|project\_dir|str, path to the project_dir project (default to os.getcwd) |



|Exception|Description|
|---|---|
|error.MissingVersionFileError|raised when the VERSION file is missing |



**Return Value:** str, version extracted from $PROJECT_DIR/VERSION or None

[Back to Top](#module-overview)


## interpret\_version
This function interprets the command to set a new version.




**Signature:** (cur\_version, new\_version)

|Parameter|Description|
|---|---|
|cur\_version|str, the current version, the one to alter.|
|new\_version|str, the new version. It can be a canonical version like "0.0.1" or a version modifier like "+rev" or "pass". Use "+maj" to increment the major number of the current version, "+min" to increment the minor number of the current version, and "+rev": to increment the revision number of the current version. |





**Return Value:** The new version as it should be saved in $PROJECT_DIR/VERSION

[Back to Top](#module-overview)


## set\_version
This function edits the content of $PROJECT_DIR/VERSION




**Signature:** (version, project\_dir=None)

|Parameter|Description|
|---|---|
|version|str, the version|
|project\_dir|str, path to the project_dir project (default: os.getcwd) |



|Exception|Description|
|---|---|
|item|val |



**Return Value:** Returns False if the project_dir doesn't exist, returns True if all right

[Back to Top](#module-overview)


## update\_build\_report
Update the build_report file




**Signature:** (version, project\_dir=None)

|Parameter|Description|
|---|---|
|version|str, version at its canonical form|
|project\_dir|str, project dir (default: os.getcwd) |





**Return Value:** None

[Back to Top](#module-overview)


