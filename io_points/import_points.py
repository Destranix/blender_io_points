""" This script is an importer for the points"""

import enum
import os
import struct
import sys
import time

import bpy
from bpy.app.translations import (pgettext_data as data_)

class Points:
    def __init__(self, frame, attributes):
        self.frame = frame;
        self.attributes = attributes;
        self.length = len(attributes[0].values);
        
    def __len__(self):
        return self.length;
    
class ValueAttribute:
    type_name = "VALUE"
    def __init__(self, attribute_str):
        self.name = attribute_str[1];
        self.values = [float(x) for x in attribute_str[2:]];
        
class IntAttribute:
    type_name = "INT"
    def __init__(self, attribute_str):
        self.name = attribute_str[1];
        self.values = [int(x) for x in attribute_str[2:]];

class BooleanAttribute:
    type_name = "BOOLEAN"
    def __init__(self, attribute_str):
        self.name = attribute_str[1];
        self.values = [bool(x) for x in attribute_str[2:]];

class VectorAttribute:
    type_name = "VECTOR"
    def __init__(self, attribute_str):
        self.name = attribute_str[1];
        self.stride = int(attribute_str[2]);
        self.element_type = parse_type(attribute_str[3]);
        splited = attribute_str[4:];
        self.values = [tuple([self.element_type((attribute_str[3], "", x)).values[0] for x in splited[n:n+self.stride]]) for n in range(0, len(splited), self.stride)];

class StringAttribute:
    type_name = "STRING"
    def __init__(self, attribute_str):
        self.name = attribute_str[1];
        self.values = attribute_str[2:];

class RGBAAttribute:
    type_name = "RGBA"
    def __init__(self, attribute_str):
        self.name = attribute_str[1];
        self.stride = 4;
        self.element_type = ValueAttribute;
        splited = attribute_str[2:];
        self.values = [tuple([self.element_type((attribute_str[3], "", x)).values[0] for x in splited[n:n+self.stride]]) for n in range(0, len(splited), self.stride)];

class ShaderAttribute:
    def __init__(self, attribute_str):
       raise Exception("NotImplementedException")

class ObjectAttribute:
    def __init__(self, attribute_str):
       raise Exception("NotImplementedException")

class ImageAttribute:
    def __init__(self, attribute_str):
       raise Exception("NotImplementedException")

class GeometryAttribute:
    def __init__(self, attribute_str):
        raise Exception("NotImplementedException")

class CollectionAttribute:
    def __init__(self, attribute_str):
        raise Exception("NotImplementedException")

class TextureAttribute:
    def __init__(self, attribute_str):
        raise Exception("NotImplementedException")

class MaterialAttribute:
    def __init__(self, attribute_str):
        raise Exception("NotImplementedException")
        

def parse_type(type):
    if type == 'VALUE':
        return ValueAttribute;
    elif type == 'INT':
        return IntAttribute;
    elif type == 'BOOLEAN':
        return BooleanAttribute;
    elif type == 'VECTOR':
        return VectorAttribute;
    elif type == 'STRING':
        return StringAttribute;
    elif type == 'RGBA':
        return RGBAAttribute;
    elif type == 'SHADER':
        return ShaderAttribute;
    elif type == 'OBJECT':
        return ObjectAttribute;
    elif type == 'IMAGE':
        return ImageAttribute;
    elif type == 'GEOMETRY':
        return GeometryAttribute;
    elif type == 'COLLECTION':
       return CollectionAttribute;
    elif type == 'TEXTURE':
        return TextureAttribute;
    elif type == 'MATERIAL':
       return MaterialAttribute;
    else:
       return StringAttribute;
       
def get_mesh_attribute_type(attribute):
    if attribute.type_name == 'VALUE':
        return 'FLOAT';
    elif attribute.type_name == 'INT':
        return 'INT';
    elif attribute.type_name == 'BOOLEAN':
        return 'BOOLEAN';
    elif attribute.type_name == 'VECTOR':
        if attribute.element_type.type_name == 'VALUE':
            return 'FLOAT_VECTOR';
        else:
            raise Exception("NotImplementedException")
    elif attribute.type_name == 'STRING':
        return 'STRING';
    elif attribute.type_name == 'RGBA':
        return 'FLOAT_COLOR';
    elif attribute.type_name == 'SHADER':
        raise Exception("NotImplementedException")
    elif attribute.type_name == 'OBJECT':
        raise Exception("NotImplementedException")
    elif attribute.type_name == 'IMAGE':
        raise Exception("NotImplementedException")
    elif attribute.type_name == 'GEOMETRY':
        raise Exception("NotImplementedException")
    elif attribute.type_name == 'COLLECTION':
        raise Exception("NotImplementedException")
    elif attribute.type_name == 'TEXTURE':
        raise Exception("NotImplementedException")
    elif attribute.type_name == 'MATERIAL':
        raise Exception("NotImplementedException")
    else:
       return 'STRING';
       
def get_mesh_attribute_access_name(attribute):
    if attribute.data_type == 'FLOAT':
        return 'value';
    elif attribute.data_type == 'INT':
        return 'value';
    elif attribute.data_type == 'FLOAT_VECTOR':
        return 'vector';
    elif attribute.data_type == 'FLOAT_COLOR':
        return 'color';
    elif attribute.data_type == 'BYTE_COLOR':
        return 'color';
    elif attribute.data_type == 'STRING':
        return 'value';
    elif attribute.data_type == 'BOOLEAN':
        return 'value';
    elif attribute.data_type == 'FLOAT2':
        return 'vector';
    elif attribute.data_type == 'INT8':
        return 'value';
    elif attribute.data_type == 'INT32_2D':
        return 'value';
    elif attribute.data_type == 'QUATERNION':
        return 'value';
    else:
        raise Exception("NotImplementedException")

def parse_attribute(attribute_str):
    attribute_type = attribute_str[0];
    attribute_type_class = parse_type(attribute_type);
    return attribute_type_class(attribute_str);

def parse_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        frame_str = file.readline();
        frame = int(frame_str.rstrip());
        attributes = [];
        while line := file.readline():
            attribute_str = line.rstrip();
            attribute = attribute_str.split(" ");
            attributes.append(parse_attribute(attribute));
        
        #Validate attributes
        if(len(attributes) == 0):
            raise Exception("At least one attribut mus be present.");
        
        attribute_length = len(attributes[0].values);
        for attribute in attributes:
            if(attribute_length != len(attribute.values)):
                raise Exception("All attributes must have the same length");
        
        return Points(frame, attributes)

def load_points_file(obj, path, smallest_frame, smallest_frame_point_count):
    import animation_animall as animall

    #Parse file
    points = parse_file(path);
    
    #Get hidden group
    hidden_group = obj.vertex_groups['hidden'];
    
    #Set frame
    bpy.context.scene.frame_set(points.frame);
    
    #Logging
    print("Loading frame", points.frame);
    
    #Increase point count if necessary
    if(len(points) > len(obj.data.vertices)):
        obj.data.vertices.add(len(points) - len(obj.data.vertices));
    
    if(points.frame < smallest_frame):
        smallest_frame = points.frame;
        smallest_frame_point_count = len(points);
    
    #If attribute is not yet existing, add it
    for attribute in points.attributes:
        #Position are built-in attributes
        if(attribute.name != "P"):
            if(obj.data.attributes.find(attribute.name) == -1):
                new_attribute = obj.data.attributes.new(name=attribute.name, type=get_mesh_attribute_type(attribute), domain="POINT");
    
    #Insert data for all attributes
    for idx in range(0, len(obj.data.vertices)):
        if(idx < len(points)):
            hidden_group.add([idx], 0.0, "REPLACE");
            for attribute in points.attributes:
                if(attribute.name == "P"):
                    obj.data.vertices[idx].co = attribute.values[idx];
                else:
                    setattr(obj.data.attributes[attribute.name].data[idx], get_mesh_attribute_access_name(obj.data.attributes[attribute.name]), attribute.values[idx]);
        else:
            #Hide vertices for which we don't have attributes
            hidden_group.add([idx], 1.0, "REPLACE");
    
    #Insert keyframe
    for idx in range(0, len(obj.data.vertices)):
        animall.insert_key(obj.data.vertices[idx].groups[obj.data.vertices[idx].groups.find('hidden')], 'weight', group=data_("Vertex %s") % idx);
        for attribute in points.attributes:
            if(attribute.name == "P"):
                animall.insert_key(obj.data.vertices[idx], 'co', group=data_("Vertex %s") % idx);

    for attribute in points.attributes:
        if(attribute.name != "P"):
            blender_attribute = obj.data.attributes.get(attribute.name);
            access_name = get_mesh_attribute_access_name(blender_attribute);
            if(not blender_attribute.data_type == 'STRING'):
                for idx in range(0, len(obj.data.vertices)):
                    animall.insert_key(obj.data, f'attributes["{blender_attribute.name}"].data[{idx}].{access_name}', group=data_("Vertex %s") % idx)
    
    return (smallest_frame, smallest_frame_point_count);

def add_keyframe_for_initially_hidden_points(obj, smallest_frame, smallest_frame_point_count):
    import animation_animall as animall
    
    #Get hidden group
    hidden_group = obj.vertex_groups['hidden'];
    
    #Set frame
    bpy.context.scene.frame_set(smallest_frame);
    
    for idx in range(smallest_frame_point_count, len(obj.data.vertices)):
       #Hide vertices for which we don't have attributes
       hidden_group.add([idx], 1.0, "REPLACE");
    for idx in range(smallest_frame_point_count, len(obj.data.vertices)):
      animall.insert_key(obj.data.vertices[idx].groups[obj.data.vertices[idx].groups.find('hidden')], 'weight', group=data_("Vertex %s") % idx);
    

def import_points(context, filepaths):
    import animation_animall as animall
    
    name = bpy.path.display_name_from_filepath(filepaths[0]);
    
    #Create object
    mesh = bpy.data.meshes.new(name);
    
    obj = bpy.data.objects.new(name, mesh);
    bpy.context.collection.objects.link(obj);
    bpy.context.view_layer.objects.active = obj;
    obj.select_set(True);
    
    #Hidden vertices and modifier for hiding
    obj.vertex_groups.new(name = 'hidden');
    hidden_mask_modifier = obj.modifiers.new("HiddenPointsMask", 'MASK');
    hidden_mask_modifier.invert_vertex_group = True;
    hidden_mask_modifier.vertex_group = 'hidden';
    
    mode = context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    #Load vertices
    smallest_frame = sys.maxsize;
    smallest_frame_point_count = 0;
    for filepath in filepaths:
        (smallest_frame, smallest_frame_point_count) = load_points_file(obj, filepath, smallest_frame, smallest_frame_point_count);
    
    print("TEST7")
    add_keyframe_for_initially_hidden_points(obj, smallest_frame, smallest_frame_point_count);
    
    print("Finished loading points.")
    
    bpy.ops.object.mode_set(mode=mode)
    animall.refresh_ui_keyframes()

    return {"FINISHED"};
