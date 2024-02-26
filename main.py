from fastui.forms import fastui_form
import uvicorn
from app.models import EachParty
from app.crud import get_lga_results_from_not_announced_lga_results
from app.models import SelectForm, BigModel, EachPartyResultInEachPolingUnit
from fastui.forms import fastui_form
from typing import Annotated
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.crud import get_all_polling_units_from_polling_units_table, get_particular_polling_units_from_announced_pu_results_table, compile_all_polling_unit_results_for_a_local_govenrnment
from fastui import AnyComponent, FastUI, components as c, prebuilt_html
from fastui.components.display import DisplayLookup
from fastui.events import GoToEvent, BackEvent

app = FastAPI()

polling_units = get_all_polling_units_from_polling_units_table()

polling_unit_id_to_party_results_mapping, pu_that_are_under_an_lga, lga_name_to_lga_id_mapping = get_lga_results_from_not_announced_lga_results()

lga_party_results = compile_all_polling_unit_results_for_a_local_govenrnment(
    polling_unit_id_to_party_results_mapping, pu_that_are_under_an_lga)

navbar = c.Navbar(
    title='Bincom X INEC',
    title_event=GoToEvent(url='/'),
    links=[
        c.Link(
            components=[c.Text(text='Polling Units Results')],
            on_click=GoToEvent(url='/polling-units/'),
            active='startswith:/polling-units',
        ),

        c.Link(
            components=[c.Text(text="LGA Results")],
            on_click=GoToEvent(url="/lga-results/"),
            active='startswith:/lga-results'
        ),

        c.Link(
            components=[c.Text(text='Store Polling Unit Results')],
            on_click=GoToEvent(url='/new-polling-unit/'),
            active='startswith:/new-polling-unit',
        )
    ]
)

# base url


@app.get(path="/api/", response_model=FastUI, response_model_exclude_none=True)
def index():
    return [
        c.PageTitle(text="Home Page"),
        navbar,
        c.Page(
            components=[
                c.Heading(text="Nigerian Elections", level=2),
                c.Paragraph(
                    text='If you want to check election results, you are in the right place'),

                c.Image(
                    src='http://www.nigerianembassy.co.il/wp-content/uploads/2019/04/flag-500x302.jpg',
                    alt='Nigerian Flag',
                    width=828,
                    height=500,
                    loading='lazy',
                    referrer_policy='no-referrer',
                    class_name='border rounded',
                ),
            ],

        )
    ]


@app.get("/api/polling-units/", response_model=FastUI, response_model_exclude_none=True)
def users_table() -> list[AnyComponent]:
    """
    Show a table of four users, `/api` is the endpoint the frontend will connect to
    when a user visits `/` to fetch components to render.
    """
    return [
        navbar,
        c.Page(
            components=[
                c.Heading(text='Polling Units', level=1),
                c.Table(
                    data=polling_units,
                    columns=[
                        DisplayLookup(
                            field='uniqueid', on_click=GoToEvent(url='/polling-units/polling-unit/{uniqueid}/')),
                        DisplayLookup(field='polling_unit_name'),
                    ],
                ),
            ]
        ),
    ]


@app.get("/api/polling-units/polling-unit/{uniqueid}/", response_model=FastUI, response_model_exclude_none=True)
def user_profile(uniqueid: str) -> list[AnyComponent]:
    """
    User profile page, the frontend will fetch this when the user visits `/user/{id}/`.
    """
    particular_polling_unit_results = get_particular_polling_units_from_announced_pu_results_table(
        uniqueid)

    dicti = []
    for each_particular_pu_results in particular_polling_unit_results:
        dicti.append(EachPartyResultInEachPolingUnit(
            party=each_particular_pu_results.party_abbreviation.strip(), result=each_particular_pu_results.party_score))

    return [
        navbar,
        c.Page(
            components=[
                c.Heading(text='Polling Units with Uniqueid', level=3),
                c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),

                c.Table(
                    data=dicti,
                    columns=[
                        DisplayLookup(field='party'),
                        DisplayLookup(field='result')
                    ],
                ),
            ]
        ),
    ]


8888


@app.get(path="/api/lga-results/", response_model=FastUI, response_model_exclude_none=True)
async def select_form_post():
    return [
        navbar,
        c.Page(
            components=[
                c.Heading(text='Select LGA', level=2),
                c.Paragraph(
                    text='Please select one local government.'),
                c.ModelForm(model=SelectForm, display_mode='default',
                            submit_url='/api/lga-results/submit'),
            ]
        )
    ]


@app.post(path="/api/lga-results/submit", response_model=FastUI, response_model_exclude_none=True)
async def select_form_post(form: Annotated[SelectForm, fastui_form(SelectForm)]):
    return [c.FireEvent(event=GoToEvent(url=f'/lga-results/{form.select_single.value}/'))]


@app.get(path="/api/lga-results/{lga_name}/", response_model=FastUI, response_model_exclude_none=True)
async def get_particular_lga_result(lga_name: str):
    lga_id = lga_name_to_lga_id_mapping[lga_name]
    res = lga_party_results[lga_id]
    leg = {}
    for each_key in res:
        leg[each_key.strip()] = res[each_key]
    del res
    usss = EachParty.model_validate(leg)
    return [
        navbar,
        c.Page(
            components=[
                c.Heading(text=lga_name, level=2),
                c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
                c.Details(data=usss)
            ]
        ),
    ]


@app.get(path="/api/new-polling-unit", response_model=FastUI, response_model_exclude_none=True)
async def new_polling_unit():
    return [
        navbar,
        c.Page(
            components=[
                c.Heading(text='Enter Details of new Polling Unit', level=2),
                c.ModelForm(model=BigModel, display_mode='default',
                            submit_url='/api/new-polling-unit/submit'),
            ]
        )
    ]


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='Bincom Interview Test'))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
