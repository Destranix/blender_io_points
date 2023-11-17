from bpy.props import StringProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.types import Operator
import bpy
import os
import sys

bl_info = {
    "name": "Load Points",
    "author": "Destranix",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "File > Import > .txt",
    "description": "Import Points",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export"
}

if "bpy" in locals():
    import importlib

    if "import_points" in locals():
        importlib.reload(import_points)


class ImportPoints(Operator, ImportHelper):
    """Import a points"""

    bl_idname = "import_mesh.points"
    bl_label = "Import points"

    filename_ext = ".txt"

    files: CollectionProperty(
        name="File Path",
        description="File path used for importing the Points",
        type=bpy.types.OperatorFileListElement,
    )

    directory: StringProperty()

    filter_glob: StringProperty(default="*.txt", options={"HIDDEN"})

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        from . import import_points

        paths = [os.path.join(self.directory, name.name) for name in self.files]

        if not paths:
            paths.append(self.filepath)

        import_points.import_points(context, paths)

        context.window.cursor_set("DEFAULT")

        return {"FINISHED"}

def menu_func_import(self, context):
    self.layout.operator(ImportPoints.bl_idname, text="Points (.txt)")


def register():
    #Find animall
    if bpy.app.version < (2, 80, 0):
        preferences = bpy.context.user_preferences
    else:
        preferences = bpy.context.preferences

    if(not 'animation_animall' in preferences.addons):
        raise Exception("AnimAll is required by this addon.")


    bpy.utils.register_class(ImportPoints)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportPoints)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
