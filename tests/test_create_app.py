"""Test Pipeline Create App"""

import pytest

from nf_core.pipelines.create import PipelineCreateApp


@pytest.mark.asyncio
async def test_app_bindings():
    """Test that the app bindings work."""
    app = PipelineCreateApp()
    async with app.run_test() as pilot:
        # Test pressing the D key
        assert app.dark
        await pilot.press("d")
        assert not app.dark
        await pilot.press("d")
        assert app.dark

        # Test pressing the Q key
        await pilot.press("q")
        assert app.return_code == 0


def test_welcome(snap_compare):
    """Test snapshot for the first screen in the app. The welcome screen."""
    assert snap_compare("../nf_core/pipelines/create/__init__.py", terminal_size=(100, 50))


def test_choose_type(snap_compare):
    """Test snapshot for the choose_type screen.
    Steps to get to this screen:
        screen welcome > press start >
        screen choose_type
    """

    async def run_before(pilot) -> None:
        await pilot.click("#start")

    assert snap_compare("../nf_core/pipelines/create/__init__.py", terminal_size=(100, 50), run_before=run_before)


def test_basic_details_nfcore(snap_compare):
    """Test snapshot for the basic_details screen of an nf-core pipeline.
    Steps to get to this screen:
        screen welcome > press start >
        screen choose_type > press nf-core >
        screen basic_details
    """

    async def run_before(pilot) -> None:
        await pilot.click("#start")
        await pilot.click("#type_nfcore")

    assert snap_compare("../nf_core/pipelines/create/__init__.py", terminal_size=(100, 50), run_before=run_before)


def test_basic_details_custom(snap_compare):
    """Test snapshot for the basic_details screen of a custom pipeline.
    Steps to get to this screen:
        screen welcome > press start >
        screen choose_type > press custom >
        screen basic_details
    """

    async def run_before(pilot) -> None:
        await pilot.click("#start")
        await pilot.click("#type_custom")

    assert snap_compare("../nf_core/pipelines/create/__init__.py", terminal_size=(100, 50), run_before=run_before)


def test_type_nfcore(snap_compare):
    """Test snapshot for the type_nfcore screen.
    Steps to get to this screen:
        screen welcome > press start >
        screen choose_type > press nf-core >
        screen basic_details > enter pipeline details > press next >
        screen type_nfcore
    """

    async def run_before(pilot) -> None:
        await pilot.click("#start")
        await pilot.click("#type_nfcore")
        await pilot.click("#name")
        await pilot.press("m", "y", "p", "i", "p", "e", "l", "i", "n", "e")
        await pilot.press("tab")
        await pilot.press("A", " ", "c", "o", "o", "l", " ", "d", "e", "s", "c", "r", "i", "p", "t", "i", "o", "n")
        await pilot.press("tab")
        await pilot.press("M", "e")
        await pilot.click("#next")

    assert snap_compare("../nf_core/pipelines/create/__init__.py", terminal_size=(100, 50), run_before=run_before)


def test_type_nfcore_validation(snap_compare):
    """Test snapshot for the type_nfcore screen.
    Validation errors should appear when input fields are empty.
    Steps to get to this screen:
        screen welcome > press start >
        screen choose_type > press nf-core >
        screen basic_details > press next >
        ERRORS
    """

    async def run_before(pilot) -> None:
        await pilot.click("#start")
        await pilot.click("#type_nfcore")
        await pilot.click("#next")

    assert snap_compare("../nf_core/pipelines/create/__init__.py", terminal_size=(100, 50), run_before=run_before)


def test_type_custom(snap_compare):
    """Test snapshot for the type_custom screen.
    Steps to get to this screen:
        screen welcome > press start >
        screen choose_type > press custom >
        screen basic_details > enter pipeline details > press next >
        screen type_custom
    """

    async def run_before(pilot) -> None:
        await pilot.click("#start")
        await pilot.click("#type_custom")
        await pilot.click("#name")
        await pilot.press("tab")
        await pilot.press("m", "y", "p", "i", "p", "e", "l", "i", "n", "e")
        await pilot.press("tab")
        await pilot.press("A", " ", "c", "o", "o", "l", " ", "d", "e", "s", "c", "r", "i", "p", "t", "i", "o", "n")
        await pilot.press("tab")
        await pilot.press("M", "e")
        await pilot.click("#next")

    assert snap_compare("../nf_core/pipelines/create/__init__.py", terminal_size=(100, 50), run_before=run_before)


def test_final_details(snap_compare):
    """Test snapshot for the final_details screen.
    Steps to get to this screen:
        screen welcome > press start >
        screen choose_type > press nf-core >
        screen basic_details > enter pipeline details > press next >
        screen type_nfcore > press continue >
        screen final_details
    """

    async def run_before(pilot) -> None:
        await pilot.click("#start")
        await pilot.click("#type_nfcore")
        await pilot.click("#name")
        await pilot.press("m", "y", "p", "i", "p", "e", "l", "i", "n", "e")
        await pilot.press("tab")
        await pilot.press("A", " ", "c", "o", "o", "l", " ", "d", "e", "s", "c", "r", "i", "p", "t", "i", "o", "n")
        await pilot.press("tab")
        await pilot.press("M", "e")
        await pilot.click("#next")
        await pilot.click("#continue")

    assert snap_compare("../nf_core/pipelines/create/__init__.py", terminal_size=(100, 50), run_before=run_before)


def test_customisation_help(snap_compare):
    """Test snapshot for the type_custom screen - showing help messages.
    Steps to get to this screen:
        screen welcome > press start >
        screen choose_type > press nf-core >
        screen basic_details > enter pipeline details > press next >
        screen type_custom > press Show more
    """

    async def run_before(pilot) -> None:
        await pilot.click("#start")
        await pilot.click("#type_custom")
        await pilot.click("#name")
        await pilot.press("tab")
        await pilot.press("m", "y", "p", "i", "p", "e", "l", "i", "n", "e")
        await pilot.press("tab")
        await pilot.press("A", " ", "c", "o", "o", "l", " ", "d", "e", "s", "c", "r", "i", "p", "t", "i", "o", "n")
        await pilot.press("tab")
        await pilot.press("M", "e")
        await pilot.click("#next")
        await pilot.click("#igenomes")
        await pilot.press("tab")
        await pilot.press("enter")

    assert snap_compare("../nf_core/pipelines/create/__init__.py", terminal_size=(100, 50), run_before=run_before)


def test_github_question(tmpdir, snap_compare):
    """Test snapshot for the github_repo_question screen.
    Steps to get to this screen:
        screen welcome > press start >
        screen choose_type > press nf-core >
        screen basic_details > enter pipeline details > press next >
        screen type_nfcore > press continue >
        screen final_details > press finish > close logging screen >
        screen github_repo_question
    """

    async def run_before(pilot) -> None:
        await pilot.click("#start")
        await pilot.click("#type_nfcore")
        await pilot.click("#name")
        await pilot.press("m", "y", "p", "i", "p", "e", "l", "i", "n", "e")
        await pilot.press("tab")
        await pilot.press("A", " ", "c", "o", "o", "l", " ", "d", "e", "s", "c", "r", "i", "p", "t", "i", "o", "n")
        await pilot.press("tab")
        await pilot.press("M", "e")
        await pilot.click("#next")
        await pilot.click("#continue")
        await pilot.press("backspace")
        await pilot.press("tab")
        await pilot.press(*str(tmpdir))
        await pilot.click("#finish")
        pilot.app.get_widget_by_id("close_screen").remove_class("hide")
        await pilot.pause()
        await pilot.click("#close_screen")

    assert snap_compare("../nf_core/pipelines/create/__init__.py", terminal_size=(100, 50), run_before=run_before)


def test_github_details(tmpdir, snap_compare):
    """Test snapshot for the github_repo screen.
    Steps to get to this screen:
        screen welcome > press start >
        screen choose_type > press nf-core >
        screen basic_details > enter pipeline details > press next >
        screen type_nfcore > press continue >
        screen final_details > press finish > close logging screen >
        screen github_repo_question > press create repo >
        screen github_repo
    """

    async def run_before(pilot) -> None:
        delete = ["backspace"] * 50
        await pilot.click("#start")
        await pilot.click("#type_nfcore")
        await pilot.click("#name")
        await pilot.press("m", "y", "p", "i", "p", "e", "l", "i", "n", "e")
        await pilot.press("tab")
        await pilot.press("A", " ", "c", "o", "o", "l", " ", "d", "e", "s", "c", "r", "i", "p", "t", "i", "o", "n")
        await pilot.press("tab")
        await pilot.press("M", "e")
        await pilot.click("#next")
        await pilot.click("#continue")
        await pilot.press("backspace")
        await pilot.press("tab")
        await pilot.press(*str(tmpdir))
        await pilot.click("#finish")
        pilot.app.get_widget_by_id("close_screen").remove_class("hide")
        await pilot.pause()
        await pilot.click("#close_screen")
        await pilot.click("#github_repo")
        await pilot.click("#gh_username")
        await pilot.press(*delete)  # delete field automatically filled using github CLI
        await pilot.press("tab")
        await pilot.press(*delete)

    assert snap_compare("../nf_core/pipelines/create/__init__.py", terminal_size=(100, 50), run_before=run_before)


def test_github_exit_message(tmpdir, snap_compare):
    """Test snapshot for the github_exit screen.
    Steps to get to this screen:
        screen welcome > press start >
        screen choose_type > press nf-core >
        screen basic_details > enter pipeline details > press next >
        screen type_nfcore > press continue >
        screen final_details > press finish > close logging screen >
        screen github_repo_question > press create repo >
        screen github_repo > press exit (close without creating a repo) >
        screen github_exit
    """

    async def run_before(pilot) -> None:
        await pilot.click("#start")
        await pilot.click("#type_nfcore")
        await pilot.click("#name")
        await pilot.press("m", "y", "p", "i", "p", "e", "l", "i", "n", "e")
        await pilot.press("tab")
        await pilot.press("A", " ", "c", "o", "o", "l", " ", "d", "e", "s", "c", "r", "i", "p", "t", "i", "o", "n")
        await pilot.press("tab")
        await pilot.press("M", "e")
        await pilot.click("#next")
        await pilot.click("#continue")
        await pilot.press("backspace")
        await pilot.press("tab")
        await pilot.press(*str(tmpdir))
        await pilot.click("#finish")
        pilot.app.get_widget_by_id("close_screen").remove_class("hide")
        await pilot.pause()
        await pilot.click("#close_screen")
        await pilot.click("#github_repo")
        await pilot.click("#exit")

    assert snap_compare("../nf_core/pipelines/create/__init__.py", terminal_size=(100, 50), run_before=run_before)
