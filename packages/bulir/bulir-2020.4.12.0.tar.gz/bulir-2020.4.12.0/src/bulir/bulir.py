#!/usr/bin/env python3
"""Provides a retriever to obtain Brazilian UFs' first and second
instances lawsuit identifications using Jusbrasil as its data source."""
import asyncio
import logging
import os
import subprocess
import random
import re
from datetime import date, datetime, timedelta
from functools import partial
from pathlib import Path
from typing import Any, Iterable, Optional, SupportsInt, Tuple, Union

import cfscrape
import asyncclick as click
from lxml import html
from yarl import URL


with (Path(__file__).parent / "VERSION").open("rt") as VERSION:
    __version__ = VERSION.read().strip()


# Validate if NodeJS is available and has minimum version required
try:
    NODE_RUN = subprocess.run(["node", "-v"], capture_output=True, text=True,)
except Exception:
    raise RuntimeError("NodeJS was not detected")
if NODE_RUN.returncode:
    raise RuntimeError("NodeJS version could not be obtained")
try:
    NODE_VERSION_TUPLE = NODE_RUN.stdout.strip().replace("v", "").split(".")
    if len(NODE_VERSION_TUPLE) < 2:
        raise ValueError("Unexpected NodeJS version numbering")
except Exception:
    raise RuntimeError("Unable to retrieve NodeJS version")
try:
    if int(NODE_VERSION_TUPLE[0]) < 10:
        raise ValueError("NodeJS minimum version not attended")
except Exception:
    raise ValueError("NodeJS minimum version not attended")


# Important setting to asyncclick
click.anyio_backend = "asyncio"


# Log level setting
LOGLEVEL = "NOTSET"
if "LOGLEVEL" in os.environ:
    try:
        VALUE = os.environ["LOGLEVEL"].upper()
        if VALUE not in (
            "CRITICAL",
            "ERROR",
            "WARNING",
            "INFO",
            "DEBUG",
            "NOTSET",
        ):
            raise ValueError()
        LOGLEVEL = VALUE
    except Exception:
        pass
    del VALUE


# Log file setting
if "LOGFILE" in os.environ:
    try:
        logging.basicConfig(filename=os.environ["LOGFILE"], level=LOGLEVEL)
    except Exception:
        logging.warning("A log file could not be created.")
        pass
logging.getLogger("asyncio").setLevel(LOGLEVEL)


BASE_URL = "https://www.jusbrasil.com.br/diarios/{uf_gazette_code}/{day}"
_JUSBRASIL_GAZETTES_PARTIAL_URLs = [
    "Caderno",
    "Edicao",
    "Judiciario",
    "Secao",
    "Suplemento",
    "Tribunal",
    "-comarcas",
    "-entrancia",
    "-grau",
    "-inst",
    "-recursos",
    "-sem-caderno",
    "-vara",
    "Abaete",
    "Acucena",
    "Aiuruoca",
    "Alfenas",
    "Almenara",
    "Alto-rio-doce",
    "Andradas",
    "Andrelandia",
    "Aracuai",
    "Araguari",
    "Araxa",
    "Arcos",
    "Areado",
    "Arinos",
    "Baependi",
    "Bambui",
    "Barbacena",
    "Belo-horizonte",
    "Belo-vale",
    "Betim",
    "Bicas",
    "Boa-esperanca",
    "Bocaiuva",
    "Bom-despacho",
    "Bom-sucesso",
    "Bonfim",
    "Bonfinopolis-de-minas",
    "Botelhos",
    "Brasilia-de-minas",
    "Brumadinho",
    "Bueno-brandao",
    "Buenopolis",
    "Buritis",
    "Cabo-verde",
    "Caete",
    "Camanducaia",
    "Cambui",
    "Campina-verde",
    "Campo-belo",
    "Campos-altos",
    "Campos-gerais",
    "Canapolis",
    "Candeias",
    "Capelinha",
    "Capinopolis",
    "Carandai",
    "Carangola",
    "Caratinga",
    "Carlos-chagas",
    "Carmo-de-minas",
    "Carmo-do-paranaiba",
    "Carmo-do-rio-claro",
    "Carmopolis-de-minas",
    "Cassia",
    "Cataguases",
    "Caxambu",
    "Claudio",
    "Conceicao-do-rio-verde",
    "Conceicao-mato-dentro",
    "Congonhas",
    "Conselheiro-lafaiete",
    "Conselheiro-pena",
    "Corinto",
    "Coronel-fabriciano",
    "Cristina",
    "Cruzilia",
    "Curvelo",
    "Diamantina",
    "Divino",
    "Divinopolis",
    "Dores-do-indaia",
    "Editais",
    "Ervalia",
    "Esmeraldas",
    "Espera-feliz",
    "Estrela-do-sul",
    "Eugenopolis",
    "Extrema",
    "Ferros",
    "Formiga",
    "Francisco-sa",
    "Frutal",
    "Governador-valadares",
    "Grao-mogol",
    "Guanhaes",
    "Guape",
    "Guaxupe",
    "Ibia",
    "Ibiraci",
    "Ibirite",
    "Igarape",
    "Iguatama",
    "Inhapim",
    "Ipanema",
    "Ipatinga",
    "Itabira",
    "Itaguara",
    "Itajuba",
    "Itamarandiba",
    "Itambacuri",
    "Itamoji",
    "Itamonte",
    "Itanhandu",
]
# Probably some entries related to MG could be missing.


_BRAZILIAN_LAWSUIT_ID_FORMAT = (
    r"(?P<full_lawsuit_id>"  # full lawsuit id
    r"(?P<numeroDigitoAnoUnificado>"  # first group to extract query parameter
    r"[0-9]{7}"  # process order number in its original court
    r"-"
    r"[0-9]{2}"  # check digits
    r"\."
    r"[0-9]{4}"  # assessment initial year
    r")"  # end of first group
    r"\."
    r"(?P<JTRNumeroUnificado>"  # second group to validate query parameter
    r"[1-9]"  # original judiciary segment
    r"\."
    r"[0-9]{2}"  # court id within segment
    r")"  # end of second group
    r"\."
    r"(?P<foroNumeroUnificado>"  # third group to extract query parameter
    r"[0-9]{4}"  # original court unit id
    r")"  # end of third group
    r")"  # end of match
)
BRAZILIAN_LAWSUIT_ID_FORMAT = re.compile(_BRAZILIAN_LAWSUIT_ID_FORMAT)


GAZETTE_CODES = {
    "AC": "DJAC",
    "AL": "DJAL",
    "AM": "DJAM",
    "AP": "DJAP",
    "BA": "DJBA",
    "CE": "DJCE",
    "DF": "DJDF",
    "ES": "TJ-ES",
    "GO": "DJGO",
    "MA": "DJMA",
    "MG": "DJMG",
    "MS": "DJMS",
    "MT": "DJMT",
    "PA": "DJPA",
    "PB": "DJPB",
    "PE": "DJPE",
    "PI": "DJPI",
    "PR": "DJPR",
    "RJ": "DJRJ",
    "RN": "DJRN",
    "RO": "DJRO",
    "RR": "DJRR",
    "RS": "DJRS",
    "SC": "DJSC",
    "SE": "DJSE",
    "SP": "DJSP",
    "TO": "DJTO",
}


def validate_tentative_uf_code(value: str = "") -> str:
    if not isinstance(value, str):
        raise TypeError(
            f"UF code argument expected to be string. '{type(value)}' found"
        )

    if not value:
        raise ValueError(
            "UF code argument expected to be a non-zero size string"
        )

    if value.upper() not in GAZETTE_CODES:
        raise ValueError(
            f"UF code argument expected to be a valid UF code. '{value}' found"
        )

    return value.upper()


def validate_uf_codes_parameter(
    ctx: Optional[click.Context] = None,
    param: Optional[Iterable[Any]] = None,
    value: Tuple[str] = lambda: tuple(),
) -> Tuple[str]:
    valid_codes = []
    invalid_codes = []

    for tentative in value:
        try:
            valid_codes.append(validate_tentative_uf_code(tentative))
        except (TypeError, ValueError):
            invalid_codes.append(tentative)

    if invalid_codes:
        raise click.BadParameter(f"Found invalid UF code: {invalid_codes}")

    return tuple(valid_codes)


class BrazilianLawsuitIDsRetriever:

    uf_codes: Tuple[str, ...] = ()
    days_to_check: int = 0
    start_date: Union[date, datetime] = date.today()
    id_: set = set()
    lock: asyncio.Lock = asyncio.Lock()
    cfscraper: cfscrape.CloudflareScraper = None

    def __init__(
        self,
        *args,
        uf_codes: Tuple[str, ...] = None,
        days_to_check_: Union[str, bytes, SupportsInt] = 0,
        start_date_: str = "",
        **kwargs,
    ) -> None:

        start_date: Union[date, datetime] = date.today()

        if not uf_codes:
            logging.error("Parameter 'uf_codes' has zero-like value.")
            raise ValueError("No valid UF code provided")

        valid_codes = []
        for code in uf_codes:
            try:
                valid_codes.append(validate_tentative_uf_code(value=code))
            except (TypeError, ValueError):
                logging.warning("UF code '%s' is invalid. Skipping it.", code)

        if not valid_codes:
            logging.error("All UF codes provided are invalid")
            raise ValueError("No valid UF code provided")

        if not days_to_check_:
            days_to_check = 1

        try:
            days_to_check = int(days_to_check_)
        except ValueError:
            logging.warning(
                "Parameter 'days_to_check_' could not be read as int."
                " Defaulting to 1."
            )

        if days_to_check < 1:
            days_to_check = 1

        try:
            start_date = datetime.strptime(start_date_, "%Y-%m-%d")
        except Exception:
            start_date = date.today()
            logging.warning(
                "Parameter 'start-date' could not be read as"
                " 'YYYY-mm-dd' date. Defaulting to %s (today).",
                start_date.strftime("%Y-%m-%d"),
            )

        self.uf_codes = tuple(valid_codes)
        self.days_to_check = days_to_check
        self.start_date = start_date
        self.id_ = set()
        self.lock = asyncio.Lock()

    async def __aenter__(self) -> "BrazilianLawsuitIDsRetriever":
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        pass

    async def reset(self):
        """Remove all stored data."""
        async with self.lock:
            self.id_.clear()

    async def here_comes_a_new_challenge(
        self, url: Union[str, URL] = None,
    ) -> None:
        """Uses cfscrape package to tentatively solve
        Javascript challenges from Cloudflare."""

        if not url:
            chosen_uf = random.choice(self.uf_codes)
            url = BASE_URL.format(
                uf_gazette_code=GAZETTE_CODES[chosen_uf], day="",
            )

        loop = asyncio.get_running_loop()

        async with self.lock:

            if self.cfscraper:
                del self.cfscraper
                self.cfscraper = None

            self.cfscraper = await loop.run_in_executor(
                None, cfscrape.create_scraper
            )

            get = partial(self.cfscraper.get, url=url,)
            response = await loop.run_in_executor(None, get)

    async def get_text_from_url(
        self, *, url: Union[str, URL]
    ) -> Tuple[int, str]:
        """Get URL content text considering JavaScript challenges."""

        http_status_code = 0
        text = ""

        loop = asyncio.get_running_loop()

        if not self.cfscraper:
            await self.here_comes_a_new_challenge()

        retry = True
        while retry:
            while not self.cfscraper:
                await asyncio.sleep(0.01)

            get = partial(self.cfscraper.get, url=url)
            response = await loop.run_in_executor(None, get)

            http_status_code = response.status_code

            if response.ok:
                logging.info("Succesfully got from %s.", url)
                text = response.text
                retry = False
            elif http_status_code in (503, 429, 403):
                logging.info("Here comes a new Cloudflare challenge!")
                try:
                    await self.here_comes_a_new_challenge(url=url)
                except Exception:
                    logging.warning(
                        "Unable to obtain Cloudflare tokens from %s.", url,
                    )
                    http_status_code = 403
                    self.tokens = None
                    return http_status_code, text
            else:
                retry = False

        return http_status_code, text

    async def consumer_flow(
        self, *args, reset: bool = True, **kwargs
    ) -> Iterable[str]:
        """Execute full flow to retrieve data."""
        if reset:
            await self.reset()

        await self.dispatch_weekdays_requests()

        logging.info(
            "Found %d lawsuits from %s.",
            len(self.id_),
            " and ".join(self.uf_codes),
        )

        return self.id_

    async def dispatch_weekdays_requests(self) -> None:
        """Start requests related to weekdays."""
        remaining_dates = self.days_to_check
        gazettes_root_to_check = []

        # List all previous weekday dates to check gazettes.
        for uf in self.uf_codes:
            current_day = self.start_date
            while remaining_dates:
                # Skip saturdays and sundays.
                if current_day.isoweekday() in (6, 7):
                    current_day -= timedelta(days=1)
                    continue

                day = current_day.strftime("%Y/%m/%d")
                url = BASE_URL.format(
                    uf_gazette_code=GAZETTE_CODES[uf], day=day,
                )

                # Check if http status code is valid
                http_status_code, _ = await self.get_text_from_url(url=url)
                if 200 <= http_status_code < 400:
                    gazettes_root_to_check.append((url, uf, day,))
                    remaining_dates -= 1

                current_day -= timedelta(days=1)

        logging.info(
            "Found %d urls to check: %s.",
            len(gazettes_root_to_check),
            ", ".join([str(grc[0]) for grc in gazettes_root_to_check]),
        )

        await asyncio.gather(
            *[
                self.filter_instances_gazettes(*root)
                for root in gazettes_root_to_check
            ]
        )

    async def filter_instances_gazettes(
        self, url: Union[str, URL], uf: str, day: str
    ) -> None:
        """Select gazette URLs related to the requested day and UF."""

        http_status_code = 0

        (
            http_status_code,
            gazettes_of_the_day_text,
        ) = await self.get_text_from_url(url=url)

        if http_status_code >= 400:
            logging.info("No valid content from %s.", url)
            return

        gazettes_tree = html.fromstring(gazettes_of_the_day_text)

        path = URL(url).path

        xpath = "".join(
            [
                f"//a[contains(@href, '{path}') and ",
                " or ".join(
                    [
                        f"contains(@href, '{partial}')"
                        for partial in _JUSBRASIL_GAZETTES_PARTIAL_URLs
                    ]
                ),
                "]/@href",
            ]
        )

        instances_urls = set(
            relative_url
            for relative_url in gazettes_tree.xpath(xpath)
            if relative_url[-1] != "/"
        )

        logging.info(
            "Found %d instances for %s gazette for %s via %s.",
            len(instances_urls),
            day,
            uf,
            url,
        )

        await asyncio.gather(
            *[
                self.dispatch_pages(URL(url).with_path(relative_url), uf)
                for relative_url in instances_urls
            ]
        )

    async def dispatch_pages(self, url: Union[str, URL], uf: str) -> None:
        """Retrieve number of pages of a gazette and dispatch pages."""

        (
            http_status_code,
            an_instance_gazette_text,
        ) = await self.get_text_from_url(url=url)

        if http_status_code >= 400:
            logging.info("No valid content from %s.", url)
            return

        gazette_tree = html.fromstring(an_instance_gazette_text)

        last_page_xpath = gazette_tree.xpath(
            "//select[@name='view_page']/option[last()]/text()"
        )

        last_page = int(last_page_xpath.pop())

        logging.info("Found %d pages from %s.", last_page, url)

        await asyncio.gather(
            *[
                self.parse_page(URL(url).with_query(f"view_page={page}"), uf)
                for page in range(1, last_page + 1)
            ]
        )

    async def parse_page(self, url: Union[str, URL], uf: str) -> None:
        """Retrieve lawsuits ids from a gazette's page content."""

        http_status_code, gazette_page_text = await self.get_text_from_url(
            url=url
        )

        if http_status_code >= 400:
            logging.info("No valid content from %s.", url)
            return

        local_id_set = set()

        for match in BRAZILIAN_LAWSUIT_ID_FORMAT.findall(gazette_page_text):
            # Store only matches' full_lawsuit_id.
            local_id_set.add(match[0])

        async with self.lock:
            self.id_.update(local_id_set)

        logging.info(
            "Found %d lawsuit ids from %s gazettes via %s.",
            len(local_id_set),
            uf,
            url,
        )


@click.command()
@click.version_option(__version__, "-V", "--version")
@click.help_option("-h", "--help")
@click.option(
    "-s",
    "--start-date",
    type=click.DateTime(formats=("%Y-%m-%d",)),
    default=lambda: date.today().strftime("%Y-%m-%d"),
    help="Starting date to retrieve from gazettes. Defaults to today.",
)
@click.option(
    "-d",
    "--days",
    default=1,
    type=int,
    help="Days to retrieve from gazettes. Defaults to 1.",
)
@click.argument(
    "uf_code", nargs=-1, required=True, callback=validate_uf_codes_parameter,
)
async def retrieve_brazilian_uf_lawsuit_ids(uf_code, start_date, days) -> None:
    """Retrieves Brazilian UF lawsuit identifications.

    UF_CODE is one or more UF code to be retrieved from.
    """
    async with BrazilianLawsuitIDsRetriever(
        start_date_=start_date, uf_codes=uf_code, days_to_check_=days,
    ) as retrieve:
        id_ = await retrieve.consumer_flow(reset=False)

    print("\n".join(sorted(id_)))


if __name__ == "__main__":
    retrieve_brazilian_uf_lawsuit_ids(_anyio_backend="asyncio")
