# -*- coding: utf-8 -*-

import json
from copy import deepcopy
from pathlib import Path

import pytest
import requests

from micropy import main, project


@pytest.fixture
def mock_requests(mocker, requests_mock, test_archive):
    mock_source = {
        "name": "Micropy Stubs",
        "location": "https://codeload.github.com/BradenM/micropy-stubs",
        "source": "https://raw.githubusercontent.com/bradenm/micropy-stubs/source.json",
        "path": "legacy.tar.gz/pkg/",
        "packages": [
            {
                "name": "micropython",
                "type": "firmware",
                "sha256sum": "7ff2cce0237268cd52164b77b6c2df6be6249a67ee285edc122960af869b8ed2"
            },
        ]
    }
    requests_mock.get(
        "https://raw.githubusercontent.com/BradenM/micropy-stubs/master/source.json",
        json=mock_source)
    requests_mock.get(
        "https://codeload.github.com/BradenM/micropy-stubs/legacy.tar.gz/pkg/micropython",
        content=test_archive)


@pytest.fixture
def mock_cwd(tmp_path, mocker):
    import pathlib
    mocker.patch('pathlib.Path.cwd')
    pathlib.Path.return_value = tmp_path
    pathlib.Path.cwd.return_value = tmp_path
    return tmp_path


@pytest.mark.usefixtures("mock_pkg", "mock_requests")
@pytest.mark.incremental
class TestCreateProject:
    mp = None

    expect_mp_data = {
        'name': 'NewProject',
        'stubs': {
            'esp32-1.11.0': '1.2.0'
        },
        'packages': {},
        'dev-packages': {
            'micropy-cli': '*'
        },
        'config': {
            'vscode': True,
            'pylint': True
        }
    }

    expect_vsc_data = [
        str(Path(".micropy/esp32_test_stub/frozen")),
        str(Path(".micropy/esp32_test_stub/stubs")),
        str(Path(".micropy/NewProject"))
    ]

    @pytest.fixture
    def new_project(self, mock_cwd, mock_micropy, shared_datadir, tmp_path,  utils):
        stub_path = (shared_datadir / 'esp32_test_stub')
        return self.build_project(mock_micropy, tmp_path, [stub_path])

    def build_project(self, mpy, path, stub_paths):
        for stub in stub_paths:
            mpy.stubs.add(stub)
        proj_path = path / 'NewProject'
        proj = project.Project(proj_path)
        proj_stub = list(mpy.stubs)[0]
        proj.add(project.modules.StubsModule, mpy.stubs, stubs=[proj_stub])
        proj.add(project.modules.PackagesModule, 'requirements.txt')
        proj.add(project.modules.DevPackagesModule, 'dev-requirements.txt')
        proj.add(project.modules.TemplatesModule, ('vscode', 'pylint'))
        return (proj, mpy)

    def check_mp_data(self, path, expect=None):
        expect_data = expect or self.expect_mp_data
        micropy_file = path
        assert micropy_file.exists()
        mp_data = json.loads(micropy_file.read_text())
        assert mp_data.items() == expect_data.items()

    def check_vscode(self, path, expect=None):
        vsc_path = path / '.vscode' / 'settings.json'
        assert vsc_path.exists()
        with vsc_path.open() as f:
            lines = [l.strip() for l in f.readlines() if l]
            valid = [l for l in lines if "//" not in l[:2]]
        vsc_data = json.loads("\n".join(valid))
        expect_data = expect or self.expect_vsc_data
        assert vsc_data['python.analysis.typeshedPaths'] == expect_data

    def test_setup_stubs(self, mock_micropy, get_stub_paths, shared_datadir):
        mpy = mock_micropy
        stub_path = (shared_datadir / 'esp32_test_stub')
        mpy.stubs.add(stub_path)

    def test_create_project(self, new_project):
        proj, mpy = new_project
        proj.create()
        self.check_mp_data(proj.info_path)
        self.check_vscode(proj.path)
        # Reload micropy project and check again
        proj = mpy.resolve_project(proj.path)
        self.check_mp_data(proj.info_path)
        self.check_vscode(proj.path)

    def test_add_package(self, new_project, mock_pkg):
        proj, mpy = new_project
        proj.create()
        proj.add_package("newpackage")
        expect_data = deepcopy(self.expect_mp_data)
        expect_data['packages']['newpackage'] = '*'
        self.check_mp_data(proj.info_path, expect=expect_data)

    @pytest.mark.parametrize('local_pkg', ['src/lib/coolpackage', '/tmp/absolute/package'])
    def test_add_local_package(self, new_project, tmp_path, local_pkg, utils):
        proj, mpy = new_project
        proj.create()
        local_package = Path(local_pkg)
        if not local_package.is_absolute():
            local_package = (proj.path / Path(local_pkg))
        local_package.mkdir(parents=True, exist_ok=True)
        (local_package / '__init__.py').touch()
        local_path = utils.str_path(local_pkg)
        proj.add_package(f"-e {local_path}")
        proj.load()
        # check micropy.json
        expect_data = deepcopy(self.expect_mp_data)
        expect_data['packages'][local_package.name] = f'-e {local_path}'
        self.check_mp_data(proj.info_path, expect=expect_data)
        # check vscode settings
        expect_vscode = deepcopy(self.expect_vsc_data)
        expect_vscode.append(local_path)
        self.check_vscode(proj.path, expect=expect_vscode)
