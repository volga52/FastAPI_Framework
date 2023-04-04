from fastapi import HTTPException, Request

from setting.config import TemplateResponse


async def server_error(request: Request, exc: HTTPException):
    return TemplateResponse('error_pages/page_500.jinja2',
                            {'request': request})
