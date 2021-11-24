# Local application/library specific imports

from pyaww import Console


def test_send_input(
    started_console: Console,
) -> None:  # this method also tests pyaww.Console.outputs()
    assert isinstance(started_console.send_input("echo hello!"), str)


def test_delete(unstarted_console: Console) -> None:  # cleanup + test
    assert unstarted_console.delete() is None
