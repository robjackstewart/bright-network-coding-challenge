from typing import Tuple
from src.application.common.interfaces import GeographyCalculatorInterface


class GeographyCalculator(GeographyCalculatorInterface):

    def extract_preferred_geographies(
        self, subject: str, available_geographies: list[str]
    ) -> list[str]:
        non_inclusive_prefixes = ["outside of", "not in", "outwith"]
        inclusive_prefixes = ["within", "in"]
        migrate_to_to_stems = ["relocate to"]
        migrate_from_stems = ["away from", "leave", "exit"]

        subject = subject.lower()

        geographies_in_subject_with_index: [Tuple[str, int]] = []

        for geography in available_geographies:
            index_of_location_in_subject = subject.find(geography)
            if index_of_location_in_subject != -1:
                geographies_in_subject_with_index.append(
                    (geography, index_of_location_in_subject)
                )

        geographies_in_subject_count = len(geographies_in_subject_with_index)

        if geographies_in_subject_count == 0:
            return available_geographies
        elif geographies_in_subject_count == 1:
            geography, index = geographies_in_subject_with_index[0]
            subject_from_start_to_geography = subject[0:index]
            is_inclusive_of_geography = any(
                entry in subject_from_start_to_geography for entry in inclusive_prefixes
            )
            is_exclusive_of_geography = any(
                entry in subject_from_start_to_geography
                for entry in non_inclusive_prefixes
            )
            match (is_inclusive_of_geography, is_exclusive_of_geography):
                case (True, False):
                    return [geography]
                case (False, True):
                    return [geo for geo in available_geographies if geo != geography]
                case _:
                    return available_geographies
        else:

            return available_geographies
