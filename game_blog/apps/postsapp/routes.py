import os

from fastapi import APIRouter, Depends, UploadFile
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import StatementError
from sqlalchemy.orm import Session

from apps.postsapp.forms import AddPostForm, UpdatePostForm
from apps.postsapp.models import Post
from core.decorators import login_required
from core.requests_framework import setup_user_dict
from database.session import get_db
from setting.config import TemplateResponse, MEDIA_URL

post_route = APIRouter(prefix='/blog')


@post_route.get('/')
async def all_post(request: Request, db: Session = Depends(get_db)):
    """Обработчик запроса вывод всех постов"""
    request.name = 'blog'
    response_dict = await setup_user_dict(request, db)
    posts = db.query(Post).order_by(Post.created_date.desc()).all()

    response_dict['posts'] = posts

    return TemplateResponse('blog/blog.jinja2', response_dict)


@post_route.get('/add_post/')
@post_route.post('/add_post/')
@login_required
async def create_post(request: Request, db: Session = Depends(get_db)):
    """Обработчик запроса создание поста"""
    request.name = 'add_post'
    response_dict = await setup_user_dict(request, db)

    if request.method == 'POST':
        form = AddPostForm(request, context=response_dict)

        is_created = await form.create_post(db)
        if is_created:
            response_dict.update({'success': True})
        else:
            form.errors = [form.errors[0]]
            response_dict.update(form.__dict__)

    return TemplateResponse('blog/create_post.jinja2', response_dict)


@post_route.get('/single/{uuid}')
async def show_post(uuid: str, request: Request, db: Session = Depends(get_db)):
    """Обработчик запроса отображение содержимого поста"""
    response_dict = await setup_user_dict(request, db)
    try:
        post = db.query(Post).filter(Post.uid == uuid).first()
    except StatementError:
        post = None

    response_dict['post'] = post

    return TemplateResponse('blog/single-post.jinja2', response_dict)


@post_route.get('/edit/{uuid}')
@post_route.post('/edit/{uuid}')
@login_required
async def edit_post(uuid: str, request: Request, db: Session = Depends(get_db)):
    """Контроллер запроса редактирования поста"""
    response_dict = await setup_user_dict(request, db)
    try:
        post = db.query(Post).filter(Post.uid == uuid).first()
    except StatementError:
        return RedirectResponse(request.headers.get('referer'))

    response_dict['post'] = post

    if request.method == 'POST':
        form = UpdatePostForm(request, response_dict)
        was_updated = await form.update_post(db, post)
        print(was_updated)
        if was_updated:
            response_dict.update({'success': True})
        else:
            form.errors = [form.errors[0]]
            response_dict.update(form.__dict__)

    return TemplateResponse('blog/edit-post.jinja2', response_dict)


@post_route.get('/remove/{uuid}')
@login_required
async def remove_post(uuid: str, request: Request,
                      db: Session = Depends(get_db)):
    """Контроллер запроса удаления поста"""
    response_dict = await setup_user_dict(request, db)
    try:
        post = db.query(Post).filter(Post.uid == uuid).first()
    except StatementError:
        post = None

    user = response_dict.get('user')

    if user == post.owner:
        db.delete(post)
        db.commit()
        return RedirectResponse('/blog/')

    return RedirectResponse(request.headers.get('referer'))
