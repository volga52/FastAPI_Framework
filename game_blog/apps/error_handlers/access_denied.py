from fastapi import HTTPException, Request

from setting.config import TemplateResponse


async def no_access(request: Request, exc: HTTPException):
    return TemplateResponse('error_pages/page_403.jinja2',
                            {'request': request})
