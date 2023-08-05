from dataclasses import dataclass, field
from typing import List, Dict, Any, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session


@dataclass
class CreateEngineArgs(object):
    args: List = field(default_factory=list)
    kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SessionMakerArgs(object):
    session_class: Type = Session
    autoflush: bool = True
    autocommit: bool = False
    expire_on_commit: bool = True
    info: Dict = None
    kwargs: Dict[str, Any] = field(default_factory=dict)


class ProcessSafeSessionFactory(object):
    def __init__(self,
                 db_path: str,
                 create_engine_args: CreateEngineArgs = None,
                 session_maker_args: SessionMakerArgs = None):

        self._db_path = db_path

        self._create_engine_args = create_engine_args if create_engine_args is not None else CreateEngineArgs()
        self._session_maker_args = session_maker_args if session_maker_args is not None else SessionMakerArgs()

        self._thread_safe_session_factory = None

    def _initialize(self):
        db_engine = create_engine(self._db_path,
                                  *self._create_engine_args.args,
                                  **self._create_engine_args.kwargs)

        session_factory = sessionmaker(bind=db_engine,
                                       class_=self._session_maker_args.session_class,
                                       autoflush=self._session_maker_args.autoflush,
                                       autocommit=self._session_maker_args.autocommit,
                                       expire_on_commit=self._session_maker_args.expire_on_commit,
                                       info=self._session_maker_args.info,
                                       **self._session_maker_args.kwargs)

        self._thread_safe_session_factory = scoped_session(session_factory)

    def __call__(self, *args, **kwargs):
        if self._thread_safe_session_factory is None:
            self._initialize()

        return self._thread_safe_session_factory(*args, **kwargs)
