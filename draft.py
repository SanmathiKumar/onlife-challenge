import sys


class Cable:

    def __set_length(self, length: int):
        if not isinstance(length, int) or length < 0 or length > sys.maxsize:
            raise ValueError

        self.length = length

    def __init__(self, length: int, name: str):
        self.__set_length(length)
        self.name = name

    def __eq__(self, other):
        if isinstance(other, Cable):
            return self.length == other.length and self.name == other.name

        return False


class Splitter:
    def __validate(self, cable: Cable, times: int):
        """
        Validates the input parameters to ensure they adhere to defined constraints.
        """
        if not (1 <= times <= 64):
            raise ValueError("The number of times must be between 1 and 64.")
        if not (2 <= cable.length <= 1024):
            raise ValueError("The cable length must be between 2 and 1024.")
        if times > cable.length - 1:
            raise ValueError("Cannot split the cable into pieces smaller than 1 in length.")

    def split(self, cable: Cable, times: int) -> list[Cable]:
        """
        Splits a cable into multiple smaller cables while adhering to the rules.
        """
        # Validate inputs
        self.__validate(cable, times)

        # Special case: Fully split into 1-length cables
        if times + 1 == cable.length:
            return [Cable(1, f"{cable.name}-{str(i).zfill(2)}") for i in range(cable.length)]

        # General case
        split_length = cable.length // (times + 1)
        remainder = cable.length % (times + 1)

        result = []
        for i in range(times + 1):
            length = split_length + 1 if remainder > 0 else split_length
            result.append(Cable(length, f"{cable.name}-{str(i).zfill(2)}"))
            if remainder > 0:
                remainder -= 1

        # Handle additional splitting of remainder if possible
        extra = []
        for cable in result:
            while cable.length > split_length + 1:
                extra.append(Cable(split_length + 1, f"{cable.name}-extra"))
                cable.length -= (split_length + 1)

        return result + extra


# Test cases
if __name__ == "__main__":
    splitter = Splitter()

    # Test 1: Split evenly
    cable1 = Cable(10, "coconuts")
    result1 = splitter.split(cable1, 2)
    print("Test 1 Result:", result1)  # Expected: [3, 3, 3, 1]

    # Test 2: Fully split into 1-length cables
    cable2 = Cable(5, "bananas")
    result2 = splitter.split(cable2, 2)
    print("Test 2 Result:", result2)  # Expected: [1, 1, 1, 1, 1]

    # Test 3: Invalid number of splits
    try:
        cable3 = Cable(5, "apples")
        result3 = splitter.split(cable3, 10)
    except ValueError as e:
        print("Test 3 Error:", e)

    # Test 4: Minimum cable length
    cable4 = Cable(3, "oranges")
    result4 = splitter.split(cable4, 1)
    print("Test 4 Result:", result4)  # Expected: [2, 1]

    # Test 5: Maximum allowed cable length and splits
    cable5 = Cable(1024, "pineapples")
    result5 = splitter.split(cable5, 64)
    print("Test 5 Result (first 5):", result5[:5])  # Expected: 64 parts of 16

    # Test 6: Complex split with non-divisible remainder
    cable6 = Cable(13, "grapes")
    result6 = splitter.split(cable6, 3)
    print("Test 6 Result:", result6)  # Expected: [4, 3, 3, 3]
