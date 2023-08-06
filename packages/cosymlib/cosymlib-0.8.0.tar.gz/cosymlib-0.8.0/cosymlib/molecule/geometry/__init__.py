from cosymlib import shape, tools
from cosymlib.symmetry import Symmetry
from cosymlib.symmetry.pointgroup import PointGroup
import numpy as np


def set_parameters(func):
    def wrapper(*args, **kwargs):
        args[0]._symmetry.set_parameters(kwargs)
        return func(*args, **kwargs)
    return wrapper


class Geometry:
    def __init__(self,
                 positions,
                 symbols=(),
                 name=None,
                 connectivity=None):

        # self._central_atom = None
        self._symbols = []
        self._positions = []
        self._atom_groups = list(symbols)

        if name.strip():
            self._name = name
        else:
            self._name = ' ' * 5

        for symbol in symbols:
            try:
                int(symbol)
                self._symbols.append(tools.atomic_number_to_element(int(symbol)))
            except (ValueError, TypeError):
                self._symbols.append(symbol.capitalize())
                for ida, a in enumerate(symbol):
                    try:
                        int(a)
                        self._symbols[-1] = self._symbols[-1][:ida]
                        break
                    except (ValueError, TypeError, IndexError):
                        pass

        try:
            float(positions[0])
            for symbol in positions:
                self._positions.append(float(symbol))
            self._positions = list(chunks(self._positions, 3))
        except (ValueError, TypeError, IndexError):
            for symbol in positions:
                self._positions.append([float(j) for j in symbol])

        self._positions = np.array(self._positions)
        self._connectivity = connectivity
        self._shape = shape.Shape(self)
        self._symmetry = Symmetry(self)

    def __len__(self):
        return len(self._positions)

    @property
    def name(self):
        return self._name

    # TODO: 'symmetry' and 'shape' properties should be removed. Methods inside these
    # TODO: classes should be mirrored in geometry/molecule class. See get_symmetry_measure()

    @property
    def symmetry(self):
        return self._symmetry

    @property
    def shape(self):
        return self._shape

    def set_name(self, name):
        self._name = name

    def get_connectivity(self):
        return self._connectivity

    def set_connectivity(self, connectivity):
        self._connectivity = connectivity
        self._symmetry._connectivity = connectivity

    def set_symbols(self, symbols):
        self._symbols = symbols
        self._symmetry._symbols = symbols

    def set_positions(self, central_atom=0):
        atom, self._positions = self._positions[central_atom], np.delete(self._positions, central_atom, 0)
        self._positions = np.insert(self._positions, len(self._positions), atom, axis=0)
        self._symmetry._positions= self._positions
        self._shape._positions= self._positions

    def get_positions(self):
        return self._positions

    def get_n_atoms(self):
        return len(self.get_positions())

    def get_symbols(self):
        return self._symbols

    # Shape methods
    def get_shape_measure(self, shape_label, central_atom=0, fix_permutation=False):
        return self._shape.measure(shape_label, central_atom=central_atom, fix_permutation=fix_permutation)

    def get_shape_structure(self, shape_label, central_atom=0, fix_permutation=False):
        return self._shape.structure(shape_label, central_atom=central_atom, fix_permutation=fix_permutation)

    def get_path_deviation(self, shape_label1, shape_label2, central_atom=0):
        return self._shape.path_deviation(shape_label1, shape_label2, central_atom)

    def get_generalized_coordinate(self, shape_label1, shape_label2, central_atom=0):
        return self._shape.generalized_coordinate(shape_label1, shape_label2, central_atom)

    # Symmetry methods
    @set_parameters
    def get_symmetry_measure(self, label, multi=1, central_atom=0, connect_thresh=1.1, center=None):
        return self._symmetry.measure(label)

    @set_parameters
    def get_symmetry_nearest_structure(self, label, multi=1, central_atom=0, connect_thresh=1.1, center=None):
        return self._symmetry.nearest_structure(label)

    def get_pointgroup(self, tol=0.01):
        return PointGroup(self, tolerance=tol).get_point_group()


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]
