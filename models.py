from dataclasses import  dataclass

@dataclass
class Point:
    x: int
    y: int
    label: str = "Точка"

if __name__ == "__main__":
    p = Point(x=1, y=3, label="A")
    print(p)