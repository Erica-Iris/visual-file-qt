from PyQt5.QtGui import QPainter, QColor

from camera import Camera
from data_struct.number_vector import NumberVector
from data_struct.rectangle import Rectangle
from entity.entity_file import EntityFile
from entity.entity_folder import EntityFolder
from paint.paint_utils import PainterUtils


def paint_grid(paint: QPainter, camera: Camera):
    try:
        line_color = QColor(255, 255, 255, 100)
        line_color_light = QColor(255, 255, 255, 255)

        for y in range(-1000, 1000, 100):
            PainterUtils.paint_solid_line(
                paint,
                camera.location_world2view(NumberVector(-1000, y)),
                camera.location_world2view(NumberVector(1000, y)),
                line_color_light if y == 0 else line_color,
                1 * camera.current_scale
            )
        for x in range(-1000, 1000, 100):
            PainterUtils.paint_solid_line(
                paint,
                camera.location_world2view(NumberVector(x, -1000)),
                camera.location_world2view(NumberVector(x, 1000)),
                line_color_light if x == 0 else line_color,
                1 * camera.current_scale
            )
    except Exception as e:
        print(e)


def paint_details_data(paint: QPainter, camera: Camera):
    """
    左上角绘制细节信息
    :param paint:
    :param camera:
    :return:
    """
    PainterUtils.paint_word_from_left_top(
        paint,
        NumberVector(0, 10),  # 左上角坐标
        f"camera scale: {camera.current_scale:.2f}",
        12,
        QColor(255, 255, 255, 100),
    )
    pass


def paint_rect_in_world(paint: QPainter,
                        camera: Camera,
                        rect: Rectangle,
                        fill_color: QColor,
                        stroke_color: QColor
                        ):
    PainterUtils.paint_rect_from_left_top(
        paint,
        camera.location_world2view(rect.location_left_top),
        rect.width * camera.current_scale,
        rect.height * camera.current_scale,
        fill_color,
        stroke_color
    )


def paint_file_rect(paint: QPainter, camera: Camera, entity_file: EntityFile):
    # 先画一个框
    PainterUtils.paint_rect_from_left_top(
        paint,
        camera.location_world2view(entity_file.body_shape.location_left_top),
        entity_file.body_shape.width * camera.current_scale,
        entity_file.body_shape.height * camera.current_scale,
        QColor(0, 0, 0, 255),
        QColor(255, 255, 255, 255)
    )
    # camera scale < 0.05 的时候不渲染文字了，会导致文字突然变大，重叠一大堆
    if camera.current_scale < 0.05:
        return
    # 再画文字
    PainterUtils.paint_word_from_left_top(
        paint,
        camera.location_world2view(entity_file.body_shape.location_left_top),
        entity_file.file_name,
        16 * camera.current_scale,
        QColor(255, 255, 255, 255),
    )

    pass


def paint_folder_rect(paint: QPainter, camera: Camera, entity_file: EntityFolder):
    """

    :param paint:
    :param camera:
    :param entity_file:
    :return:
    """
    # 先画一个框
    PainterUtils.paint_rect_from_left_top(
        paint,
        camera.location_world2view(entity_file.body_shape.location_left_top),
        entity_file.body_shape.width * camera.current_scale,
        entity_file.body_shape.height * camera.current_scale,
        QColor(255, 255, 255, 0),
        QColor(255, 255, 255, 255)
    )
    if camera.current_scale < 0.05:
        return
    # 再画文字
    PainterUtils.paint_word_from_left_top(
        paint,
        camera.location_world2view(entity_file.body_shape.location_left_top),
        entity_file.folder_name,
        16 * camera.current_scale,
        QColor(255, 255, 255, 255),
    )
