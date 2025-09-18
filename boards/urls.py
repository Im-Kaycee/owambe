from django.urls import path, include
from .views import *

urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='board-list-create'),
    path('boards/my-boards/', UserBoardsView.as_view(), name='user-boards'),
    path('boards/<slug:board_slug>/', BoardDetailView.as_view(), name='board-detail'),
    path('boards/<slug:board_slug>/add-collaborator/', add_collaborator, name='add-collaborator'),
    path('boards/<slug:board_slug>/delete/', BoardDeleteView.as_view(), name='board-delete'),
    path('boards/<slug:board_slug>/add-style/', add_style_to_board, name='add-style-to-board'),
    path('boards/<slug:board_slug>/remove-style/', remove_style_from_board, name='remove-style-from-board'),
    path('boards/<slug:board_slug>/styles/', get_board_styles, name='get-board-styles'),
]