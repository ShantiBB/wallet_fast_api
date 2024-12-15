from typing import Any
from decimal import Decimal

from starlette import status
from fastapi import HTTPException


def valid_exist_obj(obj: Any) -> None:
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Объект не найден в базе.'
        )


def valid_title_description(
        cur_title: str,
        new_title: str,
        cur_description: str,
        new_description: str
) -> None:
    if cur_title == new_title and cur_description == new_description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Требуется внести изменения.'
        )
    elif not new_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Название кошелька не может быть пустым.'
        )
    elif len(new_title) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Название кошелька не может превышать 100 символов.'
        )
    elif new_description and len(new_description) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Описание кошелька не может превышать 255 символов.'
        )


def valid_operation_type(operation_type: str) -> None:
    if operation_type not in ('deposit', 'withdraw'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Неверный тип операции.'
        )


def valid_balance(
        operation_type: str,
        amount: Decimal,
        balance: Decimal
) -> None:
    if operation_type == 'withdraw' and amount > balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Недостаточно средств.'
        )
    elif amount < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Сумма перевода не может быть меньше 10р.'
        )

    elif amount > 10000000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Сумма перевода не может превышать 10,000,000р.'
        )
