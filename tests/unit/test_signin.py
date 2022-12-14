from src.models.repositories import AppUserRepository
from app import app
import pytest
import os
from flask import Flask




def test_create_user_no_input():
    new_user = AppUserRepository.AppUserRepository()
    new_user.create_user('john',None,)

    assert new_user.check_if_user_exists_by_username('john').director == None

def test_create_user_success():
    new_user = AppUserRepository.AppUserRepository()
    new_user.create_user('john',12345678,)

    print(new_user.check_if_user_exists_by_username('john').username)
    assert new_user.check_if_user_exists_by_username('john').username == True