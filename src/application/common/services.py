from typing import Tuple
from src.application.common.interfaces import GeographyCalculatorInterface
from src.common.utils import chunk


class GeographyCalculator(GeographyCalculatorInterface):
    __NON_INCLUSIVER_PREFIXES = ["outside of", "not in", "outwith"]
    __INCLUSIVE_PREFIXES = ["within", "in"]
    __MIGRATE_TO_PREFIXES = ["relocate to", "move to"]
    __MIGRATE_FROM_PREFIXES = ["away from", "leave", "exit"]

    def extract_preferred_geographies(
        self, subject: str, available_geographies: list[str]
    ) -> list[str]:

        preferred_geographies = set()

        subject = subject.lower()

        sections, geography_indicies = chunk(subject, available_geographies)

        geographies_in_subject_count = len(geography_indicies)

        if geographies_in_subject_count == 0:
            return available_geographies
        elif geographies_in_subject_count == 1:
            subject_from_start_to_geography = sections[geography_indicies[0] - 1]
            is_inclusive_of_geography = any(
                entry in subject_from_start_to_geography
                for entry in GeographyCalculator.__INCLUSIVE_PREFIXES
            )
            is_exclusive_of_geography = any(
                entry in subject_from_start_to_geography
                for entry in GeographyCalculator.__NON_INCLUSIVER_PREFIXES
            )
            match (is_inclusive_of_geography, is_exclusive_of_geography):
                case (True, False):
                    preferred_geographies.add(sections[geography_indicies[0]])
                case (False, True):
                    for geo in available_geographies:
                        if geo != sections[geography_indicies[0]]:
                            preferred_geographies.add(geo)
                case _:
                    preferred_geographies = available_geographies
        else:

            for index in geography_indicies:
                subject_from_start_to_geography = sections[index - 1]
                is_inclusive_of_geography = any(
                    entry in subject_from_start_to_geography
                    for entry in GeographyCalculator.__MIGRATE_TO_PREFIXES
                )
                is_exclusive_of_geography = any(
                    entry in subject_from_start_to_geography
                    for entry in GeographyCalculator.__MIGRATE_FROM_PREFIXES
                )
                if is_inclusive_of_geography and not is_exclusive_of_geography:
                    preferred_geographies.add(sections[index])
                else:
                    for geo in available_geographies:
                        if geo != sections[index]:
                            preferred_geographies.add(geo)

        return list(preferred_geographies)
