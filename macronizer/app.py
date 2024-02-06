"""
Falcon app.
"""

import dataclasses
import typing as t

import falcon  # type: ignore

from macronizer.cgi import create_html_page


class IndexResource:
    """Show the original Latin Macronizer web page."""

    @dataclasses.dataclass
    class Params:
        do_macronize: bool = True
        also_maius: bool = False
        scan: int = 0
        i_to_j: bool = False
        u_to_v: bool = False
        do_evaluate: bool = False

        @classmethod
        def from_form(cls, form: t.Mapping[str, str]) -> t.Self:
            # The form sets enabled settings to `"on"`.
            return cls(
                do_macronize=form.get("macronize", "off") == "on",
                also_maius=form.get("alsomaius", "off") == "on",
                scan=int(form.get("scan", "0")),
                i_to_j=form.get("itoj", "off") == "on",
                u_to_v=form.get("utov", "off") == "on",
                do_evaluate=form.get("doevaluate", "off") == "on",
            )

    def create_html(self, text: str, params: Params) -> str:
        """Generate the HTML page."""

        return create_html_page(
            scriptname="/",
            texttomacronize=text,
            domacronize=params.do_macronize,
            alsomaius=params.also_maius,
            scan=params.scan,
            performitoj=params.i_to_j,
            performutov=params.u_to_v,
            doevaluate=params.do_evaluate,
        )

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        text = ""
        params = self.Params()

        resp.text = self.create_html(text, params)
        resp.content_type = falcon.MEDIA_HTML
        resp.status = falcon.HTTP_200

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        form = req.media
        text = form.get("textcontent", "")
        params = self.Params.from_form(form)

        resp.text = self.create_html(text, params)
        resp.content_type = falcon.MEDIA_HTML
        resp.status = falcon.HTTP_200


def create_app() -> falcon.App:
    app = falcon.App()

    app.add_route("/", IndexResource())  # type: ignore

    return app
