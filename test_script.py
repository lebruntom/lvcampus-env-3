import pytest
import subprocess
from script import (is_docker_installed, is_virtualbox_installed, 
                          is_docker_active, create_vbox_vm, create_container, 
                          install_ssh)

# 1. Mock subprocess.run for testing if Docker is installed
def test_is_docker_installed(monkeypatch):
    def mock_run(*args, **kwargs):
        class MockCompletedProcess:
            returncode = 0
        return MockCompletedProcess()
    
    monkeypatch.setattr(subprocess, "run", mock_run)
    assert is_docker_installed() is True

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: (_ for _ in ()).throw(FileNotFoundError))
    assert is_docker_installed() is False

# 2. Mock subprocess.run for testing if VirtualBox is installed
def test_is_virtualbox_installed(monkeypatch):
    def mock_run(*args, **kwargs):
        class MockCompletedProcess:
            returncode = 0
        return MockCompletedProcess()
    
    monkeypatch.setattr(subprocess, "run", mock_run)
    assert is_virtualbox_installed() is True

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: (_ for _ in ()).throw(FileNotFoundError))
    assert is_virtualbox_installed() is False

def test_is_docker_active(monkeypatch):
    def mock_run(*args, **kwargs):
        class MockCompletedProcess:
            returncode = 0
        return MockCompletedProcess()
    
    monkeypatch.setattr(subprocess, "run", mock_run)
    assert is_docker_active() is True

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: (_ for _ in ()).throw(subprocess.CalledProcessError(1, 'command')))
    assert is_docker_active() is False

# 4. Test the creation of a VirtualBox VM
def test_create_vbox_vm(monkeypatch):
    run_count = 0

    def mock_run(*args, **kwargs):
        nonlocal run_count
        run_count += 1
        class MockCompletedProcess:
            returncode = 0
        return MockCompletedProcess()
    
    monkeypatch.setattr(subprocess, "run", mock_run)
    
    iso_path = "/path/to/iso"
    create_vbox_vm("TestVM", iso_path)
    
    assert run_count > 0  

# 5. Test the creation of a Docker container
def test_create_container(monkeypatch):
    run_count = 0

    def mock_run(*args, **kwargs):
        nonlocal run_count
        run_count += 1
        class MockCompletedProcess:
            returncode = 0
        return MockCompletedProcess()
    
    monkeypatch.setattr(subprocess, "run", mock_run)

    user_inputs = iter(['1', 'n']) 
    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))

    create_container()


    assert run_count > 0  
# 6. Test the installation of SSH in a Docker container
def test_install_ssh(monkeypatch):
    run_count = 0

    def mock_run(*args, **kwargs):
        nonlocal run_count
        run_count += 1
        class MockCompletedProcess:
            returncode = 0
        return MockCompletedProcess()
    
    monkeypatch.setattr(subprocess, "run", mock_run)

    install_ssh("test_container", "ubuntu")
    
    assert run_count > 0  
