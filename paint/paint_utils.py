"""
这个里面绘制的元素都是直接基于渲染坐标来绘制的，不是世界坐标
"""

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QFontMetrics, QTransform

from data_struct.number_vector import NumberVector
import traceback


class PainterUtils:
    @staticmethod
    def paint_solid_line(
        painter: QPainter,
        point1: NumberVector,
        point2: NumberVector,
        color: QColor,
        width: float,
    ):
        """
        绘制一条实线
        :param painter:
        :param point1:
        :param point2:
        :param color:
        :param width:
        :return:
        """
        pen = QPen(color, width)  # 创建QPen并设置颜色和宽度
        painter.setPen(pen)
        painter.setBrush(color)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawLine(int(point1.x), int(point1.y), int(point2.x), int(point2.y))
        painter.setPen(QColor(0, 0, 0, 0))
        painter.setBrush(QColor(0, 0, 0, 0))
        painter.setRenderHint(QPainter.Antialiasing, False)
        pass

    @staticmethod
    def paint_dashed_line(
        painter: QPainter,
        point1: NumberVector,
        point2: NumberVector,
        color: QColor,
        width: float,
        dash_length: float,
    ):
        """
        绘制一条虚线
        :param painter:
        :param point1:
        :param point2:
        :param color:
        :param width:
        :param dash_length:
        :return:
        """
        pen = QPen(color, width)  # 创建QPen并设置颜色和宽度
        pen.setStyle(Qt.PenStyle.DashLine)  # 设置线型为虚线
        pen.setDashPattern([dash_length, dash_length])  # 设置虚线长度
        painter.setPen(pen)
        painter.setBrush(color)
        painter.setRenderHint(QPainter.Antialiasing)
        dx = point2.x - point1.x
        dy = point2.y - point1.y
        length = (dx**2 + dy**2) ** 0.5
        num_dashes = int(length / dash_length)
        if num_dashes == 0:
            num_dashes = 1
        dash_pattern = [dash_length] * num_dashes
        dash_pattern.append(length - (num_dashes - 1) * dash_length)
        painter.setPen(QColor(0, 0, 0, 0))
        painter.setBrush(QColor(0, 0, 0, 0))
        painter.setRenderHint(QPainter.Antialiasing, False)
        painter.drawLine(int(point1.x), int(point1.y), int(point2.x), int(point2.y))
        pass

    @staticmethod
    def paint_rect_from_left_top(
        painter: QPainter,
        left_top: NumberVector,
        width: float,
        height: float,
        fill_color: QColor,
        stroke_color: QColor,
    ):
        """
        绘制一个矩形，左上角坐标为left_top，宽为width，高为height，填充色为fill_color，边框色为stroke_color
        :param painter:
        :param left_top:
        :param width:
        :param height:
        :param fill_color:
        :param stroke_color:
        :return:
        """

        painter.setPen(stroke_color)
        painter.setBrush(fill_color)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawRect(int(left_top.x), int(left_top.y), int(width), int(height))
        painter.setPen(QColor(0, 0, 0, 0))
        painter.setBrush(QColor(0, 0, 0, 0))
        painter.setRenderHint(QPainter.Antialiasing, False)
        pass

    @staticmethod
    def paint_word_from_left_top(
        painter: QPainter,
        left_top: NumberVector,
        text: str,
        font_size: float,
        color: QColor,
    ):
        """
        绘制一个文本，左上角坐标为left_top，文本为text，字体大小为font_size，颜色为color
        :param painter:
        :param left_top:
        :param text:
        :param font_size:
        :param color:
        :return:
        """
        # 创建QFont对象并设置字体大小
        try:
            font = QFont("Consolas")
            font.setPointSize(round(font_size))
            # 获取字体度量信息
            font_metrics = QFontMetrics(font)
            # 设置QPainter的字体和颜色
            painter.setFont(font)
            painter.setPen(color)

            # 计算字体的ascent值，即基线到顶的距离

            # transform = QTransform()
            # factor = font_size / 20
            factor = 1
            ascent = font_metrics.ascent() * factor
            # transform.translate(left_top.x, left_top.y + ascent).scale(
            #     factor, factor
            # )
            # painter.setTransform(transform)

            # painter.drawText(QPoint(0, 0), text)

            # painter.resetTransform()
            # 转换left_top为整数坐标
            left_top = left_top.integer()
            left_top = QPoint(int(left_top.x), int(left_top.y))

            # 调整y坐标，使文本的左上角对齐
            adjusted_y = left_top.y() + ascent
            left_top.setY(adjusted_y)
            # 绘制文本
            painter.drawText(left_top, text)
        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Error message: {str(e)}")
            traceback.print_exc()
        pass

    @staticmethod
    def paint_word_from_center(
        painter: QPainter,
        center: NumberVector,
        text: str,
        font_size: float,
        color: QColor,
    ):
        """
        绘制一个文本，其中心坐标为中心point，文本为text，字体大小为font_size，颜色为color
        :param painter: QPainter对象
        :param center: 文本的中心点 (NumberVector类型)
        :param text: 要绘制的文本
        :param font_size: 字体大小
        :param color: 文本颜色
        :return: None
        """
        try:
            font = QFont("Consolas")
            font.setPointSize(int(font_size))
            font_metrics = QFontMetrics(font)

            # 设置QPainter的字体和颜色
            painter.setFont(font)
            painter.setPen(color)

            # 转换center为整数坐标
            center = center.integer()
            center = QPoint(int(center.x), int(center.y))

            # 获取文本的宽度和高度
            text_width = font_metrics.width(text)
            text_height = font_metrics.height()
            ascent = font_metrics.ascent()

            # 计算文本中心点相对于左上角的位置
            left_top_x = center.x() - text_width // 2
            left_top_y = center.y() - ascent

            # 创建新的左上角坐标
            left_top = QPoint(left_top_x, left_top_y)

            # 绘制文本
            painter.drawText(left_top, text)
        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Error message: {str(e)}")
            import traceback

            traceback.print_exc()

