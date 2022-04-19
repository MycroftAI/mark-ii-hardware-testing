"""
sudo apt-get update && sudo apt-get install python3-gpiozero python-gpiozero


run with:
sudo python3 gpiotest.py

"""

from gpiozero import Button
from time import sleep

DEFAULT_TIMEOUT = 5


class button_check:
    def __init__(self) -> None:
        self.pressed = False

    def was_pressed(self):
        self.pressed = True


def test_buttons():
    buttons = (
        (Button(22), "volume up button on the right"),
        (Button(23), "volume down button in middle"),
        (Button(24), "action button in the center of the LED ring"),
    )
    for button, description in buttons:
        check = button_check()
        print(f"Press the {description}")
        button.when_pressed = check.was_pressed
        button.wait_for_press(DEFAULT_TIMEOUT)
        if not check.pressed:
            return False
    return True


def test_mic_switch():
    """Instruct user to mute and unmute the mic."""
    mic_switch = Button(25)  # ON = not muted
    if not mic_switch.is_pressed:
        print("Unmute the mic by pushing the switch to the right.")
        print("==>> ==>> ==>> ==>> ==>> ==>> ==>>")
        mic_switch.wait_for_press(DEFAULT_TIMEOUT)
        sleep(0.1)
        assert mic_switch.is_pressed
    print("Mute the mic by pushing the switch to the left.")
    print("<<== <<== <<== <<== <<== <<== <<==")
    mic_switch.wait_for_release(DEFAULT_TIMEOUT)
    sleep(0.1)
    assert not mic_switch.is_pressed
    print("Unmute the mic by pushing the switch to the right.")
    print("==>> ==>> ==>> ==>> ==>> ==>> ==>>")
    mic_switch.wait_for_press(DEFAULT_TIMEOUT)
    sleep(0.1)
    assert mic_switch.is_pressed
    return True


if __name__ == "__main__":
    test_results = {"buttons": None, "mic_switch": None}
    test_results["buttons"] = test_buttons()
    try:
        test_results["mic_switch"] = test_mic_switch()
    except AssertionError:
        test_results["mic_switch"] = False

    if all(test_results.values()):
        print("SUCCESS")
    else:
        print("TEST FAILURE")
