# Bright Network Coding Challenge

## How to

### Run

Run the following in your terminal

```shell
poetry install && poetry run opportunities show
```

### Test

Run the following in your terminal

```shell
poetry install && poetry run pytest
```

## Architecture

![](https://www.dandoescode.com/_next/image?url=%2Fstatic%2Fimages%2Fclean-architecture-an-introduction%2Fclean-architecture.png&w=1200&q=75)

This project follows Clean Architecture by structuring code into layers with clear boundaries and dependencies, it promotes separation of concerns, making it easier to understand and modify. This approach allows for independent development and testing of each layer, improving code quality and reducing the risk of bugs.

## Algorithm

### Overview

The algorithm matches members to jobs in two steps:

1. identify preferred locations
   Given the list of distinct job locations available, identify any matching mentions of said locations in a given members bio. Then consider the context to the left of said location to identify whether the mention of the location is inclusive or exclusive and return a list of locations accordingly.
2. cross-reference words from member bio to job title
   Using the given list of preferred locations, identify the subset of jobs in said locations. Then extracts words from each given members biography and identify jobs with titles that contain that substring. I originally tried splitting the words in each propoerty into arrays and attempting to find matches in both, however, this does not work for instances where a member has expressed interest in a topic rather than the role associated with said topic e.g. design -> designer.

### Limitations

- May only find locations in user biographies if said location is in the distinct list of locations for which a job is available
- May only determine a preferred location from a biography that contains multiple locations based on a small subset of terms which must occur prior to the preferred location in the biography.
- Does not determine if one given geography is encapsulated by another e.g. London is within the UK.
- Only considers words greater than three characters as relevant for cross-referencing
