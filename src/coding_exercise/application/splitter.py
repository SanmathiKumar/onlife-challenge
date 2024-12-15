# -----------------------------------------------------------------------------
# Author: Sanmathi Kumar
# Description: Implementation of the Splitter class, which splits a cable into
#              multiple smaller cables of nearly equal lengths while handling
#              edge cases such as remainders and input validation.
# -----------------------------------------------------------------------------
import math

from coding_exercise.domain.model.cable import Cable

MIN_ALLOWED_SPLITS, MAX_ALLOWED_SPLITS = 1, 64
MIN_CABLE_LENGTH, MAX_CABLE_LENGTH = 2, 1024


class Splitter:

    @staticmethod
    def __validate(cable: Cable, times: int):
        """
        Validates the input parameters to ensure they adhere to defined constraints.

        :param cable: Cable object containing length and name
        :param times: Number of splits requested
        :raises ValueError: If the parameters are out of bounds
        """
        # Ensure the number of splits is within the allowed range
        if not (MIN_ALLOWED_SPLITS <= times <= MAX_ALLOWED_SPLITS):
            raise ValueError(
                f"The number of times must be between {MIN_ALLOWED_SPLITS} and {MAX_ALLOWED_SPLITS}."
            )
        # Ensure the cable length is within the allowed range
        if not (MIN_CABLE_LENGTH <= cable.length <= MAX_CABLE_LENGTH):
            raise ValueError(
                f"The cable length must be between {MIN_CABLE_LENGTH} and {MAX_CABLE_LENGTH}."
            )
        # Ensure that the requested splits are feasible
        if times >= cable.length:
            raise ValueError("The number of splits must be less than the cable length.")

    def split(self, cable: Cable, times: int) -> list[Cable]:
        """
        Splits a cable into multiple smaller cables with nearly equal lengths.

        :param cable: Cable object containing length and name
        :param times: Number of splits requested
        :return: A list of Cable objects representing the splits
        :raises ValueError: If the split length is less than 1
        """
        # Validate the input parameters
        self.__validate(cable, times)

        init_length = cable.length // (times + 1)

        result = [Cable(init_length, "")]
        times -= 1
        cable_count = 1
        remaining = cable.length - init_length
        while times:
            result.append(Cable(init_length, f""))
            times -= 1
            cable_count += 1
            remaining -= init_length

        while remaining and remaining > init_length:
            result.append(Cable(init_length, f""))
            cable_count += 1
            remaining -= init_length

        if remaining > 0:
            result.append(Cable(remaining, f""))

        pad_len = int(math.log10(cable_count)) + 1
        suffix = cable.name if cable.name.endswith("s") else f"{cable.name}s"
        for i, cable in enumerate(result):
            cable.name = f"{suffix}-{str(i).zfill(pad_len)}"
        return result
