from collections import OrderedDict

from holoviews.core import Dimension
from holoviews.core.ndmapping import NdIndexableMapping
from holoviews.testing import ViewTestCase


class DimensionTest(ViewTestCase):

    def test_dimension_init(self):
        Dimension('Test dimension')
        Dimension('Test dimension', cyclic=True)
        Dimension('Test dimension', cyclic=True, type=int)
        Dimension('Test dimension', cyclic=True, type=int, unit='Twilight zones')

    def test_dimension_call(self):
        dim1 = Dimension('Test dimension')
        dim2 = dim1(cyclic=True)
        self.assertEqual(dim2.cyclic,True)

        dim3 = dim1('New test dimension', unit='scovilles')
        self.assertEqual(dim3.name, 'New test dimension')
        self.assertEqual(dim3.unit, 'scovilles')

    def test_dimension_pprint(self):
        dim = Dimension('Test dimension', cyclic=True, type=float, unit='Twilight zones')
        self.assertEqual(dim.pprint_value(3.2345), 'Test dimension: 3.23 Twilight zones')
        self.assertEqual(dim.pprint_value(4.2344, rounding=3),  'Test dimension: 4.234 Twilight zones')


class NdIndexableMappingTest(ViewTestCase):

    def setUp(self):
        self.init_items_1D_list = [(1, 'a'), (5, 'b')]
        self.init_item_list = [((1, 2.0), 'a'), ((5, 3.0), 'b')]
        self.init_item_odict = OrderedDict([((1, 2.0), 'a'), ((5, 3.0), 'b')])
        self.dimension_labels = ['intdim', 'floatdim']
        self.dim1 = Dimension('intdim', type=int)
        self.dim2 = Dimension('floatdim', type=float)
        self.time_dimension = Dimension

    def test_idxmapping_init(self):
        NdIndexableMapping()

    def test_idxmapping_init_item_odict(self):
        NdIndexableMapping(self.init_item_odict, key_dimensions=[self.dim1, self.dim2])

    def test_idxmapping_init_item_list(self):
        NdIndexableMapping(self.init_item_list, key_dimensions=[self.dim1, self.dim2])

    def test_idxmapping_init_dimstr(self):
        NdIndexableMapping(self.init_item_odict, key_dimensions=self.dimension_labels)

    def test_idxmapping_init_dimensions(self):
        NdIndexableMapping(self.init_item_odict, key_dimensions=[self.dim1, self.dim2])

    def test_idxmapping_dimension_labels(self):
        idxmap = NdIndexableMapping(self.init_item_odict, key_dimensions=[self.dim1, 'floatdim'])
        self.assertEqual([d.name for d in idxmap.key_dimensions], self.dimension_labels)

    def test_idxmapping_ndims(self):
        dims = [self.dim1, self.dim2, 'strdim']
        idxmap = NdIndexableMapping(key_dimensions=dims)
        self.assertEqual(idxmap.ndims, len(dims))

    def test_idxmapping_key_len_check(self):
        try:
            NdIndexableMapping(initial_items=self.init_item_odict)
            raise AssertionError('Invalid key length check failed.')
        except KeyError:
            pass

    def test_idxmapping_nested_update(self):
        data1 = [(0, 'a'), (1, 'b')]
        data2 = [(2, 'c'), (3, 'd')]
        data3 = [(2, 'e'), (3, 'f')]

        ndmap1 = NdIndexableMapping(data1, key_dimensions=[self.dim1])
        ndmap2 = NdIndexableMapping(data2, key_dimensions=[self.dim1])
        ndmap3 = NdIndexableMapping(data3, key_dimensions=[self.dim1])

        ndmap_list = [(0.5, ndmap1), (1.5, ndmap2)]
        nested_ndmap = NdIndexableMapping(ndmap_list, key_dimensions=[self.dim2])
        nested_ndmap[(0.5,)].update(dict([(0, 'c'), (1, 'd')]))
        self.assertEquals(list(nested_ndmap[0.5].values()), ['c', 'd'])

        nested_ndmap[1.5] = ndmap3
        self.assertEquals(list(nested_ndmap[1.5].values()), ['e', 'f'])

    def test_idxmapping_reindex(self):
        data = [((0, 0.5), 'a'), ((1, 0.5), 'b')]
        ndmap = NdIndexableMapping(data, key_dimensions=[self.dim1, self.dim2])

        reduced_dims = ['intdim']
        reduced_ndmap = ndmap.reindex(reduced_dims)

        self.assertEqual([d.name for d in reduced_ndmap.key_dimensions], reduced_dims)

    def test_idxmapping_add_dimension(self):
        ndmap = NdIndexableMapping(self.init_items_1D_list, key_dimensions=[self.dim1])
        ndmap2d = ndmap.add_dimension(self.dim2, 0, 0.5)

        self.assertEqual(list(ndmap2d.keys()), [(0.5, 1), (0.5, 5)])
        self.assertEqual(ndmap2d.key_dimensions, [self.dim2, self.dim1])

    def test_idxmapping_apply_key_type(self):
        data = dict([(0.5, 'a'), (1.5, 'b')])
        ndmap = NdIndexableMapping(data, key_dimensions=[self.dim1])

        self.assertEqual(list(ndmap.keys()), [0, 1])


if __name__ == "__main__":
    import sys
    import nose
    nose.runmodule(argv=[sys.argv[0], "--logging-level", "ERROR"])
