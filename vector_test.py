from unittest import TestCase
from ds_exam_solution.vector import Vector, SparseVector, DenseVector


class VectorsTest(TestCase):

    def test_create_dense_vector(self):
        v = DenseVector(1, 3, -2, 5, -6, 0, 3, 0)
        self.assertEqual(v.size, 8)

        with self.assertRaises(AssertionError) as cm:
            DenseVector()
        self.assertTrue('vectors must have at least 1 value' in str(cm.exception))

        with self.assertRaises(AssertionError) as cm:
            DenseVector(1, 'b')
        self.assertTrue("""values must be numeric, got 'b'""" in str(cm.exception))

    def test_create_sparse_vector(self):
        v = SparseVector(10, [3, 5, 6], [1, 2, 3])
        self.assertEqual(v.size, 10)

        empty = Vector.zero(4)
        self.assertEqual(empty.size, 4)
        for i in range(empty.size):
            self.assertEqual(empty[i], 0)

        some_zeros = SparseVector(6, [0, 1, 2], [0, 0, 1])
        self.assertEqual(len(some_zeros.indices), 1)

        with self.assertRaises(AssertionError) as cm1:
            SparseVector(-1, [1], [1])
        self.assertTrue('size must be greater than 0, got -1' in str(cm1.exception))

        with self.assertRaises(AssertionError) as cm2:
            SparseVector(2, [2], [1])
        self.assertTrue('found an index (2) that is greater than size (2)' in str(cm2.exception))

        with self.assertRaises(AssertionError) as cm3:
            SparseVector(4, [1, 2], [1, 1, 1])
        self.assertTrue('length of indices is not equal to length of values' in str(cm3.exception))

        with self.assertRaises(AssertionError) as cm4:
            SparseVector(4, [-1, -2], [1, 1])
        self.assertTrue("can't instantiate SparseVector with negative indices, got [-1, -2]" in str(cm4.exception))

        with self.assertRaises(AssertionError) as cm5:
            SparseVector(4, [2, 2], [1, 1])
        self.assertTrue("index 2 is duplicate in the indices" in str(cm5.exception))

    def test_eq(self):
        d1 = DenseVector(1, 3, -2)
        d2 = DenseVector(1, 3, -2)
        self.assertEqual(d1, d2)

        s1 = SparseVector(4, [0, 2], [1, 2])
        s2 = SparseVector(4, [0, 2], [1, 2])
        self.assertEqual(s1, s2)

    def test_vector_getitem(self):
        dv = DenseVector(1, 3, -2, 5, -6, 0, 3, 0)
        sv = SparseVector(10, [3, 5, 6], [1, 2, 3])
        self.assertEqual(dv[0], 1)
        self.assertEqual(dv[1], 3)
        self.assertEqual(dv[2], -2)

        self.assertListEqual(dv[0:2].values, DenseVector(1, 3).values)
        self.assertListEqual(dv[2:5].values, DenseVector(-2, 5, -6).values)

        self.assertEqual(sv[0], 0)
        self.assertEqual(sv[1], 0)
        self.assertEqual(sv[3], 1)
        self.assertEqual(sv[5], 2)
        self.assertEqual(sv[6], 3)

        self.assertListEqual(sv[2:5].values, [0, 1, 0])

    def test_neg(self):
        d1 = DenseVector(1, 2, 3, 4)
        d2 = -d1
        self.assertEqual(d1 + d2, SparseVector(4, [], []))
        self.assertEqual(d1 - d1, SparseVector(4, [], []))

        s1 = SparseVector(4, [1, 3], [1, 1])
        s2 = -s1
        self.assertEqual(s1 + s2, SparseVector(4, [], []))

    def test_add(self):
        d1 = DenseVector(1, 2, 3, 4)
        d2 = DenseVector(2, 2, 5, 5)
        out0 = d1 + 0
        out1 = d1 + 3
        out2 = d1 + d2
        self.assertEqual(out0, d1)
        self.assertEqual(out1, DenseVector(4, 5, 6, 7))
        self.assertEqual(out2, DenseVector(3, 4, 8, 9))

        s1 = Vector.zero(4)
        s2 = SparseVector(4, [1, 3], [1, 7])
        self.assertEqual(s1 + d1, d1)
        self.assertEqual(s2 + d1, DenseVector(1, 3, 3, 11))
        self.assertEqual(s1 + 1, DenseVector(1, 1, 1, 1))

        with self.assertRaises(AssertionError) as cm:
            DenseVector(1, 2, 3, 4) + DenseVector(1, 2)
        self.assertTrue('other vector size (2) is not compatible with (4)' in str(cm.exception))

        with self.assertRaises(AssertionError) as cm:
            DenseVector(1, 2, 3, 4) + Vector.zero(2)
        self.assertTrue('other vector size (2) is not compatible with (4)' in str(cm.exception))

    def test_mult(self):
        d1 = DenseVector(1, 2, 3, 4)
        d2 = DenseVector(2, 2, 5, 5)
        out0 = d1 * 0
        out1 = d1 * 3
        out2 = d1 * d2
        out3 = d1 / d2
        self.assertEqual(out0, Vector.zero(4))
        self.assertEqual(out1, DenseVector(3, 6, 9, 12))
        self.assertEqual(out2, DenseVector(2, 4, 15, 20))

        self.assertTrue(out3.almost_equal(DenseVector(1/2, 1, 3/5, 4/5)))

        self.assertEqual(d1, d1*1)
        self.assertEqual(d1, d1/1)

    def test_compress(self):
        d1 = DenseVector(0, 0, 0, 0)
        self.assertTrue(type(d1) == DenseVector)
        self.assertTrue(type(d1.compress) == SparseVector)

        s1 = SparseVector(4, [0, 1, 2, 3], [1, 1, 1, 1])
        self.assertTrue(type(s1) == SparseVector)
        self.assertTrue(type(s1.compress) == DenseVector)

        d2 = DenseVector(1, 1, 1, 1)
        self.assertEqual(d2 * 0, SparseVector(4, [], []))
        self.assertEqual(d2 - 1, SparseVector(4, [], []))

    def test_dot(self):
        v0 = Vector.zero(8)
        v1 = Vector.one(8)
        d1 = DenseVector(1, 2, 3, 4, 5, 6, 7, 8)
        s1 = SparseVector(8, [1, 4], [2, -2])

        self.assertEqual(v0.dot(v1), 0)
        self.assertEqual(v1.dot(v0), 0)
        self.assertEqual(d1.dot(v0), 0)
        self.assertEqual(s1.dot(v0), 0)

        self.assertEqual(v1.dot(d1), 36)
        self.assertEqual((v1*2).dot(d1), 72)
        self.assertEqual(v1.dot(s1), 0)
        self.assertEqual(d1.dot(s1), -6)
