import collections.abc
import google.protobuf.message
import modal._resolver
import modal.client
import typing
import typing_extensions

O = typing.TypeVar("O", bound="_Object")

_BLOCKING_O = typing.TypeVar("_BLOCKING_O", bound="Object")

def _get_environment_name(
    environment_name: typing.Optional[str] = None, resolver: typing.Optional[modal._resolver.Resolver] = None
) -> typing.Optional[str]: ...

class _Object:
    _type_prefix: typing.ClassVar[typing.Optional[str]]
    _prefix_to_type: typing.ClassVar[dict[str, type]]
    _load: typing.Optional[
        typing.Callable[[O, modal._resolver.Resolver, typing.Optional[str]], collections.abc.Awaitable[None]]
    ]
    _preload: typing.Optional[
        typing.Callable[[O, modal._resolver.Resolver, typing.Optional[str]], collections.abc.Awaitable[None]]
    ]
    _rep: str
    _is_another_app: bool
    _hydrate_lazily: bool
    _deps: typing.Optional[typing.Callable[..., list[_Object]]]
    _deduplication_key: typing.Optional[typing.Callable[[], collections.abc.Awaitable[collections.abc.Hashable]]]
    _object_id: str
    _client: modal.client._Client
    _is_hydrated: bool
    _is_rehydrated: bool

    @classmethod
    def __init_subclass__(cls, type_prefix: typing.Optional[str] = None): ...
    def __init__(self, *args, **kwargs): ...
    def _init(
        self,
        rep: str,
        load: typing.Optional[
            typing.Callable[[O, modal._resolver.Resolver, typing.Optional[str]], collections.abc.Awaitable[None]]
        ] = None,
        is_another_app: bool = False,
        preload: typing.Optional[
            typing.Callable[[O, modal._resolver.Resolver, typing.Optional[str]], collections.abc.Awaitable[None]]
        ] = None,
        hydrate_lazily: bool = False,
        deps: typing.Optional[typing.Callable[..., list[_Object]]] = None,
        deduplication_key: typing.Optional[
            typing.Callable[[], collections.abc.Awaitable[collections.abc.Hashable]]
        ] = None,
    ): ...
    def _unhydrate(self): ...
    def _initialize_from_empty(self): ...
    def _initialize_from_other(self, other): ...
    def _hydrate(
        self, object_id: str, client: modal.client._Client, metadata: typing.Optional[google.protobuf.message.Message]
    ): ...
    def _hydrate_metadata(self, metadata: typing.Optional[google.protobuf.message.Message]): ...
    def _get_metadata(self) -> typing.Optional[google.protobuf.message.Message]: ...
    def _validate_is_hydrated(self: O): ...
    def clone(self: O) -> O: ...
    @classmethod
    def _from_loader(
        cls,
        load: typing.Callable[[O, modal._resolver.Resolver, typing.Optional[str]], collections.abc.Awaitable[None]],
        rep: str,
        is_another_app: bool = False,
        preload: typing.Optional[
            typing.Callable[[O, modal._resolver.Resolver, typing.Optional[str]], collections.abc.Awaitable[None]]
        ] = None,
        hydrate_lazily: bool = False,
        deps: typing.Optional[typing.Callable[..., collections.abc.Sequence[_Object]]] = None,
        deduplication_key: typing.Optional[
            typing.Callable[[], collections.abc.Awaitable[collections.abc.Hashable]]
        ] = None,
    ): ...
    @classmethod
    def _get_type_from_id(cls: type[O], object_id: str) -> type[O]: ...
    @classmethod
    def _is_id_type(cls: type[O], object_id) -> bool: ...
    @classmethod
    def _new_hydrated(
        cls: type[O],
        object_id: str,
        client: modal.client._Client,
        handle_metadata: typing.Optional[google.protobuf.message.Message],
        is_another_app: bool = False,
    ) -> O: ...
    def _hydrate_from_other(self, other: O): ...
    def __repr__(self): ...
    @property
    def local_uuid(self): ...
    @property
    def object_id(self) -> str: ...
    @property
    def is_hydrated(self) -> bool: ...
    @property
    def deps(self) -> typing.Callable[..., list[_Object]]: ...
    async def resolve(self, client: typing.Optional[modal.client._Client] = None): ...

class Object:
    _type_prefix: typing.ClassVar[typing.Optional[str]]
    _prefix_to_type: typing.ClassVar[dict[str, type]]
    _load: typing.Optional[
        typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Optional[str]], collections.abc.Awaitable[None]]
    ]
    _preload: typing.Optional[
        typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Optional[str]], collections.abc.Awaitable[None]]
    ]
    _rep: str
    _is_another_app: bool
    _hydrate_lazily: bool
    _deps: typing.Optional[typing.Callable[..., list[Object]]]
    _deduplication_key: typing.Optional[typing.Callable[[], collections.abc.Awaitable[collections.abc.Hashable]]]
    _object_id: str
    _client: modal.client.Client
    _is_hydrated: bool
    _is_rehydrated: bool

    def __init__(self, *args, **kwargs): ...
    @classmethod
    def __init_subclass__(cls, type_prefix: typing.Optional[str] = None): ...

    class ___init_spec(typing_extensions.Protocol):
        def __call__(
            self,
            rep: str,
            load: typing.Optional[
                typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Optional[str]], None]
            ] = None,
            is_another_app: bool = False,
            preload: typing.Optional[
                typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Optional[str]], None]
            ] = None,
            hydrate_lazily: bool = False,
            deps: typing.Optional[typing.Callable[..., list[Object]]] = None,
            deduplication_key: typing.Optional[typing.Callable[[], collections.abc.Hashable]] = None,
        ): ...
        def aio(
            self,
            rep: str,
            load: typing.Optional[
                typing.Callable[
                    [_BLOCKING_O, modal._resolver.Resolver, typing.Optional[str]], collections.abc.Awaitable[None]
                ]
            ] = None,
            is_another_app: bool = False,
            preload: typing.Optional[
                typing.Callable[
                    [_BLOCKING_O, modal._resolver.Resolver, typing.Optional[str]], collections.abc.Awaitable[None]
                ]
            ] = None,
            hydrate_lazily: bool = False,
            deps: typing.Optional[typing.Callable[..., list[Object]]] = None,
            deduplication_key: typing.Optional[
                typing.Callable[[], collections.abc.Awaitable[collections.abc.Hashable]]
            ] = None,
        ): ...

    _init: ___init_spec

    def _unhydrate(self): ...
    def _initialize_from_empty(self): ...
    def _initialize_from_other(self, other): ...
    def _hydrate(
        self, object_id: str, client: modal.client.Client, metadata: typing.Optional[google.protobuf.message.Message]
    ): ...
    def _hydrate_metadata(self, metadata: typing.Optional[google.protobuf.message.Message]): ...
    def _get_metadata(self) -> typing.Optional[google.protobuf.message.Message]: ...
    def _validate_is_hydrated(self: _BLOCKING_O): ...
    def clone(self: _BLOCKING_O) -> _BLOCKING_O: ...
    @classmethod
    def _from_loader(
        cls,
        load: typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Optional[str]], None],
        rep: str,
        is_another_app: bool = False,
        preload: typing.Optional[
            typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Optional[str]], None]
        ] = None,
        hydrate_lazily: bool = False,
        deps: typing.Optional[typing.Callable[..., collections.abc.Sequence[Object]]] = None,
        deduplication_key: typing.Optional[typing.Callable[[], collections.abc.Hashable]] = None,
    ): ...
    @classmethod
    def _get_type_from_id(cls: type[_BLOCKING_O], object_id: str) -> type[_BLOCKING_O]: ...
    @classmethod
    def _is_id_type(cls: type[_BLOCKING_O], object_id) -> bool: ...
    @classmethod
    def _new_hydrated(
        cls: type[_BLOCKING_O],
        object_id: str,
        client: modal.client.Client,
        handle_metadata: typing.Optional[google.protobuf.message.Message],
        is_another_app: bool = False,
    ) -> _BLOCKING_O: ...
    def _hydrate_from_other(self, other: _BLOCKING_O): ...
    def __repr__(self): ...
    @property
    def local_uuid(self): ...
    @property
    def object_id(self) -> str: ...
    @property
    def is_hydrated(self) -> bool: ...
    @property
    def deps(self) -> typing.Callable[..., list[Object]]: ...

    class __resolve_spec(typing_extensions.Protocol):
        def __call__(self, client: typing.Optional[modal.client.Client] = None): ...
        async def aio(self, client: typing.Optional[modal.client.Client] = None): ...

    resolve: __resolve_spec

def live_method(method): ...
def live_method_gen(method): ...

EPHEMERAL_OBJECT_HEARTBEAT_SLEEP: int
