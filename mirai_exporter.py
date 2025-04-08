bl_info = {
    "name": "Mirai Export",
    "author": "Amadeo Delgado Casado, Long H B, Minh Nguyen",
    "version": (2, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Unified tool for exporting",
    "warning": "",
    "doc_url": "",
    "category": "Mirai Tools",
}

#Base libraries
import bpy
import os
import numpy as np

#Settings

def raycast_screenshot(self,context):
    
    bpy.context.scene.display_settings.display_device = 'sRGB'
    bpy.context.scene.view_settings.view_transform = 'Standard'
    bpy.context.scene.view_settings.look = 'Medium High Contrast'

    # Get the path where the blend file is located
    basedir = bpy.path.abspath('//')

    # Get file name:
    filename = bpy.path.basename(bpy.context.blend_data.filepath)

    # Remove .blend extension:
    filename = os.path.splitext(filename)[0]
                              
    # Set up the Raycast Screenshot conditions
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas: # iterate through areas in current screen
            if area.type == 'VIEW_3D':
                for space in area.spaces: # iterate through spaces in current VIEW_3D area
                    if space.type == 'VIEW_3D': # check if space is a 3D view
                        space.shading.type = 'SOLID'
                        space.shading.light = 'FLAT'
                        space.shading.color_type =  'TEXTURE'
                        space.overlay.show_overlays = True
                # Set overlay properties
                        space.overlay.grid_lines = 0
                        space.overlay.show_axis_x = False      
                        space.overlay.show_axis_y = False    
                        space.overlay.show_axis_z = False   
                        space.overlay.show_cursor = False
                        space.overlay.show_floor = False
                        space.overlay.show_object_origins = False
                        space.overlay.show_outline_selected = False
                        space.overlay.show_stats = False
                        space.overlay.show_statvis = False
                        space.shading.show_xray = True
                        

    # Hide the rooms

    bpy.context.view_layer.layer_collection.children["raycast"].hide_viewport = False
    bpy.context.view_layer.layer_collection.children["Collection"].hide_viewport = False  
    for collection in bpy.context.view_layer.layer_collection.children:
        if collection.name == "rooms":
            collection.hide_viewport = True

    #Set the raycast to show wireframe
    bpy.data.objects["raycast"].select_set(True)
    # to select the object in the 3D viewport,
    current_state = bpy.data.objects["raycast"].select_get()
    # retrieving the current state

    # this way you can also select multiple objects

    bpy.context.view_layer.objects.active = bpy.data.objects['raycast']
    # Show wireframe of the active object
    bpy.context.object.show_wire = True

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')  

    # Take Screenshot for Raycast
    bpy.context.scene.render.filepath = os.path.join(basedir+'Screenshot_'+filename+'_Raycast')
    bpy.ops.render.opengl(animation=False, render_keyed_only=False, sequencer=False, write_still=True, view_context=True)    
    return {'FINISHED'}

def rooms_screenshot(self,context):
    
    # Get the path where the blend file is located
    basedir = bpy.path.abspath('//')

    # Get file name:
    filename = bpy.path.basename(bpy.context.blend_data.filepath)

    # Remove .blend extension:
    filename = os.path.splitext(filename)[0]
                            
    # Set up the Rooms Screenshot conditions
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas: # iterate through areas in current screen
            if area.type == 'VIEW_3D':
                for space in area.spaces: # iterate through spaces in current VIEW_3D area
                    if space.type == 'VIEW_3D': # check if space is a 3D view
                        space.shading.type = 'SOLID'
                        space.shading.light = 'FLAT'
                        space.shading.color_type =  'TEXTURE'
                        space.shading.show_xray = False
                        space.overlay.show_overlays = True
                # Set overlay properties
                        space.overlay.grid_lines = 0
                        space.overlay.show_axis_x = False      
                        space.overlay.show_axis_y = False    
                        space.overlay.show_axis_z = False   
                        space.overlay.show_cursor = False
                        space.overlay.show_floor = False
                        space.overlay.show_object_origins = False
                        space.overlay.show_outline_selected = False
                        space.overlay.show_stats = False
                        space.overlay.show_statvis = False

   
    

    # Hide the raycast
    bpy.context.view_layer.layer_collection.children["rooms"].hide_viewport = False
    
    bpy.context.view_layer.layer_collection.children["Collection"].hide_viewport = False
    for collection in bpy.context.view_layer.layer_collection.children:
        if collection.name == "raycast" :
            collection.hide_viewport = True
            
    # Take Screenshot for Rooms
    bpy.context.scene.render.filepath = os.path.join(basedir+'Screenshot_'+filename+'_Rooms')
    bpy.ops.render.opengl(animation=False, render_keyed_only=False, sequencer=False, write_still=True, view_context=True)

    return {'FINISHED'}

def restoreView_and_save(self,context):
    # Restore Overlay
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas: # iterate through areas in current screen
            if area.type == 'VIEW_3D':
                for space in area.spaces: # iterate through spaces in current VIEW_3D area
                    if space.type == 'VIEW_3D': # check if space is a 3D view
                        space.shading.type = 'SOLID'
                        space.shading.light = 'FLAT'
                        space.shading.color_type =  'TEXTURE'
                        space.overlay.show_overlays = True
                # Set overlay properties
                        space.overlay.show_cursor = True
                        space.overlay.show_object_origins = True
                        space.overlay.show_outline_selected = True
                        space.shading.show_xray = False
                        space.overlay.show_floor = True
        
        
    # Pack all resources
    bpy.ops.file.pack_all()
                                                    #Purge Unused data blocks

    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)

    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)
            
    for block in bpy.data.curves:
        if block.users == 0:
            bpy.data.curves.remove(block)
            
    for block in bpy.data.lights:
        if block.users == 0:
            bpy.data.lights.remove(block)
            
    for block in bpy.data.cameras:
        if block.users == 0:
            bpy.data.cameras.remove(block)
    # Unhide all
    def get_outliner_area():
        if bpy.context.area.type!='OUTLINER':
            for area in bpy.context.screen.areas:
                if area.type == 'OUTLINER':
                    return area

    area = get_outliner_area()
    region = next(region for region in area.regions if region.type == "WINDOW")

    with bpy.context.temp_override(area=area, reigon=region):
        bpy.ops.outliner.unhide_all()
        
    # save blend
    bpy.ops.wm.save_mainfile()
    return {'FINISHED'}

#materials

def create_opacity_texture(image_name, width, height, edge_thickness, edge_opacity, inner_opacity, color):
    # Create a new image
    image = bpy.data.images.new(name=image_name, width=width, height=height, alpha=True)
    pixels = np.zeros((width, height, 4), dtype=np.float32)
    
    # Fill pixels based on the edge and inner areas
    for x in range(width):
        for y in range(height):
            if (x < edge_thickness or x >= width - edge_thickness or
                y < edge_thickness or y >= height - edge_thickness):
                # Edge pixels (fully opaque)
                pixels[x, y] = (*color, edge_opacity)
            else:
                # Inner pixels (semi-transparent)
                pixels[x, y] = (*color, inner_opacity)
    
    # Flatten the pixel array and assign it to the image
    image.pixels = pixels.flatten()
    image.file_format = 'PNG'
    bpy.ops.image.save_all_modified()
    return image

def create_material_with_texture():
    
    #Check if the material exists
    if "GreenEdgeMaterial" in bpy.data.materials:
        return bpy.data.materials["GreenEdgeMaterial"]
    
    # Create a new material
    material = bpy.data.materials.new(name="GreenEdgeMaterial")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Clear existing nodes
    nodes.clear()
    
    # Add Principled BSDF and Output nodes
    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    bsdf_node = nodes.new(type="ShaderNodeBsdfPrincipled")
    
    # Create the opacity texture
    color = (0.0, 1.0, 0.0)  # Green color
    opacity_texture = create_opacity_texture(
        image_name="GreenEdgeTexture",
        width=1024,
        height=1024,
        edge_thickness=10,
        edge_opacity=1.0,
        inner_opacity=0.1,
        color=color
    )
    
    # Add an Image Texture node
    texture_node = nodes.new(type="ShaderNodeTexImage")
    texture_node.image = opacity_texture
    
    # Connect nodes
    links.new(texture_node.outputs['Color'], bsdf_node.inputs['Base Color'])
    links.new(texture_node.outputs['Alpha'], bsdf_node.inputs['Alpha'])
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
    
    # Enable transparency in material settings
    material.blend_method = 'BLEND'
    material.shadow_method = 'CLIP'

    #Set viewport color
    material.diffuse_color = (1.0, 1.0, 1.0, 0.2)
 

    
    return material

def create_raycast_material():
    if "RaycastMaterial" in bpy.data.materials:
        return bpy.data.materials["RaycastMaterial"]
    
    # Create a new material
    material = bpy.data.materials.new(name="RaycastMaterial")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Clear existing nodes
    nodes.clear()
    
    # Add Principled BSDF and Output nodes
    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    bsdf_node = nodes.new(type="ShaderNodeBsdfPrincipled")
    
    # Set the base color to yellow
    bsdf_node.inputs['Base Color'].default_value = (1.0, 1.0, 0.0, 1.0)  # Yellow color
    
    # Connect nodes
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
    
    return material

def is_collection_empty(self,conetext,name):
    if name in bpy.data.collections:
        if len(bpy.data.collections[name].objects) == 0:
            return True
    return False

def check_collections(self,context):
    # Check if 'rooms' collection exists, if not create it
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas: # iterate through areas in current screen
                if area.type == 'VIEW_3D':
                    for space in area.spaces: # iterate through spaces in current VIEW_3D area
                        if space.type == 'VIEW_3D': # check if space is a 3D view
                            space.overlay.show_floor = True
                            space.overlay.show_ortho_grid = True
        #Create "rooms" Collection and assign the cube to it
        if "rooms" not in bpy.data.collections:
            
            #create cube
            bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

            obj = bpy.context.object
            material = create_material_with_texture()
            for obj in bpy.context.selected_objects:
                obj.name = "Cube"
                bpy.ops.object.mode_set(mode='OBJECT', toggle=True)
                obj.data.name = "Cube"
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.uv.reset()
                bpy.ops.object.mode_set(mode='OBJECT')
                #Adds material to the object
                if len(obj.data.materials) > 0:
                    obj.data.materials[0] = material
                else:
                    obj.data.materials.append(material)
        
            collection = bpy.data.collections.new("rooms")
            bpy.context.scene.collection.children.link(collection)
            # our created cube is the active one
            ob = bpy.context.active_object
            # Remove object from all collections not used in a scene
            bpy.ops.collection.objects_remove_all()
            # add it to our specific collection
            bpy.data.collections['rooms'].objects.link(ob)

        #Create "raycast" Collection and assign the cube to it
        if "raycast" not in bpy.data.collections:
            bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

            obj = bpy.context.object

            for obj in bpy.context.selected_objects:
                obj.name = "raycast"
            # create collection
            collection = bpy.data.collections.new("raycast")
            bpy.context.scene.collection.children.link(collection)
            # our created cube is the active one
            ob = bpy.context.active_object
            # Remove object from all collections not used in a scene
            bpy.ops.collection.objects_remove_all()
            # add it to our specific collection
            bpy.data.collections['raycast'].objects.link(ob)

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

#METHODS----------------- 

class Initial_setup(bpy.types.Operator):
    """Create initial rooms and raycast cubes"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "opr.initial_setup"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Initial Setup"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.
        check_collections(self,context)

     

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

class fix_rooms(bpy.types.Operator):
    bl_label = "Fix rooms"
    bl_idname = "opr.fix_rooms_operator"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #Reset uvs of all objetcs in rooms
        material = create_material_with_texture()
        #Sets materials
        for obj in bpy.data.collections["rooms"].objects:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.reset()
            bpy.ops.object.mode_set(mode='OBJECT')

            #Adds material to the object
            if len(obj.data.materials) > 0:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)
                
        return {'FINISHED'}         

class add_cube(bpy.types.Operator):
    bl_label = "Add cube"
    bl_idname = "opr.add_cube_operator"
    bl_options = {'REGISTER', 'UNDO'}
    
    #Adds a cube in the position 0,0,100
    def execute(self, context):
        
        #Check if the cube exists
        if "MeasureCube" in bpy.data.objects:
            #Delete the cube
            bpy.data.objects.remove(bpy.data.objects["MeasureCube"])
        
        bpy.ops.mesh.primitive_cube_add(size=2)
        cube = bpy.context.object
        cube.name = "MeasureCube"

        #Moves it to the position 0,0,100
        cube.location = (0, 0, 100)
        

        return {'FINISHED'}                                   

class export_mirai(bpy.types.Operator):
    """Checks uvs of the cubes, sets up collections and exports to MiraiTwin"""
    bl_label = "Export mirai"
    bl_idname = "opr.export_mirai_operator"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
    # Get the path where the blend file is located
        basedir = bpy.path.abspath('//')

    # Get file name:
        filename = bpy.path.basename(bpy.context.blend_data.filepath)

    # Remove .blend extension:
        filename = os.path.splitext(filename)[0]
        
                # Unhide all
        def get_outliner_area():
            if bpy.context.area.type!='OUTLINER':
                for area in bpy.context.screen.areas:
                    if area.type == 'OUTLINER':
                        return area

        area = get_outliner_area()
        region = next(region for region in area.regions if region.type == "WINDOW")

        with bpy.context.temp_override(area=area, reigon=region):
            bpy.ops.outliner.unhide_all()  
        
        #PREVIOUS COMPROBATIONS -----------------
        #Check if the collections exist
        if 'Collection' not in bpy.data.collections:
            #Create the collection
            collection = bpy.data.collections.new("Collection")
            bpy.context.scene.collection.children.link(collection)


        #If both "rooms" and "raycast" collection exist
        if 'raycast' in bpy.data.collections and 'rooms' in bpy.data.collections:
        #Check if the collections are not empty
            if is_collection_empty(self,context,'rooms'):
                self.report({'ERROR'}, "No rooms, please move the rooms to the collection 'rooms'")
            if is_collection_empty(self,context,'raycast'):
                self.report({'ERROR'}, "No raycast, please move the rooms to the collection 'raycast'")
            if is_collection_empty(self,context,'rooms') or is_collection_empty(self,context,'raycast'):
                return {'FINISHED'}
        
            #Check for raycast in rooms collection
            for obj in bpy.data.collections["rooms"].objects:
                if obj.data.name == "raycast":
                    self.report({'ERROR'}, f"""Raycast model "{obj.name}" detected in rooms, please check the collections""")
                    return {'FINISHED'}
                
            #Check raycast name
            if len(bpy.data.collections["raycast"].objects) != 1:
                self.report({'ERROR'}, "Only one raycast model allowed, please join all the objects in the collection 'raycast'")
            else:
                if bpy.data.collections["raycast"].objects[0].data.name != "raycast":
                    
                    #Version that stops
                    # self.report({'ERROR'}, "Raycast model must be named 'raycast'")
                    # return {'FINISHED'}

                    #Version that renames
                    for mesh in bpy.data.meshes:
                        if mesh.name == "raycast":
                            bpy.data.meshes.remove(mesh)

                    bpy.data.collections["raycast"].objects[0].data.name = "raycast"
                    bpy.data.collections["raycast"].objects[0].name = "raycast"

            #file save check
            file_path = bpy.path.basename(bpy.context.blend_data.filepath)
            file_name = os.path.basename(file_path)
            if file_name == "":
                self.report({'ERROR'}, "Save the file before exporting")
                return {'FINISHED'}
            else:
                #Remove the extension
                file_name = os.path.splitext(file_name)[0]

            #-END COMPROBATIONS -----------------

            #Sets materials
            material = create_material_with_texture()
            
            #Reset uvs of all objetcs in rooms
            for obj in bpy.data.objects:
                obj.select_set(False)
            def get_outliner_area():
                if bpy.context.area.type!='OUTLINER':
                    for area in bpy.context.screen.areas:
                        if area.type == 'OUTLINER':
                            return area

            area = get_outliner_area()
            region = next(region for region in area.regions if region.type == "WINDOW")

            with bpy.context.temp_override(area=area, reigon=region):
           
                for collection in bpy.data.collections:
                    bpy.context.view_layer.layer_collection.children["rooms"].hide_viewport = False
                for obj in bpy.data.collections["rooms"].objects:
                    bpy.context.view_layer.objects.active = obj
                    # destroy_measure_cube(self,context)
                    obj.name = "Cube"
                    obj.data.name = "Cube"
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.uv.reset()
                    bpy.ops.object.mode_set(mode='OBJECT')

                #Adds material to the object
                
                if len(obj.data.materials) > 0:
                    obj.data.materials[0] = material
                else:
                    obj.data.materials.append(material)
            
            #Sets raycast material
            raycast_material = create_raycast_material()

            if len(bpy.data.collections["raycast"].objects[0].data.materials ) > 0:
                    bpy.data.collections["raycast"].objects[0].data.materials[0] = raycast_material
            else:
                bpy.data.collections["raycast"].objects[0].data.materials.append(raycast_material)

            #Take screenshots
            rooms_screenshot(self,context)
            raycast_screenshot(self,context)
            restoreView_and_save(self,context)

            # #Show all collections
            for collection in bpy.data.collections:
                collection.hide_viewport = False

            #Deselect all objects
            for obj in bpy.data.objects:
                obj.select_set(False)
                # bpy.ops.object.select_all(action='DESELECT')    

            #Select raycast and rooms objects
            for obj in bpy.data.collections["rooms"].objects:
                obj.select_set(True)
            bpy.data.collections["raycast"].objects[0].select_set(True)

            bpy.ops.export_scene.gltf(  filepath=os.path.join(basedir+"u-"+bpy.context.scene.filename),
                                        check_existing=False,
                                        # export_import_convert_lighting_mode='SPEC',
                                        # gltf_export_id='', 
                                        # export_use_gltfpack=False, 
                                        # export_gltfpack_tc=True,
                                        # export_gltfpack_tq=8, 
                                        # export_gltfpack_si=1.0, 
                                        # export_gltfpack_sa=False, 
                                        # export_gltfpack_slb=False, 
                                        # export_gltfpack_vp=14, 
                                        # export_gltfpack_vt=12, 
                                        # export_gltfpack_vn=8, 
                                        # export_gltfpack_vc=8, 
                                        # export_gltfpack_vpi='Integer', 
                                        # export_gltfpack_noq=True, 
                                        export_format='GLB', 
                                        # ui_tab='GENERAL', 
                                        # export_copyright='', 
                                        export_image_format='AUTO', 
                                        export_image_add_webp=False, 
                                        export_image_webp_fallback=False, 
                                        export_texture_dir='', 
                                        export_jpeg_quality=75, 
                                        export_image_quality=75, 

                                        export_keep_originals=False, 
                                        export_texcoords=True, 
                                        export_normals=False, 
                                        export_gn_mesh=False, 

                                        export_draco_mesh_compression_enable=False, 
                                        export_draco_mesh_compression_level=6, 
                                        export_draco_position_quantization=14, 
                                        export_draco_normal_quantization=10, 
                                        export_draco_texcoord_quantization=12, 
                                        export_draco_color_quantization=10, 
                                        export_draco_generic_quantization=12, 

                                        export_tangents=False, 
                                        export_materials='NONE', 
                                        export_unused_images=False, 
                                        export_unused_textures=False, 
                                        export_vertex_color='MATERIAL', 
                                        export_all_vertex_colors=False, 
                                        export_active_vertex_color_when_no_material=True, 
                                        export_attributes=False, 
                                        use_mesh_edges=False, 
                                        use_mesh_vertices=False, 
                                        export_cameras=False, 
                                        use_selection=True, 
                                        use_visible=False, 
                                        use_renderable=False, 
                                        use_active_collection_with_nested=False, 
                                        use_active_collection=False, 
                                        use_active_scene=False, 
                                        collection='', 
                                        at_collection_center=False, 
                                        export_extras=False, 
                                        export_yup=True, 
                                        export_apply=True, 
                                        export_shared_accessors=False, 
                                        export_animations=False, 
                                        export_frame_range=False, 
                                        export_frame_step=1, 
                                        export_force_sampling=False, 
                                        export_pointer_animation=False, 
                                        export_animation_mode='ACTIONS', 
                                        export_nla_strips_merged_animation_name='Animation', 
                                        export_def_bones=False, 
                                        export_hierarchy_flatten_bones=False, 
                                        export_hierarchy_flatten_objs=False, 
                                        export_armature_object_remove=False, 
                                        export_leaf_bone=False, 
                                        export_optimize_animation_size=False, 
                                        export_optimize_animation_keep_anim_armature=False, 
                                        export_optimize_animation_keep_anim_object=False, 
                                        export_optimize_disable_viewport=False, 
                                        export_negative_frame='SLIDE', 
                                        export_anim_slide_to_zero=False, 
                                        export_bake_animation=False, 
                                        export_anim_single_armature=False, 
                                        export_reset_pose_bones=False, 
                                        export_current_frame=False, 
                                        export_rest_position_armature=False, 
                                        export_anim_scene_split_object=False, 
                                        export_skins=False, 
                                        export_influence_nb=4, 
                                        export_all_influences=False, 
                                        export_morph=False, 
                                        export_morph_normal=False, 
                                        export_morph_tangent=False, 
                                        export_morph_animation=False, 
                                        export_morph_reset_sk_data=False, 
                                        export_lights=False, 
                                        export_try_sparse_sk=False, 
                                        export_try_omit_sparse_sk=False, 
                                        export_gpu_instances=False, 
                                        export_action_filter=False, 
                                        export_convert_animation_pointer=False, 
                                        export_nla_strips=False, 
                                        export_original_specular=False, 
                                        will_save_settings=False, 
                                        export_hierarchy_full_collections=False, 
                                        export_extra_animations=False, 
                                        filter_glob='*.glb',)
    
            self.report({'INFO'}, "Exported to u-" + bpy.context.scene.filename +".glb")
            return {'FINISHED'}
        else:
                    if is_collection_empty(self,context,'rooms'):
                        self.report({'ERROR'}, "No rooms, please move the rooms to the collection 'rooms'")
                    if is_collection_empty(self,context,'rooms'):
                        return {'FINISHED'}

                        #file save check
                    file_path = bpy.path.basename(bpy.context.blend_data.filepath)
                    file_name = os.path.basename(file_path)
                    if file_name == "":
                            self.report({'ERROR'}, "Save the file before exporting")
                            return {'FINISHED'}
                    else:
                            #Remove the extension
                            file_name = os.path.splitext(file_name)[0]

                        #-END COMPROBATIONS -----------------


                        
                    #Sets materials
                    material = create_material_with_texture()

                    #Reset uvs of all objetcs in rooms
                    for obj in bpy.data.objects:
                        obj.select_set(False)
                    for obj in bpy.data.collections["rooms"].objects:
                            bpy.context.view_layer.objects.active = obj
                            #destroy_measure_cube(self,context)
                            obj.name = "Cube"
                            obj.data.name = "Cube"
                            bpy.ops.object.mode_set(mode='EDIT')
                            bpy.ops.mesh.select_all(action='SELECT')
                            bpy.ops.uv.reset()
                            bpy.ops.object.mode_set(mode='OBJECT')

                            #Adds material to the object
                            
                    if len(obj.data.materials) > 0:
                                obj.data.materials[0] = material
                    else:
                                obj.data.materials.append(material)
            
                        #Take screenshots
                    rooms_screenshot(self,context)
                    restoreView_and_save(self,context)

                        # #Show all collections
                    for collection in bpy.data.collections:
                            collection.hide_viewport = False

                        #Deselect all objects
                    for obj in bpy.data.objects:
                            obj.select_set(False)
                            # bpy.ops.object.select_all(action='DESELECT')    

                        #Select rooms objects
                    for obj in bpy.data.collections["rooms"].objects:
                            obj.select_set(True)

                    bpy.ops.export_scene.gltf(  filepath=os.path.join(basedir+"u-"+bpy.context.scene.filename),
                                                    check_existing=False,
                                                    # export_import_convert_lighting_mode='SPEC',
                                                    # gltf_export_id='', 
                                                    # export_use_gltfpack=False, 
                                                    # export_gltfpack_tc=True,
                                                    # export_gltfpack_tq=8, 
                                                    # export_gltfpack_si=1.0, 
                                                    # export_gltfpack_sa=False, 
                                                    # export_gltfpack_slb=False, 
                                                    # export_gltfpack_vp=14, 
                                                    # export_gltfpack_vt=12, 
                                                    # export_gltfpack_vn=8, 
                                                    # export_gltfpack_vc=8, 
                                                    # export_gltfpack_vpi='Integer', 
                                                    # export_gltfpack_noq=True, 
                                                    export_format='GLB', 
                                                    # ui_tab='GENERAL', 
                                                    # export_copyright='', 
                                                    export_image_format='AUTO', 
                                                    export_image_add_webp=False, 
                                                    export_image_webp_fallback=False, 
                                                    export_texture_dir='', 
                                                    export_jpeg_quality=75, 
                                                    export_image_quality=75, 

                                                    export_keep_originals=False, 
                                                    export_texcoords=True, 
                                                    export_normals=False, 
                                                    export_gn_mesh=False, 

                                                    export_draco_mesh_compression_enable=False, 
                                                    export_draco_mesh_compression_level=6, 
                                                    export_draco_position_quantization=14, 
                                                    export_draco_normal_quantization=10, 
                                                    export_draco_texcoord_quantization=12, 
                                                    export_draco_color_quantization=10, 
                                                    export_draco_generic_quantization=12, 

                                                    export_tangents=False, 
                                                    export_materials='NONE', 
                                                    export_unused_images=False, 
                                                    export_unused_textures=False, 
                                                    export_vertex_color='MATERIAL', 
                                                    export_all_vertex_colors=False, 
                                                    export_active_vertex_color_when_no_material=True, 
                                                    export_attributes=False, 
                                                    use_mesh_edges=False, 
                                                    use_mesh_vertices=False, 
                                                    export_cameras=False, 
                                                    use_selection=True, 
                                                    use_visible=False, 
                                                    use_renderable=False, 
                                                    use_active_collection_with_nested=False, 
                                                    use_active_collection=False, 
                                                    use_active_scene=False, 
                                                    collection='', 
                                                    at_collection_center=False, 
                                                    export_extras=False, 
                                                    export_yup=True, 
                                                    export_apply=True, 
                                                    export_shared_accessors=False, 
                                                    export_animations=False, 
                                                    export_frame_range=False, 
                                                    export_frame_step=1, 
                                                    export_force_sampling=False, 
                                                    export_pointer_animation=False, 
                                                    export_animation_mode='ACTIONS', 
                                                    export_nla_strips_merged_animation_name='Animation', 
                                                    export_def_bones=False, 
                                                    export_hierarchy_flatten_bones=False, 
                                                    export_hierarchy_flatten_objs=False, 
                                                    export_armature_object_remove=False, 
                                                    export_leaf_bone=False, 
                                                    export_optimize_animation_size=False, 
                                                    export_optimize_animation_keep_anim_armature=False, 
                                                    export_optimize_animation_keep_anim_object=False, 
                                                    export_optimize_disable_viewport=False, 
                                                    export_negative_frame='SLIDE', 
                                                    export_anim_slide_to_zero=False, 
                                                    export_bake_animation=False, 
                                                    export_anim_single_armature=False, 
                                                    export_reset_pose_bones=False, 
                                                    export_current_frame=False, 
                                                    export_rest_position_armature=False, 
                                                    export_anim_scene_split_object=False, 
                                                    export_skins=False, 
                                                    export_influence_nb=4, 
                                                    export_all_influences=False, 
                                                    export_morph=False, 
                                                    export_morph_normal=False, 
                                                    export_morph_tangent=False, 
                                                    export_morph_animation=False, 
                                                    export_morph_reset_sk_data=False, 
                                                    export_lights=False, 
                                                    export_try_sparse_sk=False, 
                                                    export_try_omit_sparse_sk=False, 
                                                    export_gpu_instances=False, 
                                                    export_action_filter=False, 
                                                    export_convert_animation_pointer=False, 
                                                    export_nla_strips=False, 
                                                    export_original_specular=False, 
                                                    will_save_settings=False, 
                                                    export_hierarchy_full_collections=False, 
                                                    export_extra_animations=False, 
                                                    filter_glob='*.glb',)
                        
                    self.report({'INFO'}, "Exported to u-" + bpy.context.scene.filename +".glb")
                    return {'FINISHED'}
    
PROPS = [
    ("filename", bpy.props.StringProperty(name='',default="",description="HOTEL ID",maxlen=1024)),
]

#PANEL-----------------
class OBJECT_PT_exporterMirai(bpy.types.Panel):
    """Exporter for Mirai"""
    bl_label = "Export"
    bl_idname = "OBJECT_PT_miraipanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Mirai Tools'
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="General")
        boxSetup = layout.box()
        col3 = boxSetup.column()
        row = col3.row()
        row.operator('opr.initial_setup', text='Initial setup')
        row = col3.row()
        row.operator('opr.fix_rooms_operator', text='UV reset rooms')
        row = col3.row()
        row.prop(context.scene, "filename")
        row = col3.row()
        row.operator('opr.export_mirai_operator', text='Export') 

#METHODS----------------- 

#Register the properties
CLASSES = [OBJECT_PT_exporterMirai,export_mirai,fix_rooms,add_cube,Initial_setup]

def register():

    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)

    for klass in CLASSES:
        bpy.utils.register_class(klass)


def unregister():

    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    for klass in CLASSES:
        bpy.utils.unregister_class(klass)

    
if __name__ == "__main__":
    register()
    
