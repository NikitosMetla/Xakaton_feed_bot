from .feeds_repo import FeedsRepository
from .call_points_repo import CallPointsRepository
from .animals_repo import AnimalsRepository
from .volunteers_repo import VolunteersRepository
from .users_repo import UserRepository
from .calls_repo import CallsRepository
from .calls_baskets_repo import CallsBasketsRepository
from .feed_transfers_repo import FeedTransfersRepository
from .volunteer_buskets_repo import VolunteersBasketsRepository
from .feed_transfers_buskets_repo import FeedTransfersBasketsRepository
from .trasfers_albums_repo import TransfersAlbumsRepository
from .receivings_albums_repo import ReceivingAlbumsRepository

feeds_repository = FeedsRepository()
call_points_repository = CallPointsRepository()
animals_repository = AnimalsRepository()
volunteers_repository = VolunteersRepository()
users_repository = UserRepository()
calls_baskets_repository = CallsBasketsRepository()
feed_transfers_repository = FeedTransfersRepository()
transfers_albums_repository = TransfersAlbumsRepository()
receiving_albums_repository = ReceivingAlbumsRepository()
calls_repository = CallsRepository()
feed_transfers_buskets_repository = FeedTransfersBasketsRepository()


__all__ = ['feeds_repository',
           'call_points_repository',
           'animals_repository',
           'volunteers_repository',
           'users_repository',
           'calls_baskets_repository',
           'feed_transfers_repository',
           'transfers_albums_repository',
           'receiving_albums_repository',
           'calls_repository',
           'feed_transfers_buskets_repository']