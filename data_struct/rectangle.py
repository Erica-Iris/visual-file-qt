from typing import Any

from data_struct.number_vector import NumberVector


class Rectangle:
    def __init__(self, location_left_top: NumberVector, width: float, height: float):
        self.location_left_top = location_left_top
        self.width: float = width
        self.height: float = height

    def output_data(self) -> dict[str, Any]:
        return {
            "width": self.width,
            "height": self.height,
            "locationLeftTop": [self.location_left_top.x, self.location_left_top.y],
        }

    def read_data(self, data: dict[str, Any]):
        if "width" not in data or "height" not in data or "locationLeftTop" not in data:
            raise ValueError("bodyShape 更新失败，缺少必要参数")
        self.width = data["width"]
        self.height = data["height"]
        self.location_left_top = NumberVector(
            data["locationLeftTop"][0], data["locationLeftTop"][1]
        )

    def __contains__(self, item: NumberVector) -> bool:
        return (
            self.location_left_top.x <= item.x <= self.location_left_top.x + self.width
        ) and (
            self.location_left_top.y <= item.y <= self.location_left_top.y + self.height
        )

    def clone(self) -> "Rectangle":
        return Rectangle(self.location_left_top.clone(), self.width, self.height)

    def right(self):
        """返回最右侧的x坐标

        Returns:
            float: 最右侧x坐标
        """
        return self.location_left_top.x + self.width

    def left(self):
        return self.location_left_top.x

    def top(self):
        return self.location_left_top.y

    def bottom(self):
        return self.location_left_top.y + self.height

    @staticmethod
    def from_edges(left: float, top: float, right: float, bottom: float) -> "Rectangle":
        """通过四条边来创建矩形"""
        return Rectangle(NumberVector(left, top), right - left, bottom - top)

    def get_fore_points(self) -> list[NumberVector]:
        return [
            NumberVector(self.location_left_top.x, self.location_left_top.y),
            NumberVector(
                self.location_left_top.x + self.width, self.location_left_top.y
            ),
            NumberVector(
                self.location_left_top.x + self.width,
                self.location_left_top.y + self.height,
            ),
            NumberVector(
                self.location_left_top.x, self.location_left_top.y + self.height
            ),
        ]

    @property
    def center(self) -> NumberVector:
        return NumberVector(
            self.location_left_top.x + self.width / 2,
            self.location_left_top.y + self.height / 2,
        )

    def is_collision(self, rect: "Rectangle", margin: float = 0) -> bool:
        """判断self是否与rect之间的最小边距小于margin。
        当margin=0时，此时为判断self与rect是否重叠

        Args:
            rect (Rectangle): 待判断的矩形
            margin (float, optional): 判断的边距，当边距等于0时，为碰撞检测. Defaults to 0.

        Returns:
            bool: self是否与rect之间的最小边距小于margin
        """
        collision_x = (
            self.right() - rect.left() > -margin
            and rect.right() - self.left() > -margin
        )
        collision_y = (
            self.bottom() - rect.top() > -margin
            and rect.bottom() - self.top() > -margin
        )
        return collision_x and collision_y

    def is_contain(self, rect: "Rectangle") -> bool:
        """判断是否包含另一个矩形，另一个矩形是否被套在自己内部"""
        return (
            self.left() <= rect.left()
            and self.right() >= rect.right()
            and self.top() <= rect.top()
            and self.bottom() >= rect.bottom()
        )

    def is_contain_point(self, point: NumberVector) -> bool:
        """判断是否包含点"""
        return (
            self.left() <= point.x <= self.right()
            and self.top() <= point.y <= self.bottom()
        )

    def __repr__(self):
        return f"Rectangle({self.location_left_top}, {self.width}, {self.height})"


# test
if __name__ == "__main__":
    r1 = Rectangle(NumberVector(0, 0), 10, 10)
    r2 = Rectangle(NumberVector(5, 5), 10, 10)
    print(r1.is_collision(r2))  # True
    print(r2.is_collision(r1))  # True
    print(r1.center)  # (5, 5)
