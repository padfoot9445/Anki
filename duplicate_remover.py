import csv
from enum import Enum
from typing import Any, Final, cast
from py_linq import Enumerable # type: ignore
import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument("src_file", action="store")
parser.add_argument("dst_file", action="store")
parser.add_argument("-tags-col", action="store", type=int, default=9)
parser.add_argument("-front-col", action="store", type=int, default=4)
parser.add_argument("-back-col", action="store", type=int, default=5)
parser.add_argument("-guid-col", action="store", type=int, default=1)
arguments = parser.parse_args(sys.argv[1:])
class IDX:
    def __init__(self, value):
        self.value: Final[int] = value
    TAGS: "IDX" = cast("IDX", None)
    FRONT: "IDX" = cast("IDX", None)
    BACK: "IDX" = cast("IDX", None)
    GUID: "IDX" = cast("IDX", None)

IDX.TAGS = IDX(arguments.tags_col - 1)
IDX.FRONT = IDX(arguments.front_col - 1)
IDX.BACK = IDX(arguments.back_col - 1)
IDX.GUID = IDX(arguments.guid_col - 1)

class Tags(Enum):
    Review1 = "Duplicate-Handling::review-1"
    Review2 = "Duplicate-Handling::review-2"
    ReviewBoth = "Duplicate-Handling::Review-Both"

def get_tags(tag_str: str) -> list[str]:
    return tag_str.split(" ")

def reviews(y: list[str]) -> int:
    tags = get_tags(y[IDX.TAGS.value])
    return (Tags.Review1.value in tags) + (Tags.Review2.value in tags)
def replace_field(idx: IDX, note: list[str], new_value: str) -> list[str]:
    x = list(note)
    x[idx.value] = new_value
    return x

with open(arguments.src_file, "r", encoding="UTF8") as file:
    __CONTENTS = file.readlines()
    HEADER = __CONTENTS[:6]
    __NOTES = __CONTENTS[6:]
    reader = csv.reader(__NOTES, delimiter="\t",quotechar="\"")
    NOTES = list(reader)#[0:1]
    IDX_TAGS = 8

wanted: list[list[str]] = (
        Enumerable(NOTES)
            .group_by(key_names=["front"], key=lambda x: x[IDX.FRONT.value])
            .select(lambda x:
                (
                    x
                        .select(lambda y: y[IDX.BACK.value])
                        .distinct(lambda y: y)
                        .aggregate(lambda s, v: f"{s}<br/>{v}" if s != "" else v, ""),
                    x.order_by(lambda y: reviews(y)).last()
                )
            ).select(lambda x: replace_field(IDX.BACK, x[1], x[0]))
            .to_list()
)
wanted_guids = set(
    Enumerable(wanted)
        .select(lambda x: x[IDX.GUID.value])
        .to_list()
)
unwanted: list[list[str]] = (
    Enumerable(NOTES)
        .where(lambda x: x[IDX.GUID.value] not in wanted_guids)
        .select(lambda x: replace_field(IDX.FRONT, x, "MARKED_FOR_DELETION"))
        .select(lambda x: replace_field(IDX.BACK, x, "MARKED_FOR_DELETION"))
        .to_list()
)

all_rows = wanted + unwanted

with open(arguments.dst_file, "w", encoding="UTF8") as file:
    file.writelines(HEADER)
with open(arguments.dst_file, "a", encoding="UTF8", newline='') as file:
    writer = csv.writer(file, delimiter="\t", quotechar="\"")
    writer.writerows(all_rows)

