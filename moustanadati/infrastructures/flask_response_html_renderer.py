# infrastructures/flask_response_html_renderer.py

from flask import render_template, Response, make_response, redirect

from interfaces.renderer_interface import IRenderer
from interfaces.renderer_interface import RenderResult
from interfaces.view_model_interface import IViewModel

class FlaskResponseHTMLRenderer(IRenderer):
    def render(self, viewmodel: IViewModel, template_name: str | None = None) -> RenderResult:
        if viewmodel.redirect_to:
            return RenderResult(redirect_to=viewmodel.redirect_to)

        body = render_template(template_name, **viewmodel.to_dict()) if template_name else ""
        return RenderResult(
            body=body,
            status_code=200,
            headers=viewmodel.headers
        )

    def to_flask_response(self, result: RenderResult) -> Response:
       

        if result.redirect_to:
            response = redirect(result.redirect_to)
        else:
            response = make_response(result.body, result.status_code)

        for k, v in result.headers.items():
            response.headers[k] = v

        return response
