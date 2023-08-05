#! /usr/bin/env python3
import pathlib
from typing import Dict, Any, Sequence, Tuple

from ._base import Hardware

__all__ = ["ContinuousHardware"]


class ContinuousHardware(Hardware):
    traits = ["has-limits"]
    _kind: str = "continuous-hardware"
    defaults = {"out_of_limits": "closest", "limits": (-float("inf"), float("inf"))}

    def __init__(
        self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path
    ):
        super().__init__(name, config, config_filepath)
        self._out_of_limits = config["out_of_limits"]
        self._hw_limits = (-float("inf"), float("inf"))

    def get_limits(self) -> Tuple[float, float]:
        assert self._hw_limits[0] < self._hw_limits[1]
        config_limits = self.config["limits"]
        assert config_limits[0] < config_limits[1]
        out = (
            max(self._hw_limits[0], config_limits[0]),
            min(self._hw_limits[1], config_limits[1]),
        )
        assert out[0] < out[1]
        return out

    def in_limits(self, position: float) -> bool:
        low, upp = self.get_limits()
        if low <= position <= upp:
            return True
        else:
            return False

    def set_position(self, position: float) -> None:
        if not self.in_limits(position):
            if self._out_of_limits == "closest":
                low, upp = self.get_limits()
                if position > upp:
                    position = upp
                elif position < low:
                    position = low
            elif self._out_of_limits == "ignore":
                return
            else:
                raise ValueError(f"{position} not in ranges {self.get_limits()}")
        super().set_position(position)

    def get_state(self) -> Dict[str, Any]:
        state = super().get_state()
        state["hw_limits"] = self._hw_limits
        return state

    def _load_state(self, state: Dict[str, Any]) -> None:
        super()._load_state(state)
        self._hw_limits = state.get("hw_limits", (float("-inf"), float("inf")))


if __name__ == "__main__":
    ContinuousHardware.main()
