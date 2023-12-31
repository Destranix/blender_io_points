# blender_io_points
Addon for [Blender](https://www.blender.org/) 2.8+ to import point data in a custom point format as vertices.

(**NOTE:** I basically copied description and code from https://github.com/MarkHedleyJones/blender-pcd-io but made it use a custom format and added more features)

**NOTE:** This add-on is not yet well tested and the functionality is basic.

**NOTE:** Keyframe insertion is pretty slow unfortunatly. This heavily slows down the script.

## General

Points are imported as vertices of a newly created object. For each loaded frame a keyframe is added. Point creation/removal is handled by a vertex group and a mask modifier.

### Requirements:
* [Blenders AnimAll addon](https://projects.blender.org/blender/blender-addons/src/branch/main/animation_animall) is directly accessed for keyframe creation.

### Features:
* Import sequences.
* Import various types of attributes
* Very simple data format

## Installation
Download the latest zip archive (io_points.zip) from the [releases page](https://github.com/Destranix/blender_io_points/releases).

Open Blender and navigate to:

  Edit -> Preferences -> Add-ons -> Install

When prompted select the zip file `io_points.zip`.
Afterwards you will see a screen with a message telliing you to enable the add-on. You have to do what the message says (message knows best. Always trust message).

**NOTE:** You must enable the plugin by clicking the box (as the message says) before you can use it!

## Usage
After installing this plugin, there are two ways to import Points in a custom format.

### Import from the user interface
You can import Points from the File menu. You can select several files:

>  *File -> Import -> Points (.txt)*

## The Format

A file is structured like this:
```
[frame(int)]
<attribute>
<attribute>
<attribute>
...
```
The first line only contains the frame number. This must be a frame number valid for blender.

An attribute may look like this:
```
<attribute> =
[type(string/enum)] [name(string] ([stride(int)]) ([element_type(string/enum)]) <data>
```

All token are separated by single spaces.
The first token of each line is the type of the attribute. These types orientate on blender types.
The second token is the name of the attribute.
For some types (e.g. `VECTOR`) a stride and a element type are needed (third and forth token).

After the last token a space separated list of values is supplied, which will be parsed based on the provieded attribute parameters.

Currently supported types are:
```
VECTOR [name(string] [stride(int)] [element_type(string/enum)] <data>
INT [name(string] <data>
BOOLEAN [name(string] <data>
STRING [name(string] <data>
VALUE [name(string] <data>
```
Special attributes:
* The attribute `P` has a special meaning. It is used as position for the points. It must have the properties `VECTOR P 3 VALUE`.
* The attribute `IDX` has a special meaning. It may be used for indexing the points, allowing unsorted and sparse data storage. All indices must be non-negative. It must have the properties `INT IDX`.

  In a sequence of files it is allowed that only some have the `IDX` attribute while others have not. When not present it is assumed the points are provided in order starting with index 0.

As an example a file may look like this:
```
1
INT IDX 0 5 3 6
VECTOR P 3 VALUE 1.0 2.0 3.0 2.1 3.1 4.1 3.2 4.2 5.2 4.2 5.2 6.2
VECTOR N 3 VALUE 1.0 0.0 0.0 1.0 0.0 0.0 1.0 0.0 0.0 1.0 0.0 0.0
INT A 0 1 2 3
BOOLEAN B True True True True
STRING C A B C D
VALUE D 0.0 1.0 2.0 3.0
RGBA E 1.0 0.0 0.0 1.0 1.0 0.0 0.0 1.0 1.0 0.0 0.0 1.0 1.0 0.0 0.0 1.0
```
