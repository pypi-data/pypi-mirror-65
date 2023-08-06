# -*- coding: utf-8 -*-
"""openepda.updk.py

This file contains tools to work with uPDK files.

Author: Dima Pustakhod
Copyright: 2020, TU/e - PITC and authors
"""
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from .expr import ensure_num
from .validators import _check_building_block
from .validators import is_updk_sbb_valid

try:
    from ruamel.yaml import YAML

    yaml = YAML(typ="safe")
    safe_load = yaml.load
except ImportError:
    from yaml import safe_load

REQUIRED_NAZCA_VERSION = "0.5.10"

try:
    import nazca as nd

    if nd.__version__ != REQUIRED_NAZCA_VERSION:
        print(
            "This version of openepda requires nazca-{}. "
            "Version {} is installed.".format(
                REQUIRED_NAZCA_VERSION, nd.__version__
            )
        )
        HAS_NAZCA_DESIGN = False
    else:
        HAS_NAZCA_DESIGN = True
except ImportError:
    HAS_NAZCA_DESIGN = False


DEFAULT_PIN_LAYER = 1004


def _check_or_add_xsection(xs_name, layer=DEFAULT_PIN_LAYER):
    if not HAS_NAZCA_DESIGN:
        print("This function requires nazca package.")
        return

    try:
        nd.get_xsection(xs_name)
    except Exception as e:
        nd.add_layer(name=xs_name, layer=layer, accuracy=0.05)
        nd.add_xsection(name=xs_name)
        nd.add_layer2xsection(xsection=xs_name, layer=xs_name, accuracy=0.05)


class BB(object):
    """Building block class to handle the uPDK block data.

    """

    CELL_TYPES = {0: "static", 1: "p-cell"}

    def __init__(self, name, bb_data):
        self.name = name

        self._bb_data = None
        self.bb_data = bb_data
        self._cell = None

    @property
    def bb_data(self) -> Dict:
        return self._bb_data

    @bb_data.setter
    def bb_data(self, bb_data):
        if self._bb_data:
            raise UserWarning(
                "Can not change the existing BB. Create a new one instead."
            )
        self._bb_data = bb_data

        try:
            _check_building_block(self.name, self._bb_data)
        except Exception as e:
            self._bb_data = None
            raise ValueError("Error validating the BB data: {}.".format(e))

    @property
    def is_pcell(self) -> bool:
        """Flag if the building block is parametric.

        Returns
        -------
        bool
            True if the building block is a p-cell, False if it is static.
        """
        return True if self._bb_data["parameters"] else False

    @property
    def cell_type(self) -> str:
        return BB.CELL_TYPES[self.is_pcell]

    @property
    def pins(self) -> Dict[str, Dict]:
        return self._bb_data["pins"]

    @property
    def n_pins(self) -> int:
        return len(self._bb_data["pins"])

    @property
    def pin_names(self) -> Tuple[str]:
        pins: List[str] = sorted(self._bb_data["pins"].keys())
        return tuple(pins)

    def __str__(self) -> str:
        return "<BB {} ({}, {} pins)>".format(
            self.name, self.cell_type, self.n_pins
        )

    @property
    def bbox(self) -> "BBox":
        return BBox.from_points(self.bb_data["bbox"])

    def make_cell(self) -> Optional["nd.Cell"]:
        """Create a cell for the building block.

        This method runs only if nazca package is installed.
        The cell is also saved as a private attribute.

        Returns
        -------
        Optional[nazca.Cell]
            None is returned in case of parametric cell or if nazca is
            not installed.
        """
        if not HAS_NAZCA_DESIGN:
            print("This function requires nazca package.")
            return None
        if self.is_pcell:
            print("Cannot create a cell for a p-cell.")
            return None

        with nd.Cell(self.name, hashme=False) as C:
            # C.default_pins(bb_data["pin_in"], bb_data["pin_out"])
            # C.autobbox = True
            # C.store_pins = STORE_PINS
            # C.version = version
            for name, prop in self.pins.items():
                xs = prop["xsection"]
                w = prop["width"]
                doc = prop["doc"]

                _check_or_add_xsection(xs)
                nd.Pin(name=name, xs=xs, width=w, remark=doc).put(*prop["xya"])

            nd.put_stub(list(self.pin_names))

            bbox = self.bbox

            nd.put_boundingbox(
                "org",
                length=bbox.length,
                width=bbox.width,
                raise_pins=False,
                move=(bbox.sw[0], bbox.sw[1], 0),
                align="lb",
            )
            # C._add_bbox()
            # if bb_text[bn]:
            #     nd.text(bb_text[bn], height=3, align="cc", layer="DeepLogic").put(
            #         C.pin["bc"].move(-3, 0, 90)
            #     )
        self._cell = C
        return C


class BBox(object):
    """Class to handle building block bounding boxes.

    Bounding box is a rectangle aligned with XY axis, and is characterized
    by its south-west and north-east corners.
    """

    def __init__(self, sw: Tuple[float, float], ne: Tuple[float, float]):
        assert sw[0] < ne[0]
        assert sw[1] < ne[1]
        self._sw = sw
        self._ne = ne

    @property
    def length(self) -> float:
        """Bounding box size along X-axis

        Returns
        -------
        float
        """
        length = self._ne[0] - self._sw[0]
        assert length >= 0
        return length

    @property
    def width(self) -> float:
        """Bounding box size along Y-axis

        Returns
        -------
        float
        """
        w = self._ne[1] - self._sw[1]
        assert w >= 0
        return w

    @property
    def sw(self) -> Tuple[float, float]:
        return self._sw

    @property
    def ne(self) -> Tuple[float, float]:
        return self._ne

    @property
    def nw(self) -> Tuple[float, float]:
        return self._sw[0], self._ne[1]

    @property
    def se(self) -> Tuple[float, float]:
        return self._ne[0], self._sw[1]

    @staticmethod
    def from_points(pts: Iterable[Tuple[float, float]]):
        """Create a bounding box from a list of points.

        Points can describe any polygon.

        Parameters
        ----------
        pts: Iterable[Tuple[float, float]]
            List of (x, y) coordinates of the points.

        Returns
        -------
        BBox
            Minimal bounding box which includes all points.
        """
        x_coords = [ensure_num(p[0]) for p in pts]
        y_coords = [ensure_num(p[1]) for p in pts]

        x_min = min(x_coords)
        x_max = max(x_coords)
        y_min = min(y_coords)
        y_max = max(y_coords)
        return BBox(sw=(x_min, y_min), ne=(x_max, y_max))


class UPDK(object):
    """Class to handle the uPDK file data.
    """

    def __init__(self, updk_data):
        self._updk_data = None
        self.updk_data = updk_data
        self._cells: Dict[str, "nd.Cell"] = {}

    @property
    def updk_data(self):
        return self._updk_data

    @updk_data.setter
    def updk_data(self, updk_data):
        is_updk_sbb_valid(updk_data, raise_error=True)
        self._updk_data = updk_data

    @staticmethod
    def from_file(filename):
        """Create a UPDK instance from a uPDK file.

        Parameters
        ----------
        filename
            str or a path-like object

        Returns
        -------
        UPDK
        """
        with open(filename) as s:
            updk_data = safe_load(s)
        return UPDK(updk_data)

    @property
    def building_block_names(self):
        return sorted(list(self._updk_data["blocks"].keys()))

    def get_building_block_data(self, bb_name):
        if bb_name in self.building_block_names:
            return self._updk_data["blocks"][bb_name]
        else:
            raise ValueError(
                "Building block '{bb_name}' is not defined in the uPDK."
            )

    def get_building_block(self, bb_name):
        bb_data = self.get_building_block_data(bb_name)
        bb = BB(bb_name, bb_data)
        return bb

    @property
    def cell_dict(self) -> Dict[str, "nd.Cell"]:
        return self._cells

    @property
    def cells(self) -> Tuple["nd.Cell"]:
        return tuple(self._cells.values())

    def make_cells(self) -> None:
        """Create cells for the building blocks.

        This method runs only if nazca package is installed.
        Only static cells are processed now. The created cells are
        available via UPDK.cells or UPDK.cell_dict properties.

        Returns
        -------
        None
        """
        if not HAS_NAZCA_DESIGN:
            print("This function requires nazca package.")
            return

        for bb_name in self.building_block_names:
            bb = self.get_building_block(bb_name)
            if bb.is_pcell:
                continue
            self._cells.update({bb_name: bb.make_cell()})

    def export_cells(self, filename) -> None:
        """Export building block cells to a GDSII file.

        This method runs only if nazca package is installed.
        The cells should be first created usign UPDK.make_cells() method.

        Parameters
        ----------
        filename : str
            The target GDSII filename.
        """
        if not HAS_NAZCA_DESIGN:
            print("This function requires nazca package.")
            return

        if not self.cells:
            print(
                "No cells were created for this PDK. "
                "Run UPDK.make_sells() first."
            )

        nd.export_gds(list(self.cells), filename=filename)
