"""Regression checks for the previously uncommitted required-condition behavior."""
import copy
import unittest

from ranking_service import rank_vehicles


class RequiredConditionTests(unittest.TestCase):
    def setUp(self):
        self.preference = dict(minBudget=3000, maxBudget=5000, bodyTypes=['SUV'],
                               powertrains=['하이브리드'], origins=['국산'], features=['통풍시트', '후방카메라'])
        self.vehicle = dict(model='일치 차량', priceFrom=35000000, bodyType='SUV',
                            powertrain='가솔린 하이브리드', origin='국산', features=['통풍시트', '후방카메라'])

    def test_selected_conditions_are_required(self):
        for field, value in [('bodyType', '세단'), ('powertrain', '전기'), ('origin', '수입')]:
            with self.subTest(field=field):
                self.assertEqual(rank_vehicles([dict(self.vehicle, **{field: value})], self.preference), [])

    def test_every_selected_feature_is_required(self):
        self.assertEqual(rank_vehicles([dict(self.vehicle, features=['통풍시트'])], self.preference), [])

    def test_multiple_types_are_alternatives(self):
        preference = dict(self.preference, bodyTypes=['세단', 'SUV'])
        self.assertEqual(len(rank_vehicles([self.vehicle], preference)), 1)

    def test_unselected_conditions_do_not_filter(self):
        result = rank_vehicles([dict(self.vehicle, bodyType='세단', features=[])], dict(minBudget=3000, maxBudget=5000))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['reasons'], ['예산 범위 일치'])

    def test_budget_uses_won_and_includes_boundaries(self):
        vehicles = [dict(self.vehicle, priceFrom=p) for p in [29999999, 30000000, 50000000, 50000001]]
        self.assertEqual([v['priceFrom'] for v in rank_vehicles(vehicles, self.preference)], [30000000, 50000000])

    def test_missing_price_is_excluded(self):
        self.assertEqual(rank_vehicles([dict(self.vehicle, priceFrom=None)], self.preference), [])

    def test_equal_matches_are_sorted_by_price(self):
        expensive = dict(self.vehicle, priceFrom=45000000)
        result = rank_vehicles([expensive, self.vehicle], self.preference)
        self.assertEqual([v['priceFrom'] for v in result], [35000000, 45000000])
        self.assertEqual(result[0]['score'], result[1]['score'])

    def test_inputs_are_not_mutated(self):
        original = copy.deepcopy(self.vehicle)
        rank_vehicles([self.vehicle], self.preference)
        self.assertEqual(self.vehicle, original)
        self.assertNotIn('score', self.vehicle)


if __name__ == '__main__':
    unittest.main()
