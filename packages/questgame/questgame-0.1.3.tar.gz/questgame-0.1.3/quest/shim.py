# Really horrible stuff in here. Don't look.
# Based on arcade v2.3.8

import os
from arcade import SpriteList
import pytiled_parser
from arcade.tilemap import (
    get_tilemap_layer,
    _get_tile_by_gid,
    _get_image_source,
    _get_image_info_from_tileset,
)

def process_layer(sprite_class, map_object, layer_name, scaling=1, base_directory=""):
    if len(base_directory) > 0 and not base_directory.endswith("/"):
        base_directory += "/"
    layer = get_tilemap_layer(map_object, layer_name)
    if layer is None:
        print(f"Warning, no layer named '{layer_name}'.")
        return SpriteList()
    if isinstance(layer, pytiled_parser.objects.TileLayer):
        return _process_tile_layer(sprite_class, map_object, layer, scaling, base_directory)
    elif isinstance(layer, pytiled_parser.objects.ObjectLayer):
        raise NotImplementedError("This shim does not include _process_object_layer")
    print(f"Warning, layer '{layer_name}' has unexpected type. '{type(layer)}'")
    return SpriteList()

def _process_tile_layer(sprite_class, map_object, layer, scaling=1, base_directory=""):
    sprite_list = SpriteList()
    map_array = layer.data
    for row_index, row in enumerate(map_array):
        for column_index, item in enumerate(row):
            if item == 0:
                continue
            tile = _get_tile_by_gid(map_object, item)
            if tile is None:
                print(f"Warning, couldn't find tile for item {item} in layer "
                      f"'{layer.name}' in file '{map_object.tmx_file}'.")
                continue
            my_sprite = _create_sprite_from_tile(sprite_class, map_object, tile, scaling=scaling,
                                                 base_directory=base_directory)
            if my_sprite is None:
                print(f"Warning: Could not create sprite number {item} in layer '{layer.name}' {tile.image.source}")
            else:
                my_sprite.center_x = column_index * (map_object.tile_size[0] * scaling) + my_sprite.width / 2
                my_sprite.center_y = (map_object.map_size.height - row_index - 1) \
                    * (map_object.tile_size[1] * scaling) + my_sprite.height / 2
                sprite_list.append(my_sprite)
    return sprite_list

def _create_sprite_from_tile(sprite_class, map_object, tile, scaling=1.0, base_directory=None):
    map_source = map_object.tmx_file
    map_directory = os.path.dirname(map_source)
    image_file = _get_image_source(tile, base_directory, map_directory)

    if tile.animation:
        raise NotImplementedError("Quest does not support animated tiles")
    else:
        image_x, image_y, width, height = _get_image_info_from_tileset(tile)

        my_sprite = sprite_class(image_file,
                           scaling,
                           image_x,
                           image_y,
                           width,
                           height)
        # Added by CP
        x1, y1 = - my_sprite._width / 2, - my_sprite._height / 2
        x2, y2 = + my_sprite._width / 2, - my_sprite._height / 2
        x3, y3 = + my_sprite._width / 2, + my_sprite._height / 2
        x4, y4 = - my_sprite._width / 2, + my_sprite._height / 2
        my_sprite._points = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]

    if tile.properties is not None and len(tile.properties) > 0:
        for my_property in tile.properties:
            my_sprite.properties[my_property.name] = my_property.value

    if tile.objectgroup is not None:

        if len(tile.objectgroup) > 1:
            print(f"Warning, only one hit box supported for tile with image {tile.image.source}.")

        for hitbox in tile.objectgroup:
            points: List[Point] = []
            if isinstance(hitbox, pytiled_parser.objects.RectangleObject):
                if hitbox.size is None:
                    print(f"Warning: Rectangle hitbox created for without a "
                          f"height or width for {tile.image.source}. Ignoring.")
                    continue

                sx = hitbox.location[0] - (my_sprite.width / (scaling * 2))
                sy = -(hitbox.location[1] - (my_sprite.height / (scaling * 2)))
                ex = (hitbox.location[0] + hitbox.size[0]) - (my_sprite.width / (scaling * 2))
                ey = -((hitbox.location[1] + hitbox.size[1]) - (my_sprite.height / (scaling * 2)))

                p1 = [sx, sy]
                p2 = [ex, sy]
                p3 = [ex, ey]
                p4 = [sx, ey]
                points = [p1, p2, p3, p4]

            elif isinstance(hitbox, pytiled_parser.objects.PolygonObject) \
                    or isinstance(hitbox, pytiled_parser.objects.PolylineObject):
                for point in hitbox.points:
                    adj_x = point[0] + hitbox.location[0] - my_sprite.width / (scaling * 2)
                    adj_y = -(point[1] + hitbox.location[1] - my_sprite.height / (scaling * 2))
                    adj_point = [adj_x, adj_y]
                    points.append(adj_point)

                if points[0][0] == points[-1][0] and points[0][1] == points[-1][1]:
                    points.pop()

            elif isinstance(hitbox, pytiled_parser.objects.ElipseObject):
                if hitbox.size is None:
                    print(f"Warning: Ellipse hitbox created for without a height "
                          f"or width for {tile.image.source}. Ignoring.")
                    continue

                hw = hitbox.size[0] / 2
                hh = hitbox.size[1] / 2
                cx = hitbox.location[0] + hw
                cy = hitbox.location[1] + hh

                acx = cx - (my_sprite.width / (scaling * 2))
                acy = cy - (my_sprite.height / (scaling * 2))
                total_steps = 8
                angles = [step / total_steps * 2 * math.pi for step in range(total_steps)]
                for angle in angles:
                    x = (hw * math.cos(angle) + acx)
                    y = (-(hh * math.sin(angle) + acy))
                    point = [x, y]
                    points.append(point)
            else:
                print(f"Warning: Hitbox type {type(hitbox)} not supported.")

            my_sprite.points = points

    return my_sprite
