import json
import os

from fastapi import APIRouter, Depends, UploadFile, HTTPException
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import StatementError
from sqlalchemy.orm import Session

from apps.authapp import User
from apps.authapp.utils import get_user_by_token
from apps.postsapp.forms import AddPostForm, UpdatePostForm
from apps.postsapp.models import Post, Comments
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
async def show_post(uuid: str, request: Request,
                    db: Session = Depends(get_db)):
    """Обработчик запроса отображение содержимого поста"""
    response_dict = await setup_user_dict(request, db)

    comments = db.query(Comments).filter(Comments.post_uid == uuid).all()
    users = [
        db.query(User).filter(User.uid == comment.owner_uid).first().username
        for comment in comments]
    response_dict['comments'] = [
        {'username': username, 'comment': comment.content} for
        username, comment in zip(users, comments)]

    try:
        post: Post = db.query(Post).filter(Post.uid == uuid).first()
    except StatementError:
        post = None

    response_dict['post'] = post
    response = TemplateResponse('blog/single-post.jinja2', response_dict)

    response.set_cookie('post_uid', post.uid)
    return response


@post_route.get('/edit/{uuid}')
@post_route.post('/edit/{uuid}')
@login_required
async def edit_post(uuid: str, request: Request,
                    db: Session = Depends(get_db)):
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


@post_route.post('/add_comment')
async def add_comment(request: Request, db: Session = Depends(get_db)):
    data = json.loads(await request.body())
    text = data.get('text')
    token = data.get('token')
    post_uid = data.get('postUid')

    if token:
        user = await get_user_by_token(token, db)
        if not user:
            raise HTTPException(status_code=403)

        comment = Comments(content=text, owner_uid=user.uid, post_uid=post_uid)
        db.add(comment)
        db.commit()
        return {'username': user.username, 'text': text}

    raise HTTPException(status_code=404)
