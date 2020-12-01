from unittest import TestCase
from ds_exam.sequence_question import find_most_frequent
import random


class SequenceTest(TestCase):

    def test_implementation(self):
        in1 = [1]
        in2 = random.choices([2, 3, 4, 5, 6], k=100)
        in2 = in2 + [7]*101
        random.shuffle(in2)
        print(in2)
        out1 = find_most_frequent(in1)
        out2 = find_most_frequent(in2)
        self.assertEqual(out1, 1)
        self.assertEqual(out2, 7)
